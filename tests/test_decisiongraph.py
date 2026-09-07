import json
import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path

from decisiongraph.ciso_assistant import import_framework_catalog
from decisiongraph.adapters import aws_privileged_mfa_receipt, kubernetes_audit_receipt, log_query_receipt
from decisiongraph.board import build_board_pack, render_board_markdown
from decisiongraph.crossmap import CrossMapRegistry
from decisiongraph.economics import calculate_economics
from decisiongraph.engine import DecisionGraph
from decisiongraph.evidence import evidence_digest, qualify_evidence
from decisiongraph.models import CrossMapping, EvidenceClass, EvidenceReceipt, MappingStrength, Qualification, Verdict
from decisiongraph.risk import RiskDistribution, simulate_loss
from decisiongraph.revenue import Attribution, Opportunity, evaluate_opportunity


NOW = datetime(2026, 9, 7, tzinfo=timezone.utc)


def receipt(**overrides):
    values = {
        "evidence_id": "ev-001",
        "evidence_class": EvidenceClass.OBSERVED,
        "resource": "arn:aws:iam::123:role/admin",
        "collector": "aws-iam@1.0.0",
        "observed_at": "2026-09-06T00:00:00Z",
        "valid_until": "2026-09-08T00:00:00Z",
        "digest": evidence_digest(b"fixture"),
        "scope": ("production", "identity"),
        "source_uri": "fixture://aws/iam",
        "statement": "MFA is enabled for the privileged identity.",
    }
    values.update(overrides)
    return EvidenceReceipt(**values)


class EvidenceTests(unittest.TestCase):
    def test_qualified_receipt(self):
        result = qualify_evidence(receipt(), required_scope={"production"}, now=NOW)
        self.assertEqual(result.status, Qualification.QUALIFIED)
        self.assertTrue(all(value is Verdict.PASS for value in result.checks.values()))

    def test_expired_receipt(self):
        result = qualify_evidence(receipt(valid_until="2026-09-01T00:00:00Z"), required_scope={"production"}, now=NOW)
        self.assertEqual(result.status, Qualification.EXPIRED)

    def test_bad_digest_rejected(self):
        self.assertEqual(qualify_evidence(receipt(digest="bad"), required_scope={"production"}, now=NOW).status, Qualification.REJECTED)

    def test_wrong_scope_rejected(self):
        self.assertEqual(qualify_evidence(receipt(), required_scope={"payments"}, now=NOW).status, Qualification.REJECTED)

    def test_missing_provenance_rejected(self):
        self.assertEqual(qualify_evidence(receipt(collector=""), required_scope={"production"}, now=NOW).status, Qualification.REJECTED)

    def test_unavailable_is_unknown(self):
        result = qualify_evidence(receipt(evidence_class=EvidenceClass.UNAVAILABLE), required_scope={"production"}, now=NOW)
        self.assertEqual(result.status, Qualification.UNKNOWN)
        self.assertNotEqual(result.status, Qualification.QUALIFIED)

    def test_naive_timestamp_rejected(self):
        with self.assertRaises(ValueError):
            qualify_evidence(receipt(valid_until="2026-09-08T00:00:00"), required_scope={"production"}, now=NOW)

    def test_digest_is_stable(self):
        self.assertEqual(evidence_digest(b"fixture"), evidence_digest(b"fixture"))


class CrossMapTests(unittest.TestCase):
    def setUp(self):
        self.mapping = CrossMapping("SOC2:CC6.1", "ISO27001:A.5.15", MappingStrength.SUBSTANTIAL, 85, "scope overlaps", "reviewer", "1.0")

    def test_direct_mapping(self):
        self.assertEqual(CrossMapRegistry([self.mapping]).find("SOC2:CC6.1", "ISO27001:A.5.15"), self.mapping)

    def test_reverse_not_inferred(self):
        self.assertIsNone(CrossMapRegistry([self.mapping]).find("ISO27001:A.5.15", "SOC2:CC6.1"))

    def test_transitive_not_inferred(self):
        second = CrossMapping("ISO27001:A.5.15", "NIST:AC-1", MappingStrength.RELATED, 45, "related", "reviewer", "1.0")
        self.assertIsNone(CrossMapRegistry([self.mapping, second]).find("SOC2:CC6.1", "NIST:AC-1"))

    def test_exact_requires_full_coverage(self):
        with self.assertRaises(ValueError):
            CrossMapRegistry([CrossMapping("a", "b", MappingStrength.EXACT, 99, "r", "u", "1")])

    def test_coverage_bounds(self):
        with self.assertRaises(ValueError):
            CrossMapRegistry([CrossMapping("a", "b", MappingStrength.RELATED, 101, "r", "u", "1")])

    def test_average_coverage(self):
        self.assertEqual(CrossMapRegistry([self.mapping]).coverage("SOC2", "ISO27001"), 85)


class EngineTests(unittest.TestCase):
    def test_control_passes_with_qualified_evidence(self):
        graph = DecisionGraph(); graph.add_evidence(receipt()); graph.map_control("CC6.1", {"ev-001"})
        self.assertEqual(graph.evaluate("CC6.1", required_scope={"production"}, now=NOW).verdict, Verdict.PASS)

    def test_control_fails_with_expired_evidence(self):
        graph = DecisionGraph(); graph.add_evidence(receipt(valid_until="2026-09-01T00:00:00Z")); graph.map_control("CC6.1", {"ev-001"})
        self.assertEqual(graph.evaluate("CC6.1", required_scope={"production"}, now=NOW).verdict, Verdict.FAIL)

    def test_no_evidence_is_unknown(self):
        self.assertEqual(DecisionGraph().evaluate("CC6.1", required_scope={"production"}, now=NOW).verdict, Verdict.UNKNOWN)

    def test_duplicate_evidence_rejected(self):
        graph = DecisionGraph(); graph.add_evidence(receipt())
        with self.assertRaises(ValueError): graph.add_evidence(receipt())

    def test_unknown_mapping_rejected(self):
        with self.assertRaises(ValueError): DecisionGraph().map_control("CC6.1", {"missing"})


class EconomicsTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.inputs = json.loads(Path("catalog/economics.json").read_text())
        cls.result = calculate_economics(cls.inputs)

    def test_labor_savings(self): self.assertEqual(self.result["annual_labor_savings"], 123750)
    def test_unconfirmed_values_excluded(self): self.assertEqual(self.result["excluded_value"], 4100000)
    def test_recognized_value(self): self.assertEqual(self.result["recognized_value"], 723750)
    def test_first_year_cost(self): self.assertEqual(self.result["first_year_cost"], 216000)
    def test_net_value(self): self.assertEqual(self.result["first_year_net_value"], 507750)
    def test_roi_is_reconcilable(self): self.assertEqual(self.result["first_year_roi_pct"], 235.07)
    def test_payback_is_reconcilable(self): self.assertEqual(self.result["payback_months"], 3.58)
    def test_zero_cost_safe(self):
        values = dict(self.inputs); values["annual_platform_cost"] = 0; values["implementation_cost"] = 0
        self.assertEqual(calculate_economics(values)["first_year_roi_pct"], 0)


class RiskTests(unittest.TestCase):
    def test_deterministic_simulation(self):
        args = (RiskDistribution(.05, .18, .55), RiskDistribution(500000, 1800000, 6500000))
        self.assertEqual(simulate_loss(*args, iterations=1000), simulate_loss(*args, iterations=1000))

    def test_percentiles_ordered(self):
        out = simulate_loss(RiskDistribution(.05, .18, .55), RiskDistribution(500000, 1800000, 6500000), iterations=1000)
        self.assertLessEqual(out["p10"], out["p50"]); self.assertLessEqual(out["p50"], out["p90"])

    def test_invalid_distribution_rejected(self):
        with self.assertRaises(ValueError): simulate_loss(RiskDistribution(2, 1, 3), RiskDistribution(1, 2, 3))

    def test_minimum_iterations(self):
        with self.assertRaises(ValueError): simulate_loss(RiskDistribution(0, 1, 2), RiskDistribution(1, 2, 3), iterations=10)


class CisoAssistantTests(unittest.TestCase):
    def test_sample_import(self):
        result = import_framework_catalog(json.loads(Path("catalog/ciso-assistant-sample.json").read_text()))
        self.assertEqual(result["framework_count"], 3)
        self.assertEqual(result["provider"], "ciso-assistant")

    def test_results_shape_import(self):
        self.assertEqual(import_framework_catalog({"results": [{"id": 1, "name": "Test"}]})["framework_count"], 1)

    def test_missing_list_rejected(self):
        with self.assertRaises(ValueError): import_framework_catalog({})

    def test_missing_identifier_rejected(self):
        with self.assertRaises(ValueError): import_framework_catalog({"frameworks": [{}]})


class AdapterTests(unittest.TestCase):
    def test_aws_adapter_is_order_independent(self):
        users = [{"UserName": "b", "Privileged": True, "MFAActive": True}, {"UserName": "a", "Privileged": True, "MFAActive": False}]
        one = aws_privileged_mfa_receipt(users, account_id="123", observed_at="2026-09-07T00:00:00Z", valid_until="2026-09-08T00:00:00Z")
        two = aws_privileged_mfa_receipt(list(reversed(users)), account_id="123", observed_at="2026-09-07T00:00:00Z", valid_until="2026-09-08T00:00:00Z")
        self.assertEqual(one.digest, two.digest)

    def test_aws_adapter_reports_missing_mfa(self):
        value = aws_privileged_mfa_receipt([{"UserName": "admin", "Privileged": True, "MFAActive": False}], account_id="123", observed_at="2026-09-07T00:00:00Z", valid_until="2026-09-08T00:00:00Z")
        self.assertIn("admin", value.statement)

    def test_kubernetes_adapter_reports_terminal_stage(self):
        events = [{"auditID": "1", "verb": "create", "stage": "ResponseComplete", "user": {"username": "alice"}}, {"auditID": "2", "verb": "get", "stage": "RequestReceived", "user": {"username": "bob"}}]
        value = kubernetes_audit_receipt(events, cluster="prod", observed_at="2026-09-07T00:00:00Z", valid_until="2026-09-08T00:00:00Z")
        self.assertIn("1/2", value.statement)

    def test_kubernetes_adapter_detects_missing_identity(self):
        value = kubernetes_audit_receipt([{"auditID": "1", "stage": "Panic"}], cluster="prod", observed_at="2026-09-07T00:00:00Z", valid_until="2026-09-08T00:00:00Z")
        self.assertIn("1 lack", value.statement)

    def test_log_backends_supported(self):
        for backend in ("elastic", "opensearch", "victorialogs", "wazuh"):
            value = log_query_receipt(backend=backend, endpoint_alias="prod", query="failure", result=[{"id": 1}], observed_at="2026-09-07T00:00:00Z", valid_until="2026-09-08T00:00:00Z")
            self.assertEqual(value.evidence_class, EvidenceClass.OBSERVED)

    def test_unknown_log_backend_rejected(self):
        with self.assertRaises(ValueError):
            log_query_receipt(backend="unknown", endpoint_alias="prod", query="x", result=[], observed_at="2026-09-07T00:00:00Z", valid_until="2026-09-08T00:00:00Z")

    def test_empty_log_query_rejected(self):
        with self.assertRaises(ValueError):
            log_query_receipt(backend="elastic", endpoint_alias="prod", query="", result=[], observed_at="2026-09-07T00:00:00Z", valid_until="2026-09-08T00:00:00Z")


class BoardPackTests(unittest.TestCase):
    def setUp(self):
        self.payload = json.loads(Path("catalog/board-decision.json").read_text())

    def test_board_pack_is_deterministic(self):
        one = build_board_pack(self.payload, generated_at="2026-09-07T00:00:00Z")
        two = build_board_pack(self.payload, generated_at="2026-09-08T00:00:00Z")
        self.assertEqual(one["pack_sha256"], two["pack_sha256"])

    def test_board_pack_requires_alternatives(self):
        payload = dict(self.payload); payload["options"] = payload["options"][:1]
        with self.assertRaises(ValueError): build_board_pack(payload)

    def test_recommendation_must_exist(self):
        payload = dict(self.payload); payload["recommended_option"] = "Missing"
        with self.assertRaises(ValueError): build_board_pack(payload)

    def test_board_pack_requires_evidence(self):
        payload = dict(self.payload); payload["evidence_ids"] = []
        with self.assertRaises(ValueError): build_board_pack(payload)

    def test_markdown_contains_decision_and_receipt(self):
        markdown = render_board_markdown(build_board_pack(self.payload, generated_at="2026-09-07T00:00:00Z"))
        self.assertIn("Targeted remediation", markdown)
        self.assertIn("Receipt:", markdown)


class RevenueTests(unittest.TestCase):
    def opportunity(self, **changes):
        values = {"opportunity_id": "OPP-1", "contract_value": 2400000, "grc_blocker": "Evidence gap", "opened_at": "2026-09-01", "resolved_at": "2026-09-18", "commercial_owner_confirmed": True, "automation_contribution_pct": 35, "attribution": Attribution.DIRECT, "finance_approved_attributable_value": 420000}
        values.update(changes)
        return Opportunity(**values)

    def test_confirmed_resolved_direct_value_recognized(self):
        result = evaluate_opportunity(self.opportunity())
        self.assertEqual(result["confirmed_contract_value_unblocked"], 2400000)
        self.assertEqual(result["recognized_value_for_roi"], 420000)
        self.assertTrue(result["included_in_recognized_value"])

    def test_unconfirmed_direct_value_excluded(self):
        result = evaluate_opportunity(self.opportunity(commercial_owner_confirmed=False))
        self.assertEqual(result["confirmed_contract_value_unblocked"], 0)
        self.assertEqual(result["recognized_value_for_roi"], 0)

    def test_unresolved_direct_value_excluded(self):
        result = evaluate_opportunity(self.opportunity(resolved_at=None))
        self.assertEqual(result["confirmed_contract_value_unblocked"], 0)

    def test_contributory_value_not_recognized(self):
        result = evaluate_opportunity(self.opportunity(attribution=Attribution.CONTRIBUTORY))
        self.assertEqual(result["confirmed_contract_value_unblocked"], 0)
        self.assertEqual(result["modeled_weighted_influence"], 840000)

    def test_capacity_has_no_weighted_revenue(self):
        result = evaluate_opportunity(self.opportunity(attribution=Attribution.CAPACITY))
        self.assertEqual(result["modeled_weighted_influence"], 0)

    def test_invalid_contribution_rejected(self):
        with self.assertRaises(ValueError): evaluate_opportunity(self.opportunity(automation_contribution_pct=101))

    def test_missing_blocker_rejected(self):
        with self.assertRaises(ValueError): evaluate_opportunity(self.opportunity(grc_blocker=""))

    def test_finance_value_cannot_exceed_contract(self):
        with self.assertRaises(ValueError): evaluate_opportunity(self.opportunity(finance_approved_attributable_value=2400001))


if __name__ == "__main__": unittest.main()
