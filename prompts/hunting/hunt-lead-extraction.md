---
id: hunt-lead-extraction
title: Hunt lead extraction and prioritization
stage: lead
source:
  provider: Feedly
  upstream_id: R2-07
  url: https://github.com/feedly/skills/blob/main/prompts/feedly-complete-cti-prompt-library/R2-07-hunt-lead-extraction-prioritization.md
adaptation: ger1e-threat-hunting-lab
consumes:
  - normalized_cti
  - provenance
produces:
  - prioritized_hunt_leads
requires:
  - source_citations
gates:
  - no_query_generation
  - no_detection_rules
  - no_full_hypothesis
next:
  - hunt-feasibility
---
# Hunt lead extraction

Generate candidate hunt leads, not hunts. Each lead must identify a specific source-supported observable behavior or artifact worth investigating, expected data sources, priority, confidence, source citation, analyst-review items, and discarded signals.

Do not generate KQL, detection rules, or a full hunt hypothesis at this stage. Do not invent telemetry availability. Leads advance only to feasibility assessment.
