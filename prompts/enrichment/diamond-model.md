---
id: diamond-model
title: Diamond Model relationship analysis
stage: enrichment
source:
  provider: Feedly
  upstream_id: R3-03
  url: https://github.com/feedly/skills/tree/main/prompts/feedly-complete-cti-prompt-library
adaptation: ger1e-threat-hunting-lab
consumes:
  - source_material
produces:
  - diamond_model
requires:
  - source_citations
gates:
  - evidence_inference_separation
next:
  - hunt-lead-extraction
  - structured-threat-assessment
---
# Diamond Model

Structure source-supported relationships among adversary, capability, infrastructure, and victim. For every relationship, label whether it is directly observed, reported by a source, or analyst inference.

Do not invent missing vertices to complete the model. Preserve uncertainty, temporal context, and competing explanations.
