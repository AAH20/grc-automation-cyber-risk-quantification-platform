# CISO Assistant 150+ Framework Integration

## Objective

Consume the framework catalog available to an authorized CISO Assistant deployment, preserve its identifiers and versions, and connect those requirements to independently qualified evidence on the intended `a2zsoc.com` hosted plane.

The upstream library count changes as CISO Assistant adds or updates content. Product language therefore says **150+ integration-ready** rather than hard-coding an exact permanent count.

## Import contract

The reference adapter accepts a JSON object containing `frameworks`, `results`, or `objects`. Each record requires an `urn`, `id`, or `name`. It emits only normalized metadata:

```json
{
  "external_id": "urn:intuitem:risk:library:iso27001",
  "name": "ISO/IEC 27001",
  "version": "2022",
  "provider": "ciso-assistant"
}
```

Production integrations should use the supported CISO Assistant API/export mechanism and the organization's authorized framework content. This repository does not redistribute upstream libraries.

## Mapping contract

Every mapping requires:

- source and target requirement identifiers;
- direction;
- mapping strength;
- explicit coverage percentage;
- rationale;
- source citations when authoritative content is available;
- reviewer;
- version; and
- review/expiration date in production.

Mappings can reduce duplicate work. They cannot automatically transfer a control verdict or evidence conclusion between requirements.

## Qualification contract

Cross-mapping answers, “How do these objectives relate?” Evidence qualification answers, “Does this evidence actually support this control in this scope, at this time?” These conclusions are stored separately.

An evidence receipt is qualified only if provenance, integrity, freshness, scope, and relevance pass. Unavailable evidence produces UNKNOWN. Expired or invalid evidence cannot satisfy a control.

## Sync behavior

Recommended production flow:

1. Import framework metadata from CISO Assistant.
2. Detect new versions and requirements.
3. Preserve previous mapping versions.
4. Flag mappings requiring review.
5. Qualify evidence within the tenant boundary or hosted plane.
6. Export conclusions, evidence references, and reviewer decisions.
7. Never overwrite authoritative upstream framework content.
