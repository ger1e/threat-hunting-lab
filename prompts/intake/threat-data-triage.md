---
id: threat-data-triage
title: Threat data triage
stage: intake
source:
  provider: Feedly
  upstream_id: R4-01
  url: https://github.com/feedly/skills/tree/main/prompts/feedly-complete-cti-prompt-library
adaptation: ger1e-threat-hunting-lab
consumes:
  - source_material
  - provenance
produces:
  - triaged_threat_data
requires:
  - source_citations
gates:
  - no_query_generation
  - evidence_inference_separation
next:
  - ioc-extract-enrich
  - hunt-lead-extraction
---
# Threat data triage

Reduce mixed reporting into source-supported claims, observables, behaviors, affected technology, temporal context, and candidate analyst actions. Preserve provenance for every material claim.

Do not generate KQL or detection rules. Do not infer product presence, actor attribution, campaign identity, or exploitation status from industry prevalence. Missing evidence is `Unknown` or `Not stated in source`.
