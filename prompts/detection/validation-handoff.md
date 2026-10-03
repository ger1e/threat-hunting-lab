---
id: validation-handoff
title: Detection validation handoff
stage: validation
source:
  provider: Feedly
  upstream_id: R2-06
  url: https://github.com/feedly/skills/blob/main/prompts/feedly-complete-cti-prompt-library/R2-06-detection-validation-handoff-ttp.md
adaptation: ger1e-threat-hunting-lab
consumes:
  - candidate_kql
  - telemetry_requirements
produces:
  - validation_handoff
requires:
  - analyst_validation
gates:
  - no_default_production_claim
next:
  - structured-threat-assessment
  - incident-sitrep
---
# Validation handoff

Produce detection rationale, required telemetry and fields, known limitations and evasions, false-positive sources, tuning guidance, safe validation approach, expected telemetry, pass/fail criteria, and deployment-readiness status.

KQL is the canonical local detection language. Validation must be safe and environment-specific. Candidate logic remains untested until syntax and target-environment checks pass. Never claim production readiness, deployment, or validation merely because a query was generated.
