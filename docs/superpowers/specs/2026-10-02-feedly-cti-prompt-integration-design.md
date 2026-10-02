# Feedly CTI Prompt Integration Design

Date: 2026-10-02
Status: Approved design
Repository: `ger1e/threat-hunting-lab`
Source library: `feedly/skills/prompts/feedly-complete-cti-prompt-library`

## 1. Purpose

Integrate the most useful workflows from Feedly's CTI prompt library into the threat-hunting lab as a curated, evidence-first prompt layer.

The integration must strengthen the repository's existing operating model rather than replace it. The governing lifecycle remains:

```text
SOURCE -> PROVENANCE -> CLAIM -> RELEVANCE -> OBSERVABLE BEHAVIOR
      -> TELEMETRY -> HYPOTHESIS -> QUERY -> EVIDENCE -> CONFIDENCE
```

Feedly-derived prompts are upstream reasoning modules. The repository's existing telemetry-readiness, provenance, evidence, KQL, false-positive, and public-safety contracts remain authoritative.

## 2. Goals

The integration must:

1. Turn external reporting into prioritized hunt leads before query generation.
2. Evaluate source reliability and claim credibility before operational use.
3. Check hunt feasibility against available telemetry and controls before analyst effort is committed.
4. Produce falsifiable hunt hypotheses that conform to the existing hunting methodology.
5. Generate Microsoft Defender XDR / Sentinel KQL opportunities without bypassing schema, performance, or validation requirements.
6. Preserve attribution to the original Feedly prompt source and distinguish source text from local adaptation.
7. Make prompt modules machine-addressable through a compact manifest without building a full orchestration application.
8. Add CI checks so prompt contracts cannot silently drift into vague or unsafe prose.

## 3. Non-goals

This change will not:

- copy all 44 Feedly prompts verbatim into the repository;
- turn the repository into an agent platform or autonomous CTI application;
- make Feedly prompts authoritative over local methodology;
- add a runtime LLM dependency;
- execute KQL against a tenant;
- claim generated detections are production-ready without validation;
- make Sigma or Splunk first-class output formats;
- add customer, tenant, incident, or other private operational data;
- resurrect PARA11AX or introduce a replacement platform abstraction.

## 4. Architectural decision

Use a curated native prompt layer.

Each imported workflow is adapted into the repository's terminology, constraints, and lifecycle. The prompt files remain independently readable, but they also expose a small machine-readable contract in front matter so later tooling can discover stage, inputs, outputs, gates, provenance, and next-stage relationships.

The prompt layer is documentation plus structured contracts, not an execution engine.

## 5. Target workflow

```text
RAW CTI
  |
  v
SOURCE / PROVENANCE ASSESSMENT
  |
  v
NORMALIZATION + IOC EXTRACTION
  |
  v
HUNT-LEAD EXTRACTION
  |
  v
ENVIRONMENT / TELEMETRY FEASIBILITY
  |
  v
FALSIFIABLE HYPOTHESIS
  |
  v
ATT&CK MAPPING
  |
  v
KQL OPPORTUNITY GENERATION
  |
  v
KQL CONTRACT + PARSER VALIDATION
  |
  v
EVIDENCE / FALSE-POSITIVE / TUNING REVIEW
  |
  v
DETECTION / GAP / SITREP / KNOWLEDGE
```

No stage may imply evidence that an earlier stage did not establish.

## 6. Repository layout

```text
prompts/
├── README.md
├── manifest.json
├── intake/
│   ├── source-assessment.md
│   ├── threat-data-triage.md
│   └── multi-feed-consolidation.md
├── enrichment/
│   ├── ioc-extract-enrich.md
│   ├── attack-mapping.md
│   └── diamond-model.md
├── hunting/
│   ├── hunt-lead-extraction.md
│   ├── hunt-feasibility.md
│   ├── hunt-hypothesis.md
│   └── hunt-package.md
├── detection/
│   ├── sentinel-kql-opportunities.md
│   └── validation-handoff.md
└── reporting/
    ├── structured-threat-assessment.md
    ├── incident-sitrep.md
    └── executive-brief.md

docs/
└── CTI-PROMPT-ORCHESTRATION.md

tests/
└── test_prompt_contracts.py
```

The directory names represent lifecycle responsibilities, not vendor taxonomy.

## 7. Prompt contract

Each native prompt must begin with YAML front matter containing at least:

```yaml
id: hunt-lead-extraction
title: Hunt lead extraction and prioritization
stage: lead
source:
  provider: Feedly
  upstream_id: R2-07
  url: https://github.com/feedly/skills/blob/main/prompts/feedly-complete-cti-prompt-library/R2-07-hunt-lead-extraction-prioritization.md
adaptation: ger1e-threat-hunting-lab
consumes:
  - source_material
  - provenance
produces:
  - prioritized_hunt_leads
requires:
  - source_citations
gates:
  - no_query_generation
  - no_unverified_attack_ids
  - evidence_inference_separation
next:
  - hunt-feasibility
```

Required semantics:

- `id`: stable repository-local identifier.
- `stage`: one of `intake`, `enrichment`, `lead`, `feasibility`, `hypothesis`, `mapping`, `detection`, `validation`, `reporting`.
- `source.provider`: upstream source organization.
- `source.upstream_id`: Feedly library identifier where applicable.
- `source.url`: exact public upstream file or report URL.
- `adaptation`: declares that the local prompt is modified, not a verbatim mirror.
- `consumes`: named inputs required for correct use.
- `produces`: named outputs promised by the prompt.
- `requires`: evidence or metadata that must be present.
- `gates`: constraints the prompt must enforce.
- `next`: allowed downstream prompt IDs.

## 8. Core modules

### 8.1 Source assessment

Adapt Feedly R2-02.

Purpose: evaluate reporting quality before intelligence drives action.

Must preserve separate axes for source reliability and information credibility. It must flag single-sourcing, circular reporting, origin ambiguity, vendor bias, recency drift, and context loss. Unknown source track record must remain unknown rather than being converted into a guessed middle score.

This module supplements the existing CTI provenance model. It does not replace the repository's 0-100 observation confidence field.

### 8.2 Threat-data triage

Adapt the useful prioritization behavior from Feedly R4-01.

Purpose: reduce a mixed intelligence input into claims, observables, behaviors, affected technology, temporal context, and candidate actions while preserving provenance.

It must not generate KQL.

### 8.3 Multi-feed consolidation

Adapt Feedly R4-02.

Purpose: combine multiple reports without falsely inflating confidence when several sources repeat one upstream originator.

The module must explicitly track apparent corroboration versus independent corroboration.

### 8.4 IOC extraction and enrichment

Adapt Feedly R3-01.

Purpose: extract normalized observables and context while remaining compatible with `cti-schema.json`.

The local prompt must preserve full URL paths and source context where they matter. It must not reduce intelligence into a flat IOC list when behavioral or campaign context is present.

### 8.5 ATT&CK mapping

Adapt Feedly R3-02 and relevant mapping guidance from R1-05.

Purpose: map only behaviors supported by the supplied source material.

Requirements:

- no fabricated ATT&CK IDs;
- prefer the narrowest valid sub-technique when the procedure supports it;
- mark ambiguous mappings for analyst review;
- separate directly evidenced techniques from inferred adjacent techniques.

### 8.6 Diamond Model

Adapt Feedly R3-03 / R1-01.

Purpose: structure adversary, capability, infrastructure, and victim relationships without converting inference into fact.

### 8.7 Hunt-lead extraction

Adapt Feedly R2-07.

Purpose: generate prioritized candidate leads, not hunts.

A lead must describe a specific observable behavior or artifact worth investigating. The prompt must prohibit KQL, detection-rule generation, and full hypotheses at this stage.

Output must include expected data sources, priority, confidence, source citation, analyst-review items, and discarded signals.

### 8.8 Hunt feasibility

Adapt Feedly R2-08.

Purpose: decide whether a lead is huntable in the stated environment before analyst time is committed.

Assessment must consider required telemetry, actual stack coverage, detection overlap, query complexity, likely effort, skills, and gaps.

If stack information is absent, coverage must be marked unknown. The prompt must never invent available telemetry.

### 8.9 Hunt hypothesis

Adapt Feedly R1-04 and R3-07, but make the repository's existing hypothesis contract authoritative.

Every hypothesis must be reducible to:

> If the suspected behavior is occurring, then the required telemetry should contain observable pattern X, under conditions Y, with legitimate explanations Z considered.

The prompt must explicitly include falsifiers, benign collisions, scope, time horizon, and required telemetry.

### 8.10 Sentinel KQL opportunities

Adapt Feedly R2-04 heavily.

Purpose: translate a validated behavior or hypothesis into candidate Microsoft Defender XDR / Sentinel KQL.

Local rules:

- Defender XDR / Sentinel first.
- Prefer the repository's known Microsoft tables and semantics.
- Match telemetry to the behavior, not to convenient string searches.
- Time-bound both sides of every join.
- Prefer early filters and aggregation when investigation value is preserved.
- Avoid broad joins where staged correlation is sufficient.
- Preserve fields needed for the analyst's next action.
- Do not present uncertain fields or `ActionType` values as certain.
- Label IOC-only logic as short-lived and provide a behavioral complement where feasible.
- Generated KQL remains untested until the existing validation pipeline accepts its syntax and an analyst validates it in the target environment.

### 8.11 Validation handoff

Adapt the validation, telemetry, evasion, false-positive, and handoff concepts from Feedly R2-06.

KQL is the primary local detection language. Sigma may be mentioned as a portability concept but is not required as the canonical output.

Each handoff must state:

- detection rationale;
- required telemetry and fields;
- known limitations and evasions;
- false-positive sources;
- tuning guidance;
- safe validation approach;
- expected telemetry;
- pass/fail criteria;
- deployment readiness status.

### 8.12 Reporting modules

Adapt the useful structures from Feedly R2-11, R4-07, and R4-08.

Provide separate outputs for:

- structured technical threat assessment;
- CTI incident SITREP;
- executive intelligence brief.

All reporting prompts must distinguish observed facts, source claims, analyst inference, confidence, limitations, and unanswered intelligence gaps.

## 9. Explicit exclusions from the native core

The following Feedly prompts are not first-class local modules in this implementation:

- tariff monitoring;
- phishing awareness newsletter;
- Splunk SPL conversion;
- MITRE ATLAS mapping;
- fraud-cyber assessment;
- BFSI-specific stakeholder material;
- generic stakeholder feedback synthesis;
- tabletop exercise generation;
- resilience assessment;
- red-team emulation planning;
- Sigma-first rule generation.

They remain accessible upstream and may be added later if a real repository use case appears.

## 10. Manifest

`prompts/manifest.json` is the registry for all native prompts.

Each entry must include:

- `id`;
- relative path;
- stage;
- upstream source ID;
- inputs;
- outputs;
- gates;
- allowed downstream modules.

The manifest must not contain prompt text. Its purpose is discovery, validation, documentation generation, and future tooling compatibility.

## 11. Documentation

`prompts/README.md` must explain:

- why this layer exists;
- how prompt modules differ from operational detections;
- how provenance and validation work;
- which Feedly modules were adapted;
- how to select the next module;
- that prompt output is analysis assistance, not ground truth.

`docs/CTI-PROMPT-ORCHESTRATION.md` must describe the end-to-end workflow and give at least three example routes:

1. threat report -> source assessment -> hunt lead -> feasibility -> hypothesis;
2. vulnerability exploitation report -> lead -> feasibility -> KQL -> validation;
3. incident intelligence -> normalization -> mapping -> SITREP.

The documentation must cross-link `HUNTING-METHODOLOGY.md` and `CTI-NORMALIZATION.md` as authoritative local doctrine.

## 12. Provenance and licensing

Every adapted prompt must retain:

- Feedly attribution;
- exact upstream prompt ID;
- exact upstream URL;
- a statement that the local version is adapted;
- the repository's own validation requirements.

The implementation must not imply that Feedly endorses the local adaptations.

No file should copy large upstream explanatory sections unnecessarily. Adapt the workflow and preserve attribution rather than creating a redundant mirror.

## 13. Error handling and uncertainty rules

Prompt instructions must define failure behavior rather than encourage plausible completion.

When required evidence is absent:

- write `Not stated in source`, `Unknown`, or equivalent explicit uncertainty;
- do not infer product presence from generic industry prevalence;
- do not fabricate ATT&CK mappings, IOCs, CVE facts, field names, telemetry coverage, actor names, campaign names, or validation results;
- do not convert an empty query result into evidence that activity did not occur;
- do not treat repeated secondary reporting as independent corroboration.

When output cannot meet a stage contract, the prompt should return the gap and stop rather than silently skip the requirement.

## 14. Public-safety boundary

The existing public repository boundary applies to every prompt and example.

Prompt examples must not include:

- customer names;
- internal hostnames;
- tenant IDs;
- credentials;
- proprietary detections;
- unpublished incident evidence;
- private infrastructure;
- operational data that cannot safely be public.

Prompts may describe the shape of sensitive inputs, but example data must be synthetic or sanitized.

## 15. Testing and CI

Add `tests/test_prompt_contracts.py`.

The tests must verify at least:

1. every manifest entry points to an existing prompt file;
2. every native prompt has valid YAML front matter;
3. every prompt has a unique stable `id`;
4. every prompt declares stage, source, adaptation, inputs, outputs, gates, and next-stage relationships;
5. every `next` ID resolves to a manifest entry;
6. every Feedly-derived prompt has an upstream URL and ID;
7. no prompt claims generated KQL is tested or production-ready by default;
8. detection-stage prompts mention telemetry requirements and validation;
9. hunt-stage prompts preserve the lead -> feasibility -> hypothesis separation;
10. public prompt files contain no obvious placeholders such as `TODO` or `TBD`.

The existing KQL parser and hunt semantic tests remain unchanged and authoritative for `.kql` artifacts.

The prompt-contract test should be added to the existing CI workflow rather than creating a parallel CI universe unless workflow isolation is required by the implementation.

## 16. Acceptance criteria

The integration is complete when:

- the curated prompt tree exists;
- every prompt has a valid contract and provenance metadata;
- `manifest.json` resolves every module and transition;
- orchestration documentation explains the workflow and examples;
- repository README links to the prompt layer without displacing the existing methodology links;
- prompt-contract tests pass;
- existing hunt semantic and KQL parser tests still pass;
- no excluded Feedly prompt has been copied into the native core without a documented reason;
- no prompt weakens the existing evidence-first, telemetry-first, provenance, or public-safety requirements.

## 17. Implementation boundary

This design is intentionally one implementation unit: a documentation-and-contract layer plus CI validation. It does not require a runtime service, CLI, database, web interface, or LLM client.

Future work may add a small local router or CLI that reads `manifest.json`, but that is explicitly outside this implementation and requires a separate design.
