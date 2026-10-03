---
id: multi-feed-consolidation
title: Multi-feed intelligence consolidation
stage: intake
source:
  provider: Feedly
  upstream_id: R4-02
  url: https://github.com/feedly/skills/tree/main/prompts/feedly-complete-cti-prompt-library
adaptation: ger1e-threat-hunting-lab
consumes:
  - source_material
  - provenance
produces:
  - consolidated_intelligence
requires:
  - source_citations
gates:
  - no_query_generation
  - independent_corroboration_required
next:
  - threat-data-triage
  - hunt-lead-extraction
---
# Multi-feed consolidation

Consolidate multiple reports while tracking the original reporting chain. Distinguish apparent corroboration from independent corroboration and identify when several publishers repeat one upstream source.

Do not generate KQL. Do not increase confidence merely because the same claim appears in multiple secondary reports. Preserve disagreements, timestamps, origin ambiguity, and unresolved intelligence gaps.
