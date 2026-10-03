---
id: sentinel-kql-opportunities
title: Sentinel and Defender XDR KQL opportunities
stage: detection
source:
  provider: Feedly
  upstream_id: R2-04
  url: https://github.com/feedly/skills/blob/main/prompts/feedly-complete-cti-prompt-library/R2-04-detection-opportunity-generator-sentinel-kql.md
adaptation: ger1e-threat-hunting-lab
consumes:
  - hunt_hypothesis
  - required_telemetry
produces:
  - candidate_kql
requires:
  - telemetry_requirements
  - analyst_validation
gates:
  - untested_by_default
  - schema_uncertainty_explicit
next:
  - validation-handoff
---
# Sentinel KQL opportunities

Generate candidate Microsoft Defender XDR / Microsoft Sentinel KQL only for source-supported, feasible behavior. State exact required telemetry and tables. Match telemetry to behavior rather than convenient strings.

Time-bound both sides of every join. Prefer early filters and aggregation where investigation value is preserved; avoid broad joins when staged correlation is sufficient. Preserve fields required for the analyst's next action.

Do not present uncertain fields or `ActionType` values as certain. Label schema assumptions for analyst verification. IOC-only logic is short-lived and should have a behavioral complement where feasible. Include false-positive sources and tuning guidance.

Generated KQL is **untested by default**. It is not production-ready, validated, deployed, or proven until the repository syntax gate and an analyst in the target environment validate it.
