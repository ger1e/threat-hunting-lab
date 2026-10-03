---
id: incident-sitrep
title: CTI incident SITREP
stage: reporting
source:
  provider: Feedly
  upstream_id: R4-07
  url: https://github.com/feedly/skills/tree/main/prompts/feedly-complete-cti-prompt-library
adaptation: ger1e-threat-hunting-lab
consumes:
  - evidence
  - source_claims
  - analyst_inference
produces:
  - incident_sitrep
requires:
  - source_citations
gates:
  - evidence_inference_separation
next:
---
# Incident SITREP

Summarize current incident intelligence with timestamps and scope. Separate observed facts, external source claims, analyst inference, confidence, limitations, unanswered intelligence gaps, and immediate collection or validation needs.

Do not report absence of evidence as evidence of absence when collection is incomplete.
