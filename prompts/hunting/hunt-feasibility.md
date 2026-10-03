---
id: hunt-feasibility
title: Hunt feasibility and telemetry coverage
stage: feasibility
source:
  provider: Feedly
  upstream_id: R2-08
  url: https://github.com/feedly/skills/blob/main/prompts/feedly-complete-cti-prompt-library/R2-08-hunt-lead-feasibility-coverage.md
adaptation: ger1e-threat-hunting-lab
consumes:
  - prioritized_hunt_leads
  - environment_facts
produces:
  - feasibility_assessment
requires:
  - telemetry_inventory
gates:
  - unknown_coverage_stays_unknown
next:
  - hunt-hypothesis
---
# Hunt feasibility

Assess required telemetry, actual stack coverage, existing detection overlap, query complexity, analyst effort, required skills, and logging gaps before promoting a lead.

If environment or stack information is absent, mark coverage `Unknown`; never invent available telemetry. A lead that cannot be tested with available evidence should stop here with the gap documented.
