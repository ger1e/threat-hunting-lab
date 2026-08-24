### CONTRIBUTING

This repository is a public, sanitized threat-hunting lab. Contributions should improve detection quality, reproducibility, analyst usability, or telemetry clarity without introducing customer data or operationally sensitive material.

#### Submission contract

Every new hunt should include:

- a falsifiable hunting hypothesis;
- required telemetry and table assumptions;
- a standard header covering title, description, suspicious behavior, MITRE ATT&CK, Pyramid of Pain, Kill Chain, and relevant CTI;
- investigation-useful output fields;
- expected legitimate collisions / false positives;
- tuning guidance that preserves the behavior being hunted;
- source provenance for external intelligence;
- sanitized examples only.

#### Query quality

Prefer cheap filters and early aggregation. Avoid unnecessary joins, wildcard projections, giant dynamic payloads, and dependencies on nonstandard tables unless clearly marked optional. A query that returns rows but cannot support an analyst decision is not finished.

#### Safety boundary

Do not submit customer names, private hostnames, tenant identifiers, internal IP ranges, credentials, unpublished incident evidence, proprietary architecture, or anything copied from a production environment without explicit authorization for public release.

#### Pull requests

Keep PRs narrow. Explain the hypothesis, telemetry assumptions, ATT&CK mapping, expected false positives, and what changed. If a hunt is derived from public CTI, link the original source rather than an aggregator where possible.
