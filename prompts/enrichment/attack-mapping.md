---
id: attack-mapping
title: Evidence-bounded ATT&CK mapping
stage: mapping
source:
  provider: Feedly
  upstream_id: R3-02
  url: https://github.com/feedly/skills/tree/main/prompts/feedly-complete-cti-prompt-library
adaptation: ger1e-threat-hunting-lab
consumes:
  - source_supported_behaviors
produces:
  - attack_mapping
requires:
  - source_citations
gates:
  - no_unverified_attack_ids
  - evidence_inference_separation
next:
  - hunt-lead-extraction
  - structured-threat-assessment
---
# ATT&CK mapping

Map only behaviors supported by supplied evidence. Prefer the narrowest valid sub-technique when the procedure supports it. Separate directly evidenced mappings from inferred adjacent techniques and mark ambiguous mappings for analyst review.

Never fabricate ATT&CK IDs or fill a matrix for visual completeness. Include the source behavior and rationale beside each mapping.
