# Threat hunting lab

Sanitized, vendor-practical examples of how I structure hunts and CTI-oriented detection work. No customer data, private architecture, production identifiers, or proprietary incident material is included.

## Contents

- `hunts/suspicious-powershell-encoded-command.kql` — suspicious encoded/obfuscated PowerShell execution.
- `hunts/device-code-follow-on.kql` — device-code authentication followed by unusual activity.
- `hunts/rare-outbound-beaconing.kql` — low-volume periodic outbound network behavior.
- `cti-schema.json` — compact normalization schema for API-driven threat-intelligence enrichment.

## Method

1. State a falsifiable hypothesis.
2. Name the telemetry required before writing the query.
3. Aggregate early and project only investigation-useful fields.
4. Separate observed evidence from inference.
5. Record ATT&CK mapping, expected false positives, and tuning guidance.
6. Treat IOC matches as leads; behavior and context decide priority.
