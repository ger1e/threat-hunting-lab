<p align="center">
  <img src="assets/lab-signal.svg" alt="GER1E threat hunting lab — hypothesis to tuned evidence" width="100%">
</p>

# THREAT HUNTING LAB

`GER1E // PUBLIC SIGNAL SET`

Sanitized, vendor-practical examples of how I structure threat hunts and CTI-oriented detection work. No customer data, private architecture, production identifiers, credentials, or proprietary incident material belongs here.

```text
STATUS      PUBLIC / SANITIZED
MODEL       HYPOTHESIS → TELEMETRY → QUERY → EVIDENCE → TUNING
PLATFORM    MICROSOFT DEFENDER XDR / SENTINEL
LANGUAGE    KQL
PRIORITY    BEHAVIOR + CONTEXT + EVIDENCE
```

## Hunt set

The queries in this repository are public examples of the methodology, not a ranked or representative list of real-world hunting priorities.

| Hunt | Signal | Primary telemetry |
| --- | --- | --- |
| [`device-code-follow-on.kql`](hunts/device-code-follow-on.kql) | OAuth device-code authentication requiring contextual investigation | `AADSignInEventsBeta` |
| [`rare-outbound-beaconing.kql`](hunts/rare-outbound-beaconing.kql) | low-volume periodic outbound behavior | `DeviceNetworkEvents` |
| [`suspicious-powershell-encoded-command.kql`](hunts/suspicious-powershell-encoded-command.kql) | encoded / obfuscated PowerShell execution | `DeviceProcessEvents` |

## CTI normalization

[`cti-schema.json`](cti-schema.json) is a compact normalization contract for API-driven enrichment. It separates source/provenance, observable value/type, actor or campaign context, confidence, temporal fields, and ingestion metadata so enrichment does not erase where evidence came from.

## Hunt contract

Every hunt should answer these before the first operator runs:

1. What falsifiable behavior is being tested?
2. Which telemetry must exist for the query to mean anything?
3. What ATT&CK behavior is relevant, and what is merely adjacent?
4. What should an analyst inspect in the returned rows?
5. Which legitimate behaviors are expected to collide with the signal?
6. How should the query be tuned without deleting the behavior being hunted?

Each `.kql` file carries a standard header: `Title` · `Description` · `Suspicious Behavior` · `MITRE ATT&CK` · `Pyramid of Pain` · `Kill Chain` · `Relevant CTI`.

CI rejects hunts that drop this context. A query without telemetry assumptions and investigation context is decorative syntax.

## Method

```text
HYPOTHESIS
   ↓
TELEMETRY READINESS
   ↓
CHEAP FILTERS / EARLY AGGREGATION
   ↓
INVESTIGATION-USEFUL OUTPUT
   ↓
FALSE-POSITIVE ANALYSIS
   ↓
TUNING / COVERAGE / GAP RECORD
```

- State a falsifiable hypothesis.
- Name the telemetry required before writing the query.
- Aggregate early and project only investigation-useful fields.
- Separate observed evidence from inference.
- Record ATT&CK mapping, expected false positives, and tuning guidance.
- Treat IOC matches as leads; behavior and context decide priority.

## Contribution standard

See [`CONTRIBUTING.md`](CONTRIBUTING.md). Pull requests use a hunt-focused template that forces telemetry assumptions, analyst value, ATT&CK scope, false-positive analysis, provenance, and a public-safety check into the review path.

## Safety boundary

This repository is intentionally sanitized. Do not submit customer telemetry, real internal hostnames, tenant identifiers, private infrastructure, credentials, unpublished incident evidence, or material that cannot be safely made public. See [`SECURITY.md`](SECURITY.md) for disclosure guidance and scope.

## License

MIT. See [`LICENSE`](LICENSE). The license covers the public example material in this repository; third-party names, trademarks, and linked intelligence sources remain the property of their respective owners.
