---
id: ioc-extract-enrich
title: IOC extraction and contextual enrichment
stage: enrichment
source:
  provider: Feedly
  upstream_id: R3-01
  url: https://github.com/feedly/skills/tree/main/prompts/feedly-complete-cti-prompt-library
adaptation: ger1e-threat-hunting-lab
consumes:
  - source_material
  - provenance
produces:
  - normalized_observables
requires:
  - source_citations
gates:
  - cti_schema_compatible
  - preserve_context
next:
  - attack-mapping
  - hunt-lead-extraction
---
# IOC extraction and enrichment

Extract source-supported observables using types compatible with `cti-schema.json`: IP, domain, URL, SHA-256, SHA-1, MD5, email, or other. Preserve first/last-seen context when stated and retain full URL paths when operationally relevant.

Do not flatten behavioral or campaign context into a naked IOC list. Do not invent enrichment, actor ownership, maliciousness, or timestamps. Mark missing values explicitly unknown.
