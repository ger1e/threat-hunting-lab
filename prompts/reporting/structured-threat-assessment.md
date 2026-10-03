---
id: structured-threat-assessment
title: Structured technical threat assessment
stage: reporting
source:
  provider: Feedly
  upstream_id: R2-11
  url: https://github.com/feedly/skills/tree/main/prompts/feedly-complete-cti-prompt-library
adaptation: ger1e-threat-hunting-lab
consumes:
  - evidence
  - source_claims
  - analyst_inference
produces:
  - technical_assessment
requires:
  - source_citations
gates:
  - evidence_inference_separation
next:
---
# Structured threat assessment

Produce a technical assessment that separately labels observed facts, source claims, analyst inference, confidence, limitations, unanswered intelligence gaps, and recommended next collection or hunting actions.

Do not smooth contradictions into certainty. Every material conclusion must be traceable to evidence or explicitly labeled inference.
