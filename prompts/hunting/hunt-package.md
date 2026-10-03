---
id: hunt-package
title: Hunt package assembly
stage: hypothesis
source:
  provider: Feedly
  upstream_id: R3-07
  url: https://github.com/feedly/skills/tree/main/prompts/feedly-complete-cti-prompt-library
adaptation: ger1e-threat-hunting-lab
consumes:
  - hunt_hypothesis
  - feasibility_assessment
produces:
  - hunt_package
requires:
  - source_citations
gates:
  - feasibility_required
next:
  - sentinel-kql-opportunities
---
# Hunt package

Package one or more source-supported, feasibility-checked hypotheses with provenance, scope, telemetry requirements, benign explanations, falsifiers, and analyst next actions.

Do not bypass feasibility, infer unavailable telemetry, or claim execution results. This is an investigation package, not evidence that the behavior occurred.
