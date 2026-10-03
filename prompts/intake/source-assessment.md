---
id: source-assessment
title: Source reliability and credibility assessment
stage: intake
source:
  provider: Feedly
  upstream_id: R2-02
  url: https://github.com/feedly/skills/blob/main/prompts/feedly-complete-cti-prompt-library/R2-02-source-reliability-credibility-evaluator.md
adaptation: ger1e-threat-hunting-lab
consumes:
  - source_material
produces:
  - provenance_assessment
requires:
  - source_citations
gates:
  - evidence_inference_separation
  - unknown_stays_unknown
next:
  - threat-data-triage
  - multi-feed-consolidation
---
# Source assessment

Assess source reliability separately from information credibility. Preserve citations and distinguish originator, publisher, and secondary repetition. Flag single-sourcing, circular reporting, origin ambiguity, vendor bias, stale reporting, and context loss.

Do not turn an unknown track record into a guessed score. Use `Unknown` or `Not stated in source` when evidence is absent. Separate observed facts, source claims, and analyst inference. Do not fabricate actors, campaigns, IOCs, CVEs, ATT&CK mappings, or corroboration.

Output the source identity, reliability rationale, claim-by-claim credibility, independent versus apparent corroboration, limitations, and analyst-review items. This assessment supplements, but does not replace, the repository CTI confidence field.
