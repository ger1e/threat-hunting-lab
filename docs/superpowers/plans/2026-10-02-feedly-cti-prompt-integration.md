# Feedly CTI Prompt Integration Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a curated, provenance-aware Feedly-derived CTI prompt layer that converts source reporting into telemetry-ready hunt and detection artifacts without weakening the repository's existing evidence-first contracts.

**Architecture:** Prompt modules live under `prompts/` and expose a small YAML front-matter contract mirrored by `prompts/manifest.json`. Python `unittest` contract tests validate provenance, stage transitions, safety rules, and manifest/file consistency; existing KQL semantic and Microsoft parser gates remain authoritative for `.kql` artifacts.

**Tech Stack:** Markdown, JSON, Python 3 standard library (`unittest`, `json`, `pathlib`, `re`), GitHub Actions, existing Microsoft Kusto.Language validator.

**Spec:** `docs/superpowers/specs/2026-10-02-feedly-cti-prompt-integration-design.md`

## Global Constraints

- `docs/HUNTING-METHODOLOGY.md` and `docs/CTI-NORMALIZATION.md` remain authoritative local doctrine.
- Defender XDR / Sentinel and KQL remain the first-class detection target.
- Do not add a runtime LLM dependency, CLI, service, database, or orchestration engine.
- Do not execute KQL against a tenant or claim generated KQL is tested or production-ready by default.
- Every adapted module retains Feedly attribution, exact upstream prompt ID, exact upstream URL, and `adaptation: ger1e-threat-hunting-lab`.
- Unknown evidence, telemetry coverage, ATT&CK mappings, actor/campaign context, and validation results remain explicitly unknown.
- Lead, feasibility, hypothesis, detection, and validation stages remain distinct.
- Examples are synthetic or sanitized and contain no customer names, internal hostnames, tenant IDs, credentials, private infrastructure, proprietary detections, or unpublished incident evidence.
- Add no third-party Python package solely to parse prompt metadata; the validator supports only the repository's deliberately small front-matter subset.

## Review Focus

1. **Manifest drift:** missing files, duplicate IDs, mismatched stages, or unresolved `next` targets must fail tests.
2. **Malformed metadata:** missing delimiters, duplicate keys, or unsupported nesting must be rejected rather than partially parsed.
3. **Stage collapse:** lead/feasibility prompts must not generate KQL or assume telemetry exists.
4. **False validation claims:** detection prompts must not imply generated KQL is tested, deployed, validated, or production-ready by default.
5. **Provenance laundering:** any adapted module missing Feedly attribution, upstream ID, or exact HTTPS URL must fail closed.

---

### Task 1: Prompt Contract Validator and Registry Skeleton

**Files:**
- Create: `tests/test_prompt_contracts.py`
- Create: `prompts/manifest.json`

**Interfaces:**
- Consumes: repository root and files registered in `prompts/manifest.json`.
- Produces: `load_manifest() -> list[dict[str, object]]`, `parse_front_matter(text: str) -> dict[str, object]`, and reusable contract assertions.
- Manifest entry keys are exactly: `id`, `path`, `stage`, `upstream_id`, `inputs`, `outputs`, `gates`, `next`.

- [ ] **Step 1: Write failing validator tests**

Add in-memory fixtures covering valid scalar/list/source metadata, missing delimiters, duplicate keys, unsupported deeper nesting, duplicate manifest IDs, and unresolved `next` IDs. Assert malformed contracts raise `ValueError` with stable reason text.

- [ ] **Step 2: Run the focused tests and verify failure**

Run: `python -m unittest tests.test_prompt_contracts -v`

Expected: FAIL because parser/helpers and registry are absent.

- [ ] **Step 3: Implement the minimal stdlib-only parser and empty registry**

Implement only top-level scalars, top-level lists, and a two-level `source` mapping. Reject everything deeper or ambiguous. Create `prompts/manifest.json` as `{"prompts": []}`.

- [ ] **Step 4: Run the focused tests**

Run: `python -m unittest tests.test_prompt_contracts -v`

Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add tests/test_prompt_contracts.py prompts/manifest.json
git commit -m "test: add prompt contract validator"
```

### Task 2: Intake and Enrichment Modules

**Files:**
- Create: `prompts/intake/source-assessment.md`
- Create: `prompts/intake/threat-data-triage.md`
- Create: `prompts/intake/multi-feed-consolidation.md`
- Create: `prompts/enrichment/ioc-extract-enrich.md`
- Create: `prompts/enrichment/attack-mapping.md`
- Create: `prompts/enrichment/diamond-model.md`
- Modify: `prompts/manifest.json`
- Modify: `tests/test_prompt_contracts.py`

**Interfaces:**
- Produces IDs: `source-assessment`, `threat-data-triage`, `multi-feed-consolidation`, `ioc-extract-enrich`, `attack-mapping`, `diamond-model`.
- Primary upstream IDs: R2-02, R4-01, R4-02, R3-01, R3-02, R3-03. `attack-mapping` may cite R1-05 and `diamond-model` may cite R1-01 as supplementary source context.

- [ ] **Step 1: Add failing module/provenance tests**

Assert all six IDs are registered; paths exist; front matter matches manifest; every module has `source.provider: Feedly`, exact upstream ID, HTTPS GitHub upstream URL, `adaptation: ger1e-threat-hunting-lab`, `consumes`, `produces`, `requires`, `gates`, and `next`.

- [ ] **Step 2: Run tests and verify failure**

Run: `python -m unittest tests.test_prompt_contracts -v`

Expected: FAIL on missing modules.

- [ ] **Step 3: Create the six prompts and manifest entries**

Enforce source citations, explicit uncertainty, evidence/inference separation, and no fabricated ATT&CK/IOC/context values. `threat-data-triage` and `multi-feed-consolidation` prohibit KQL. `ioc-extract-enrich` preserves URL paths/context and remains compatible with `cti-schema.json`. `attack-mapping` marks ambiguous mappings. `diamond-model` separates observed relationships from inference.

- [ ] **Step 4: Run all Python tests**

Run: `python -m unittest discover -s tests -p 'test_*.py' -v`

Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add prompts/intake prompts/enrichment prompts/manifest.json tests/test_prompt_contracts.py
git commit -m "feat: add CTI intake and enrichment prompts"
```

### Task 3: Hunting Chain and Stage Separation

**Files:**
- Create: `prompts/hunting/hunt-lead-extraction.md`
- Create: `prompts/hunting/hunt-feasibility.md`
- Create: `prompts/hunting/hunt-hypothesis.md`
- Create: `prompts/hunting/hunt-package.md`
- Modify: `prompts/manifest.json`
- Modify: `tests/test_prompt_contracts.py`

**Interfaces:**
- Produces IDs: `hunt-lead-extraction`, `hunt-feasibility`, `hunt-hypothesis`, `hunt-package`.
- Upstream IDs: R2-07, R2-08, R1-04, R3-07.
- Required route: `hunt-lead-extraction -> hunt-feasibility -> hunt-hypothesis`. `hunt-package` aggregates source-supported hypotheses only after feasibility.

- [ ] **Step 1: Add failing hunting-chain tests**

Assert required transitions resolve; lead text explicitly forbids queries, detection rules, and full hypotheses; feasibility marks absent stack coverage as unknown; hypothesis text contains the repository falsifiable contract plus scope, time horizon, benign collisions, falsifiers, and required telemetry; `hunt-package` cannot bypass feasibility.

- [ ] **Step 2: Run tests and verify failure**

Run: `python -m unittest tests.test_prompt_contracts -v`

Expected: FAIL on missing hunting modules/transitions.

- [ ] **Step 3: Create hunting prompts and manifest entries**

Keep lead, feasibility, hypothesis, and package outputs distinct. Never infer unavailable telemetry or claim execution results.

- [ ] **Step 4: Run all Python tests**

Run: `python -m unittest discover -s tests -p 'test_*.py' -v`

Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add prompts/hunting prompts/manifest.json tests/test_prompt_contracts.py
git commit -m "feat: add threat hunting prompt chain"
```

### Task 4: Sentinel Detection and Validation

**Files:**
- Create: `prompts/detection/sentinel-kql-opportunities.md`
- Create: `prompts/detection/validation-handoff.md`
- Modify: `prompts/manifest.json`
- Modify: `tests/test_prompt_contracts.py`

**Interfaces:**
- Produces IDs: `sentinel-kql-opportunities`, `validation-handoff`.
- Upstream IDs: R2-04, R2-06.
- `sentinel-kql-opportunities` produces candidate KQL only. `validation-handoff` produces rationale, telemetry requirements, limitations/evasions, FP/tuning guidance, validation steps, expected telemetry, pass/fail criteria, and readiness status.

- [ ] **Step 1: Add failing detection-safety tests**

Assert the modules require Defender XDR/Sentinel telemetry, time-bounded joins, schema uncertainty handling, false-positive/tuning guidance, analyst/environment validation, and untested status. Reject default claims containing `production-ready`, `validated`, `tested`, or `deployed` as completed states.

- [ ] **Step 2: Run tests and verify failure**

Run: `python -m unittest tests.test_prompt_contracts -v`

Expected: FAIL on missing detection modules.

- [ ] **Step 3: Create detection/validation prompts and manifest entries**

Use KQL as canonical local output. Require behavior-first telemetry mapping, early filtering/aggregation, time-bounded joins, explicit uncertainty for unverified fields/`ActionType` values, and short-lived labeling for IOC-only logic.

- [ ] **Step 4: Run Python tests and existing KQL syntax validation**

Run:

```bash
python -m unittest discover -s tests -p 'test_*.py' -v
dotnet run --project tools/kql-validate/KqlValidate.csproj -- hunts
```

Expected: PASS with no existing KQL regressions.

- [ ] **Step 5: Commit**

```bash
git add prompts/detection prompts/manifest.json tests/test_prompt_contracts.py
git commit -m "feat: add Sentinel detection prompt modules"
```

### Task 5: Reporting Modules and Orchestration Documentation

**Files:**
- Create: `prompts/reporting/structured-threat-assessment.md`
- Create: `prompts/reporting/incident-sitrep.md`
- Create: `prompts/reporting/executive-brief.md`
- Create: `prompts/README.md`
- Create: `docs/CTI-PROMPT-ORCHESTRATION.md`
- Modify: `prompts/manifest.json`
- Modify: `tests/test_prompt_contracts.py`

**Interfaces:**
- Produces IDs: `structured-threat-assessment`, `incident-sitrep`, `executive-brief`.
- Upstream IDs: R2-11, R4-07, R4-08.

- [ ] **Step 1: Add failing reporting/documentation tests**

Assert reporting modules separate observed facts, source claims, analyst inference, confidence, limitations, and intelligence gaps. Assert `prompts/README.md` links the Feedly source library and says prompt output is analysis assistance, not ground truth. Assert `docs/CTI-PROMPT-ORCHESTRATION.md` links both authoritative local doctrine files and includes the three spec-required example routes.

- [ ] **Step 2: Run tests and verify failure**

Run: `python -m unittest tests.test_prompt_contracts -v`

Expected: FAIL on missing reporting files/docs.

- [ ] **Step 3: Create reporting modules and documentation**

Document transitions as discovery/documentation contracts, not automatic execution. Include the three exact routes from the spec.

- [ ] **Step 4: Run all Python tests**

Run: `python -m unittest discover -s tests -p 'test_*.py' -v`

Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add prompts/reporting prompts/README.md docs/CTI-PROMPT-ORCHESTRATION.md prompts/manifest.json tests/test_prompt_contracts.py
git commit -m "docs: add CTI prompt reporting and orchestration"
```

### Task 6: Repository Surface, CI Wiring, and Final Acceptance

**Files:**
- Modify: `README.md`
- Modify: `.github/workflows/hunt-contract.yml`
- Modify: `tests/test_prompt_contracts.py`

**Interfaces:**
- Consumes: all 15 prompt modules and final manifest.
- Produces: top-level discoverability and CI enforcement for prompt/doc changes.

- [ ] **Step 1: Add final failing acceptance tests**

Assert exactly these 15 IDs exist: `source-assessment`, `threat-data-triage`, `multi-feed-consolidation`, `ioc-extract-enrich`, `attack-mapping`, `diamond-model`, `hunt-lead-extraction`, `hunt-feasibility`, `hunt-hypothesis`, `hunt-package`, `sentinel-kql-opportunities`, `validation-handoff`, `structured-threat-assessment`, `incident-sitrep`, `executive-brief`. Also assert: no prompt contains `TODO` or `TBD`; every `next` resolves; every Feedly-derived prompt has complete provenance; excluded native-core topics are absent from the manifest; top-level `README.md` links both `prompts/README.md` and `docs/CTI-PROMPT-ORCHESTRATION.md`; `.github/workflows/hunt-contract.yml` includes path filters for `prompts/**/*.md` and `prompts/manifest.json`.

- [ ] **Step 2: Run focused tests and verify failure**

Run: `python -m unittest tests.test_prompt_contracts -v`

Expected: FAIL specifically on missing README/CI wiring before Step 3.

- [ ] **Step 3: Update top-level README and quality-gates workflow**

Add compact prompt-layer/orchestration links without displacing methodology/normalization links. Add `prompts/**/*.md` and `prompts/manifest.json` to push path filters. Keep `python -m unittest discover -s tests -p 'test_*.py' -v` as the single Python test entry point.

- [ ] **Step 4: Run complete local verification**

Run:

```bash
python -m json.tool cti-schema.json >/dev/null
python -m json.tool prompts/manifest.json >/dev/null
python -m unittest discover -s tests -p 'test_*.py' -v
dotnet run --project tools/kql-validate/KqlValidate.csproj -- hunts
```

Expected: all commands exit 0 and all tests pass.

- [ ] **Step 5: Review the scoped diff**

Run: `git diff main...HEAD -- README.md .github/workflows/hunt-contract.yml prompts docs/CTI-PROMPT-ORCHESTRATION.md tests/test_prompt_contracts.py`

Expected: only approved prompt-layer files, documentation, tests, and CI wiring; no runtime service, CLI, tenant data, or excluded Feedly modules.

- [ ] **Step 6: Commit**

```bash
git add README.md .github/workflows/hunt-contract.yml tests/test_prompt_contracts.py
git commit -m "ci: enforce CTI prompt contracts"
```

- [ ] **Step 7: Verify clean implementation state**

Run: `git status --short`

Expected: no uncommitted implementation files.
