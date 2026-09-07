# Privileged production access remediation

**Decision ID:** BD-2026-014
**Decision owner:** CISO
**Decision due:** 2026-10-01

## Decision context

- Business objective: Reduce material access risk without delaying priority delivery
- Current P50 exposure: $1,840,000
- Risk tolerance: $750,000

## Alternatives

| Alternative | Cost | P50 residual exposure | Time | Business impact |
|---|---:|---:|---:|---|
| Accept current risk | $0 | $1,840,000 | 0 days | Preserves capacity but remains above tolerance |
| Targeted remediation | $180,000 | $540,000 | 60 days | Best risk-adjusted return |
| Full redesign | $720,000 | $210,000 | 270 days | Lowest exposure with roadmap delay |

## Recommended decision

Targeted remediation

## Evidence lineage

- `aws-iam-mfa-123`
- `k8s-audit-prod`
- `log-query-elastic-security`

Receipt: `eb16aba3251fde92fea4ed4077f524b0ed23600124e0156310b78f998ec5c58f`
