# CTI Prompt Orchestration

The prompt layer converts external reporting into bounded analyst artifacts while preserving the repository lifecycle:

`SOURCE -> PROVENANCE -> CLAIM -> RELEVANCE -> OBSERVABLE BEHAVIOR -> TELEMETRY -> HYPOTHESIS -> QUERY -> EVIDENCE -> CONFIDENCE`

Authoritative doctrine:
- [Hunting methodology](HUNTING-METHODOLOGY.md)
- [CTI normalization](CTI-NORMALIZATION.md)

The prompt contracts describe allowed reasoning transitions. They are not an autonomous execution engine.

## Route 1: Threat report to hunt hypothesis

`source-assessment -> threat-data-triage -> hunt-lead-extraction -> hunt-feasibility -> hunt-hypothesis`

Use this when a report contains potentially huntable behavior but environment coverage has not yet been established. The feasibility gate prevents a compelling report from becoming imaginary telemetry.

## Route 2: Vulnerability exploitation report to candidate KQL

`source-assessment -> threat-data-triage -> hunt-lead-extraction -> hunt-feasibility -> hunt-hypothesis -> sentinel-kql-opportunities -> validation-handoff`

Candidate KQL is generated only after the behavior is source-supported and feasible. The detection module must state required Defender XDR/Sentinel telemetry, schema uncertainty, false positives, tuning, and validation status. Generated KQL is untested until syntax and target-environment validation pass.

## Route 3: Incident intelligence to SITREP

`source-assessment -> ioc-extract-enrich -> attack-mapping -> incident-sitrep`

Use this when the immediate deliverable is situational awareness rather than a new hunt. The SITREP must keep observed facts, external source claims, analyst inference, confidence, limitations, and intelligence gaps separate.

## Failure behavior

If a required stage lacks evidence, telemetry, provenance, or environment facts, stop and report the gap. Use `Unknown` or `Not stated in source`; do not silently manufacture the missing link. Empty query results do not prove absence when telemetry coverage is incomplete.
