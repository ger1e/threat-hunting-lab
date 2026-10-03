---
id: executive-brief
title: Executive intelligence brief
stage: reporting
source:
  provider: Feedly
  upstream_id: R4-08
  url: https://github.com/feedly/skills/tree/main/prompts/feedly-complete-cti-prompt-library
adaptation: ger1e-threat-hunting-lab
consumes:
  - evidence
  - source_claims
  - analyst_inference
produces:
  - executive_brief
requires:
  - source_citations
gates:
  - evidence_inference_separation
next:
---
# Executive intelligence brief

Explain decision-relevant intelligence concisely while preserving epistemic boundaries. Separate observed facts, source claims, analyst inference, confidence, limitations, unanswered intelligence gaps, business relevance, and recommended decisions.

Do not exaggerate impact, attribution, exploitation, or certainty for executive readability.
