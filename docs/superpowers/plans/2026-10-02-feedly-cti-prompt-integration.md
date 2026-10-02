# Feedly CTI Prompt Integration Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a curated, provenance-aware Feedly-derived CTI prompt layer that converts source reporting into telemetry-ready hunt and detection artifacts without weakening the repository's existing evidence-first contracts.

**Architecture:** Prompt modules live under `prompts/` and expose a small YAML front-matter contract mirrored by `prompts/manifest.json`. Python `unittest` contract tests validate provenance, stage transitions, safety rules, and manifest/file consistency; existing KQL semantic and Microsoft parser gates remain authoritative for `.kql` artifacts.

**Tech Stack:** Markdown, JSON, Python 3 standard library (`unittest`, `json`, `pathlib`, `re`), GitHub Actions, existing Microsoft Kusto.Language validator.

**Spec:** `docs/superpowers/specs/2026-10-02-feedly-cti-prompt-integration-design.md`

## Global Constraints

- Feedly-derived prompts are upstream reasoning modules; `docs/HUNTING-METHODOLOGY.md` and `docs/CTI-NORMALIZATION.md` remain authoritative local doctrine.
- Defender XDR / Sentinel and KQL are the first-class detection target.
- Do not add a runtime LLM dependency, CLI, service, database, or orchestration engine.
- Do not execute KQL against a tenant or claim generated KQL is tested or production-ready by default.
- Preserve source identity, upstream Feedly prompt ID, exact upstream URL, and an explicit local-adaptation marker for every adapted module.
- Unknown evidence, telemetry coverage, ATT&CK mappings, actor/campaign context, and validation results must remain explicitly unknown rather than inferred.
- Lead, feasibility, hypothesis, detection, and validation stages must remain distinct.
- Examples must be synthetic or sanitized and must not include customer names, internal hostnames, tenant IDs, credentials, private infrastructure, proprietary detections, or unpublished incident evidence.
- Use no new third-party Python package solely to parse prompt metadata; the validator supports only the repository's intentionally small front-matter subset.

## Review Focus

1. **Manifest drift:** a path, ID, stage, or `next` target changes in one place but not the other; tests must fail on unresolved paths, duplicate IDs, and unresolved downstream IDs.
2. **Malformed metadata:** front matter is missing, duplicated, or uses unsupported nesting; the validator must reject it rather than silently partially parse it.
3. **Stage collapse:** lead or feasibility prompts start generating KQL or pretending telemetry exists; stage-specific tests must pin the lead -> feasibility -> hypothesis separation.
4. **False validation claims:** detection prompts imply generated KQL is tested, deployed, or production-ready; detection-specific tests must require telemetry/validation language and reject those claims.
5. **Provenance laundering:** an adapted prompt lacks Feedly attribution, upstream ID, or exact URL; every manifest-backed prompt must fail closed when provenance metadata is incomplete.

---

### Task 1: Prompt Contract Validator and Empty Registry

**Files:**
- Create: `tests/test_prompt_contracts.py`
- Create: `prompts/manifest.json`

**Interfaces:**
- Consumes: repository root and prompt files registered in `prompts/manifest.json`.
- Produces: `load_manifest() -> list[dict[str, object]]`, `parse_front_matter(text: str) -> dict[str, object]`, and reusable assertion helpers inside `tests/test_prompt_contracts.py` for later tasks.

- [ ] **Step 1: Write failing validator unit tests**

Add tests using in-memory front-matter fixtures for: valid scalar/list/nested-source metadata, missing delimiters, duplicate keys, unsupported nesting, duplicate IDs, and unresolved `next` IDs. Assert malformed contracts raise `ValueError` with a stable reason string.

- [ ] **Step 2: Run the focused tests and confirm failure**

Run: `python -m unittest tests.test_prompt_contracts -v`

Expected: FAIL because the parser/helpers and registry do not exist yet.

- [ ] **Step 3: Implement the minimal stdlib-only contract parser and registry loader**

In `tests/test_prompt_contracts.py`, implement only the YAML subset used by this repository: top-level scalars, top-level lists, and the two-level `source` mapping. Reject duplicate keys, unsupported deeper nesting, and malformed list items. Create `prompts/manifest.json` as `{"prompts": []}`.

- [ ] **Step 4: Run the focused tests**

Run: `python -m unittest tests.test_prompt_contracts -v`

Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add tests/test_prompt_contracts.py prompts/manifest.json
git commit -m "test: add prompt contract validator"
```

### Task 2: Intake and Enrichment Prompt Modules

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
- Consumes: source material and provenance context.
- Produces module IDs: `source-assessment`, `threat-data-triage`, `multi-feed-consolidation`, `ioc-extract-enrich`, `attack-mapping`, `diamond-model`.
- Primary upstream mappings: R2-02, R4-01, R4-02, R3-01, R3-02, R3-03 respectively. `attack-mapping` may cite R1-05 as supplementary source context; `diamond-model` may cite R1-01 as supplementary source context.

- [ ] **Step 1: Add failing manifest/provenance tests for the six module IDs**

Assert all six IDs are registered, each path exists, each front matter contract matches the manifest, each Feedly-derived module has `source.provider: Feedly`, an exact `source.upstream_id`, an HTTPS GitHub upstream URL, and `adaptation: ger1e-threat-hunting-lab`.

- [ ] **Step 2: Run the focused tests and confirm failure**

Run: `python -m unittest tests.test_prompt_contracts -v`

Expected: FAIL on missing module registrations/files.

- [ ] **Step 3: Create the six adapted prompt files and manifest entries**

Use the spec-defined responsibilities. Require explicit uncertainty, source citations, evidence/inference separation, and no fabricated ATT&CK/IOC/context values. `threat-data-triage` and `multi-feed-consolidation` must prohibit KQL generation. `ioc-extract-enrich` must stay compatible with `cti-schema.json` and preserve URL paths/context. `attack-mapping` must flag ambiguous mappings. `diamond-model` must separate observed relationships from inference.

- [ ] **Step 4: Run contract and existing repository tests**

Run: `python -m unittest discover -s tests -p 'test_*.py' -v`

Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add prompts/intake prompts/enrichment prompts/manifest.json tests/test_prompt_contracts.py
git commit -m "feat: add CTI intake and enrichment prompts"
```

### Task 3: Hunting Chain Modules and Stage-Separation Gates

**Files:**
- Create: `prompts/hunting/hunt-lead-extraction.md`
- Create: `prompts/hunting/hunt-feasibility.md`
- Create: `prompts/hunting/hunt-hypothesis.md`
- Create: `prompts/hunting/hunt-package.md`
- Modify: `prompts/manifest.json`
- Modify: `tests/test_prompt_contracts.py`

**Interfaces:**
- Consumes: normalized CTI, prioritized leads, environment/stack facts, and telemetry requirements from earlier modules.
- Produces module IDs: `hunt-lead-extraction`, `hunt-feasibility`, `hunt-hypothesis`, `hunt-package`.
- Upstream mappings: R2-07, R2-08, R1-04, R3-07 respectively.
- Required route: `hunt-lead-extraction -> hunt-feasibility -> hunt-hypothesis`; `hunt-package` packages multiple source-supported hypotheses but does not bypass feasibility.

- [ ] **Step 1: Add failing hunting-chain tests**

Assert all four modules exist, the required `next` transitions resolve, lead prompt text explicitly forbids queries/detection rules/full hypotheses, feasibility marks missing stack coverage as unknown, and hypothesis text contains the repository's falsifiable `If ... then ... X ... Y ... Z` contract plus scope, time horizon, benign collisions, falsifiers, and required telemetry.

- [ ] **Step 2: Run focused tests and confirm failure**

Run: `python -m unittest tests.test_prompt_contracts -v`

Expected: FAIL on missing hunting modules and transitions.

- [ ] **Step 3: Create hunting prompts and update manifest**

Keep lead, feasibility, hypothesis, and package outputs distinct. `hunt-package` may aggregate validated hypotheses but must reference feasibility outcomes and must not infer unavailable telemetry or claim execution results.

- [ ] **Step 4: Run full Python tests**

Run: `python -m unittest discover -s tests -p 'test_*.py' -v`

Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add prompts/hunting prompts/manifest.json tests/test_prompt_contracts.py
git commit -m "feat: add threat hunting prompt chain"
```

### Task 4: Sentinel Detection and Validation Modules

**Files:**
- Create: `prompts/detection/sentinel-kql-opportunities.md`
- Create: `prompts/detection/validation-handoff.md`
- Modify: `prompts/manifest.json`
- Modify: `tests/test_prompt_contracts.py`

**Interfaces:**
- Consumes: feasible source-supported behavior/hypotheses and stated telemetry.
- Produces module IDs: `sentinel-kql-opportunities`, `validation-handoff`.
- Upstream mappings: R2-04 and R2-06 respectively.
- `sentinel-kql-opportunities` produces candidate KQL only; `validation-handoff` produces rationale, telemetry requirements, limitations/evasions, FP/tuning guidance, validation steps, expected telemetry, pass/fail criteria, and readiness status.

- [ ] **Step 1: Add failing detection-safety tests**

Assert detection modules mention Defender XDR/Sentinel, exact telemetry requirements, time-bounded joins, schema uncertainty, false positives/tuning, analyst/environment validation, and untested status. Reject phrases that claim generated KQL is `production-ready`, `validated`, `tested`, or `deployed` by default.

- [ ] **Step 2: Run focused tests and confirm failure**

Run: `python -m unittest tests.test_prompt_contracts -v`

Expected: FAIL on missing detection modules.

- [ ] **Step 3: Create detection and validation prompts and update manifest**

Use KQL as the canonical local output. Preserve behavior-first telemetry matching, early filtering/aggregation guidance, time-bounded joins, uncertainty labels for unverified fields/`ActionType` values, and short-lived labeling for IOC-only logic.

- [ ] **Step 4: Run Python tests and the existing Microsoft KQL parser gate**

Run:

```bash
python -m unittest discover -s tests -p 'test_*.py' -v
dotnet run --project tools/kql-validate/KqlValidate.csproj -- hunts
```

Expected: all tests PASS; KQL validator reports no syntax regressions in existing hunts.

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
- Consumes: evidence, source claims, analyst inference, confidence, limitations, and unresolved intelligence gaps from prior modules.
- Produces module IDs: `structured-threat-assessment`, `incident-sitrep`, `executive-brief`.
- Upstream mappings: R2-11, R4-07, R4-08 respectively.

- [ ] **Step 1: Add failing reporting/documentation tests**

Assert the three reporting modules are registered and explicitly separate observed facts, source claims, analyst inference, confidence, limitations, and intelligence gaps. Assert `prompts/README.md` links the Feedly source library and states prompt output is analysis assistance rather than ground truth. Assert `docs/CTI-PROMPT-ORCHESTRATION.md` links both authoritative local doctrine files and contains the three routes required by the spec.

- [ ] **Step 2: Run focused tests and confirm failure**

Run: `python -m unittest tests.test_prompt_contracts -v`

Expected: FAIL on missing reporting files/docs.

- [ ] **Step 3: Create reporting modules and documentation**

Document module selection and stage transitions without introducing an execution engine. Include the three exact example routes from the spec and explain that manifest transitions are discovery/documentation contracts, not automatic execution.

- [ ] **Step 4: Run full Python tests**

Run: `python -m unittest discover -s tests -p 'test_*.py' -v`

Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add prompts/reporting prompts/README.md docs/CTI-PROMPT-ORCHESTRATION.md prompts/manifest.json tests/test_prompt_contracts.py
git commit -m "docs: add CTI prompt reporting and orchestration"
```

### Task 6: Repository Surface, CI Integration, and Final Acceptance Gate

**Files:**
- Modify: `README.md`
- Modify: `.github/workflows/hunt-contract.yml`
- Modify: `tests/test_prompt_contracts.py`

**Interfaces:**
- Consumes: all 15 prompt modules and the final manifest from Tasks 2-5.
- Produces: top-level discoverability and CI enforcement on prompt/doc changes.

- [ ] **Step 1: Add final failing acceptance tests**

Assert the manifest contains exactly these 15 unique IDs: `source-assessment`, `threat-data-triage`, `multi-feed-consolidation`, `ioc-extract-enrich`, `attack-mapping`, `diamond-model`, `hunt-lead-extraction`, `hunt-feasibility`, `hunt-hypothesis`, `hunt-package`, `sentinel-kql-opportunities`, `validation-handoff`, `structured-threat-assessment`, `incident-sitrep`, `executive-brief`. Assert no public prompt contains `TODO` or `TBD`, every `next` target resolves, every Feedly-derived prompt has complete provenance, and excluded native-core topics are absent from `prompts/manifest.json`.

- [ ] **Step 2: Run focused tests and confirm failure**

Run: `python -m unittest tests.test_prompt_contracts -v`

Expected: FAIL until README/CI surface and final acceptance assertions are satisfied.

- [ ] **Step 3: Update top-level README and quality-gates workflow**

Add a compact `CTI prompt layer` link to `prompts/README.md` and `docs/CTI-PROMPT-ORCHESTRATION.md` without displacing the existing methodology/normalization links. Add `prompts/**/*.md` and `prompts/manifest.json` to push path filters. Ensure the existing `python -m unittest discover -s tests -p 'test_*.py' -v` step remains the single Python test entry point.

- [ ] **Step 4: Run complete local verification**

Run:

```bash
python -m json.tool cti-schema.json >/dev/null
python -m json.tool prompts/manifest.json >/dev/null
python -m unittest discover -s tests -p 'test_*.py' -v
dotnet run --project tools/kql-validate/KqlValidate.csproj -- hunts
```

Expected: all commands exit 0; all Python tests PASS; existing hunts pass Microsoft KQL syntax validation.

- [ ] **Step 5: Review repository diff for scope and safety**

Run: `git diff main...HEAD -- README.md .github/workflows/hunt-contract.yml prompts docs/CTI-PROMPT-ORCHESTRATION.md tests/test_prompt_contracts.py`

Expected: only the approved prompt-layer integration, documentation, tests, and CI wiring are present; no runtime service, CLI, tenant data, or excluded Feedly modules appear.

- [ ] **Step 6: Commit**

```bash
git add README.md .github/workflows/hunt-contract.yml tests/test_prompt_contracts.py
git commit -m "ci: enforce CTI prompt contracts"
```

- [ ] **Step 7: Final verification from clean branch state**

Run: `git status --short`

Expected: no uncommitted implementation files.
