# Architecture

## Planes

1. **Source adapters** collect read-only evidence from AWS, Kubernetes, GRC, workflow, observability, identity, and commercial systems.
2. **Evidence integrity** creates immutable receipts with provenance, scope, freshness, relevance, and integrity metadata.
3. **Decision graph** links evidence, controls, requirements, risks, exceptions, owners, contracts, and decisions.
4. **Control runtime** produces deterministic PASS, FAIL, or UNKNOWN conclusions.
5. **Framework cross-map** maintains reviewed directional mappings without transitive inference.
6. **Risk engine** creates reproducible loss distributions and records uncertainty.
7. **Economics ledger** separates recognized value from excluded capacity or unconfirmed attribution.
8. **Governed agents** propose cited analysis, then pass deterministic evaluation and human approval gates.
9. **Experience plane** prepares views for operators, control owners, auditors, customers, executives, and boards.

## Hosted plane

The intended `a2zsoc.com` hosted plane provides qualification and cross-mapping APIs while allowing deployments to keep raw evidence inside their trust boundary. Production architecture should support:

- tenant-specific encryption and keys;
- OIDC workload identity;
- mTLS between collectors and qualification endpoints;
- signed receipts and append-only decision history;
- regional storage selection;
- evidence redaction before transfer;
- least-privilege, read-only adapters by default;
- webhook replay protection and idempotency; and
- export of all customer-owned records.

## System boundaries

AWS, Kubernetes, Elastic, VictoriaLogs, Vanta, Linear, CISO Assistant, and other systems remain sources or destinations. DecisionGraph does not replace their operational owners. An integration failure invalidates or ages evidence; it does not silently preserve a prior PASS.

## Non-goals for v0.1

- Automatic material risk acceptance
- Unreviewed external assurance
- Production infrastructure mutation
- Copying third-party framework content
- Treating one framework mapping as certification
- Claiming capacity pipeline as revenue
