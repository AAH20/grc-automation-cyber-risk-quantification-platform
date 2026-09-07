# GRC DecisionGraph

[![CI](https://github.com/AAH20/grc-automation-cyber-risk-quantification-platform/actions/workflows/ci.yml/badge.svg)](https://github.com/AAH20/grc-automation-cyber-risk-quantification-platform/actions/workflows/ci.yml)
[![License](https://img.shields.io/badge/license-Apache--2.0-blue.svg)](LICENSE)

**Evidence-backed GRC automation, continuous compliance, cyber-risk quantification, framework cross-mapping, AI governance, board reporting, audit readiness, and revenue assurance.**

GRC DecisionGraph connects technical evidence to control conclusions, financial exposure, unit economics, priority-contract blockers, and decision-ready board narratives. It is not another checklist or opaque compliance score.

## Why this exists

GRC teams frequently operate across disconnected systems:

```text
AWS · Kubernetes · Vanta · Linear · Elastic/VictoriaLogs
                         ↓
             verifiable evidence graph
                         ↓
       controls · frameworks · risks · owners
                         ↓
        evaluation and evolution engineering
                         ↓
    CRQ · unit economics · revenue assurance
                         ↓
        boards · auditors · priority customers
```

The platform treats infrastructure, observability, workflow, and commercial systems as replaceable evidence sources. It does not take ownership of SRE migrations or declare that a vendor integration proves a control.

## 150+ framework integration plane

GRC DecisionGraph is designed to import and preserve the framework catalog made available by the open-source [CISO Assistant](https://github.com/intuitem/ciso-assistant-community) project. That catalog lists more than 150 security, privacy, risk, resilience, AI, and regulatory frameworks; the exact upstream count can evolve.

The adapter does **not** copy, silently modify, or claim ownership of those framework libraries. It imports stable identifiers, names, and versions so organizations can:

- connect their licensed or permitted framework content;
- maintain comprehensive, directional framework cross-mappings;
- qualify evidence independently of requirement mapping;
- reuse one qualified evidence receipt across supported obligations;
- preserve source attribution and framework version history; and
- synchronize conclusions with CISO Assistant or another system of record.

The intended hosted qualification plane is `a2zsoc.com`, with tenant-controlled execution and evidence boundaries. This repository contains the portable engine and reference interface; deployment to that domain requires the domain owner's production environment and is not implied by the demo deployment.

## Cross-mapping rules

Mappings are directional and versioned:

- `EXACT`: complete semantic equivalence; requires 100% reviewed coverage.
- `SUBSTANTIAL`: most of the objective overlaps, but framework-specific work remains.
- `PARTIAL`: only an explicit portion overlaps.
- `RELATED`: useful context without satisfying the target requirement.

`A → B` and `B → C` never create an inferred `A → C`. Every mapping requires rationale, a reviewer, a version, and an explicit coverage percentage.

## Evidence qualification

Each receipt is evaluated independently across five gates:

1. **Provenance** — collector and source can be identified.
2. **Integrity** — a reproducible SHA-256 receipt exists.
3. **Freshness** — the evidence remains inside its validity window.
4. **Scope** — all required accounts, environments, assets, or processes are covered.
5. **Relevance** — the observation directly supports the control objective.

Evidence classes are `OBSERVED`, `DECLARED`, `EXERCISED`, `ATTESTED`, `INFERRED`, and `UNAVAILABLE`. Missing evidence remains `UNKNOWN`; it never silently becomes PASS.

## Evaluation and evolution loops

The **evaluation loop** measures whether evidence, controls, AI output, risk forecasts, and economics remain trustworthy. The **evolution loop** classifies failure causes, ranks changes by risk-adjusted value, tests them offline, canaries them, and requires human approval or rollback.

Agents may propose mappings, explanations, remediation alternatives, or evidence-backed drafts. They cannot autonomously approve material controls, accept risk, make external assurances, change production controls, or attribute revenue.

## Unit economics

The reference ledger distinguishes recognized from possible value:

```text
recognized value
= verified labor savings
+ confirmed direct revenue
+ validated expected-loss reduction
```

Capacity pipeline, contributory pipeline, and unconfirmed claims remain visible but are excluded from recognized value and ROI.

The controlled fixture produces:

| Metric | Value |
|---|---:|
| Verified labor savings | $123,750 |
| Confirmed direct revenue | $420,000 |
| Validated loss reduction | $180,000 |
| Recognized first-year value | $723,750 |
| First-year cost | $216,000 |
| First-year net value | $507,750 |
| First-year ROI | 235.07% |
| Modeled payback | 3.58 months |
| Excluded capacity/contributory value | $4,100,000 |

All figures are synthetic decision-support fixtures, not claims about a named organization.

## Quick start

```bash
python3 -m venv .venv
.venv/bin/pip install -e .
.venv/bin/grc-decisiongraph economics catalog/economics.json --output outputs/economics.json
.venv/bin/grc-decisiongraph risk catalog/risk.json --output outputs/risk.json
.venv/bin/grc-decisiongraph import-ciso-assistant catalog/ciso-assistant-sample.json --output outputs/frameworks.json
python3 -m unittest discover -s tests -v
```

Run the decision workspace:

```bash
npm install
npm run dev
```

## Core KPIs

### Trust and control

- evidence provenance completeness;
- freshness-SLO compliance;
- reproducible control verdict rate;
- unsupported AI claim rate;
- material false-positive and false-negative rates;
- human-approval enforcement; and
- board metrics traceable to evidence.

### GRC operations and audit

- evidence collection hours per control;
- control-review cycle time;
- first-submission evidence acceptance;
- auditor follow-up requests;
- evidence reuse rate;
- exception-resolution time; and
- cost per accepted evidence item.

### Commercial enablement

- GRC-blocked pipeline;
- median blocker age;
- priority-response SLA;
- requirements answered with reusable evidence;
- confirmed direct revenue enabled;
- contributory revenue shown separately; and
- assurance cost per priority contract.

### Board decision quality

- material risks above tolerance;
- P10/P50/P90 loss exposure;
- forecast calibration;
- risk reduction per dollar;
- decision latency; and
- realized benefit against the approved business case.

See [KPI and economics specification](docs/KPIS_AND_UNIT_ECONOMICS.md), [framework integration contract](docs/CISO_ASSISTANT_150_FRAMEWORK_INTEGRATION.md), and [architecture](docs/ARCHITECTURE.md).

## Safety boundary

- Reference records and economics are controlled synthetic fixtures.
- No external organization or product is scored.
- Framework mappings are illustrative until reviewed against authoritative content.
- The risk engine is decision support, not actuarial or financial advice.
- The UI's board packet must be reviewed by accountable owners before external use.

## License

Apache-2.0. See [LICENSE](LICENSE).
