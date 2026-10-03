# CTI Prompt Layer

This directory contains a curated, locally adapted CTI reasoning layer derived from the Feedly Complete CTI Prompt Library. It is designed to support the repository's evidence-first workflow, not replace analyst judgment or operational validation.

Upstream library: https://github.com/feedly/skills/tree/main/prompts/feedly-complete-cti-prompt-library

## Authority and provenance

`docs/HUNTING-METHODOLOGY.md` and `docs/CTI-NORMALIZATION.md` remain authoritative local doctrine. Every native prompt declares its Feedly source ID and URL, local adaptation marker, inputs, outputs, gates, and allowed downstream modules. Prompt output is analysis assistance, not ground truth.

## Stages

- `intake/`: source reliability, triage, and multi-feed consolidation.
- `enrichment/`: IOC/context normalization, ATT&CK mapping, and Diamond Model relationships.
- `hunting/`: lead extraction, feasibility, falsifiable hypothesis, and hunt packaging.
- `detection/`: candidate Sentinel/Defender XDR KQL and validation handoff.
- `reporting/`: technical assessment, SITREP, and executive brief.

Use `manifest.json` for discovery. A `next` relationship documents an allowed workflow transition; it does not execute anything automatically.

Generated detections remain untested until repository syntax checks and analyst validation in the target environment pass. Unknown evidence and telemetry coverage stay unknown. Repeated secondary reporting is not independent corroboration merely because the Internet has discovered copy and paste.
