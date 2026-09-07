# KPIs and Unit Economics

## Measurement rules

1. Establish a signed baseline with GRC and executive sponsors.
2. Store numerator, denominator, source, owner, cadence, and confidence for every KPI.
3. Separate observed, modeled, and attributed values.
4. Exclude capacity and unconfirmed claims from recognized value.
5. Reconcile value with Finance or an appointed business owner.
6. Preserve the original baseline when targets change.

## KPI dictionary

| KPI | Formula | Decision supported |
|---|---|---|
| Evidence qualification rate | qualified receipts / assessed receipts | Is collected evidence decision-ready? |
| Evidence freshness compliance | current receipts / receipts with freshness SLO | Can controls rely on current observations? |
| Reproducible verdict rate | reproduced verdicts / sampled verdicts | Can audit conclusions be independently repeated? |
| Unsupported AI claim rate | unsupported material claims / sampled material claims | Is agentic automation safe enough to scale? |
| Evidence reuse rate | reused accepted items / accepted evidence items | Are cross-mappings reducing duplicate work? |
| Priority response SLA | responses inside SLA / priority requests | Is GRC reducing commercial delay? |
| First-pass auditor acceptance | accepted first submissions / first submissions | Is audit preparation improving? |
| Risk reduction per dollar | validated expected-loss reduction / remediation cost | Which investment should leadership fund? |
| Forecast calibration error | absolute predicted minus realized outcomes / realized outcomes | Are quantified risks becoming more reliable? |
| Direct revenue confirmation | confirmed direct value / claimed direct value | Is commercial attribution defensible? |

## Value classifications

- **VERIFIED_SAVINGS** — observed reduction against an approved baseline.
- **CONFIRMED_DIRECT_REVENUE** — opportunity owner confirms a GRC blocker prevented progress until resolved.
- **VALIDATED_LOSS_REDUCTION** — approved risk model measures reduced expected loss.
- **CONTRIBUTORY_REVENUE** — GRC helped but was not the only causal factor; excluded by default.
- **CAPACITY_ONLY** — additional potential throughput; never reported as realized revenue.

## Reference formulas

```text
labor savings = (baseline hours − current hours) × annual volume × loaded rate
recognized value = verified savings + confirmed direct revenue + validated loss reduction
first-year cost = implementation cost + annual platform cost
first-year net value = recognized value − first-year cost
first-year ROI = first-year net value / first-year cost
payback months = first-year cost / (recognized value / 12)
```

The bundled controlled fixture reconciles to $723,750 recognized value, $216,000 first-year cost, $507,750 net value, 235.07% ROI, and 3.58 months payback. $4.1 million of contributory and capacity value is visible but excluded.
