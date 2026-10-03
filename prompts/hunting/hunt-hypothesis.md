---
id: hunt-hypothesis
title: Falsifiable hunt hypothesis
stage: hypothesis
source:
  provider: Feedly
  upstream_id: R1-04
  url: https://github.com/feedly/skills/tree/main/prompts/feedly-complete-cti-prompt-library
adaptation: ger1e-threat-hunting-lab
consumes:
  - feasibility_assessment
produces:
  - hunt_hypothesis
requires:
  - required_telemetry
gates:
  - falsifiable_hypothesis
next:
  - sentinel-kql-opportunities
  - hunt-package
---
# Hunt hypothesis

Use the repository hypothesis contract: **If the suspected behavior is occurring, then the required telemetry should contain observable pattern X, under conditions Y, with legitimate explanations Z considered.**

State scope, time horizon, required telemetry, falsifiers, benign collisions, expected observable behavior, and what result would weaken the hypothesis. Do not treat lack of results as proof of absence when telemetry coverage is incomplete.
