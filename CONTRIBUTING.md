<!-- GER1E-DOC-SCHEMA: v1 -->
<a id="contributing"></a>
<div align="center">

<strong>CONTRIBUTING</strong><br/>
<sub>GER1E // THREAT HUNTING LAB // DOCUMENTATION</sub>

</div>

This repository is a public, sanitized threat-hunting lab. Contributions should improve detection quality, reproducibility, analyst usability, or telemetry clarity without introducing customer data or operationally sensitive material.

<a id="submission-contract"></a>
<sub><strong>01 // Submission contract</strong></sub>

Every new hunt should include:

- a falsifiable hunting hypothesis;
- required telemetry and table assumptions;
- a standard header covering title, description, suspicious behavior, MITRE ATT&CK, Pyramid of Pain, Kill Chain, and relevant CTI;
- investigation-useful output fields;
- expected legitimate collisions / false positives;
- tuning guidance that preserves the behavior being hunted;
- source provenance for external intelligence;
- sanitized examples only.

<a id="query-quality"></a>
<sub><strong>02 // Query quality</strong></sub>

Prefer cheap filters and early aggregation. Avoid unnecessary joins, wildcard projections, giant dynamic payloads, and dependencies on nonstandard tables unless clearly marked optional. A query that returns rows but cannot support an analyst decision is not finished.

<a id="safety-boundary"></a>
<sub><strong>03 // Safety boundary</strong></sub>

Do not submit customer names, private hostnames, tenant identifiers, internal IP ranges, credentials, unpublished incident evidence, proprietary architecture, or anything copied from a production environment without explicit authorization for public release.

<a id="pull-requests"></a>
<sub><strong>04 // Pull requests</strong></sub>

Keep PRs narrow. Explain the hypothesis, telemetry assumptions, ATT&CK mapping, expected false positives, and what changed. If a hunt is derived from public CTI, link the original source rather than an aggregator where possible.

<p align="center"><sub>GER1E // THREAT HUNTING LAB // MOBILE-SAFE DOCUMENTATION</sub></p>
