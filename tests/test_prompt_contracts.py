from pathlib import Path
import json
import unittest

ROOT = Path(__file__).resolve().parents[1]
EXPECTED_IDS = {
    "source-assessment", "threat-data-triage", "multi-feed-consolidation",
    "ioc-extract-enrich", "attack-mapping", "diamond-model",
    "hunt-lead-extraction", "hunt-feasibility", "hunt-hypothesis", "hunt-package",
    "sentinel-kql-opportunities", "validation-handoff",
    "structured-threat-assessment", "incident-sitrep", "executive-brief",
}


def load_manifest() -> list[dict[str, object]]:
    data = json.loads((ROOT / "prompts" / "manifest.json").read_text(encoding="utf-8"))
    entries = data.get("prompts")
    if not isinstance(entries, list):
        raise ValueError("manifest prompts must be a list")
    ids = [entry.get("id") for entry in entries]
    if len(ids) != len(set(ids)):
        raise ValueError("duplicate id")
    known = set(ids)
    for entry in entries:
        for target in entry.get("next", []):
            if target not in known:
                raise ValueError(f"unresolved next id: {target}")
    return entries


def parse_front_matter(text: str) -> dict[str, object]:
    lines = text.splitlines()
    if len(lines) < 3 or lines[0] != "---" or "---" not in lines[1:]:
        raise ValueError("front matter delimiters missing")
    end = lines[1:].index("---") + 1
    result: dict[str, object] = {}
    current_key: str | None = None
    current_map: dict[str, str] | None = None
    for raw in lines[1:end]:
        if not raw.strip():
            continue
        indent = len(raw) - len(raw.lstrip(" "))
        line = raw.strip()
        if indent >= 4:
            raise ValueError("unsupported nesting")
        if indent == 2:
            if line.startswith("- "):
                if current_key is None or not isinstance(result.get(current_key), list):
                    raise ValueError("malformed list item")
                result[current_key].append(line[2:].strip())
                continue
            if current_map is None or ":" not in line:
                raise ValueError("unsupported nesting")
            key, value = [part.strip() for part in line.split(":", 1)]
            if not value or key in current_map:
                raise ValueError("duplicate key" if key in current_map else "unsupported nesting")
            current_map[key] = value
            continue
        if indent != 0 or ":" not in line:
            raise ValueError("unsupported nesting")
        key, value = [part.strip() for part in line.split(":", 1)]
        if key in result:
            raise ValueError("duplicate key")
        current_key = key
        current_map = None
        if value:
            result[key] = value
        elif key == "source":
            current_map = {}
            result[key] = current_map
        else:
            result[key] = []
    return result


class PromptContractParserTests(unittest.TestCase):
    def test_parses_supported_contract_shape(self) -> None:
        text = """---
id: source-assessment
stage: intake
source:
  provider: Feedly
  upstream_id: R2-02
  url: https://example.invalid/source
consumes:
  - source_material
next:
  - threat-data-triage
---
body
"""
        data = parse_front_matter(text)
        self.assertEqual(data["id"], "source-assessment")
        self.assertEqual(data["source"]["provider"], "Feedly")
        self.assertEqual(data["consumes"], ["source_material"])

    def test_rejects_missing_delimiters(self) -> None:
        with self.assertRaisesRegex(ValueError, "front matter delimiters"):
            parse_front_matter("id: broken")

    def test_rejects_duplicate_keys(self) -> None:
        with self.assertRaisesRegex(ValueError, "duplicate key"):
            parse_front_matter("---\nid: one\nid: two\n---\n")

    def test_rejects_unsupported_nesting(self) -> None:
        with self.assertRaisesRegex(ValueError, "unsupported nesting"):
            parse_front_matter("---\nsource:\n  nested:\n    value: no\n---\n")


class PromptRegistryTests(unittest.TestCase):
    def test_manifest_has_exact_curated_module_set(self) -> None:
        entries = load_manifest()
        self.assertEqual({entry["id"] for entry in entries}, EXPECTED_IDS)

    def test_manifest_files_and_front_matter_match(self) -> None:
        for entry in load_manifest():
            path = ROOT / str(entry["path"])
            self.assertTrue(path.is_file(), entry["path"])
            contract = parse_front_matter(path.read_text(encoding="utf-8"))
            self.assertEqual(contract["id"], entry["id"])
            self.assertEqual(contract["stage"], entry["stage"])
            self.assertEqual(contract["source"]["provider"], "Feedly")
            self.assertEqual(contract["source"]["upstream_id"], entry["upstream_id"])
            self.assertTrue(contract["source"]["url"].startswith("https://github.com/feedly/skills/"))
            self.assertEqual(contract["adaptation"], "ger1e-threat-hunting-lab")
            for key in ("consumes", "produces", "requires", "gates", "next"):
                self.assertIn(key, contract)

    def test_public_prompts_have_no_placeholders(self) -> None:
        for entry in load_manifest():
            text = (ROOT / str(entry["path"])).read_text(encoding="utf-8")
            self.assertNotIn("TODO", text)
            self.assertNotIn("TBD", text)

    def test_hunting_stage_separation_is_explicit(self) -> None:
        lead = (ROOT / "prompts/hunting/hunt-lead-extraction.md").read_text(encoding="utf-8")
        feasibility = (ROOT / "prompts/hunting/hunt-feasibility.md").read_text(encoding="utf-8")
        hypothesis = (ROOT / "prompts/hunting/hunt-hypothesis.md").read_text(encoding="utf-8")
        self.assertIn("Do not generate KQL", lead)
        self.assertIn("never invent available telemetry", feasibility)
        for phrase in ("If the suspected behavior is occurring", "scope", "time horizon", "falsifiers", "benign collisions", "required telemetry"):
            self.assertIn(phrase, hypothesis)

    def test_detection_prompts_require_validation_and_uncertainty(self) -> None:
        kql = (ROOT / "prompts/detection/sentinel-kql-opportunities.md").read_text(encoding="utf-8")
        handoff = (ROOT / "prompts/detection/validation-handoff.md").read_text(encoding="utf-8")
        for phrase in ("Defender XDR", "Sentinel", "Time-bound both sides of every join", "schema", "false-positive", "tuning", "untested by default"):
            self.assertIn(phrase, kql)
        for phrase in ("required telemetry", "limitations", "evasions", "pass/fail", "readiness"):
            self.assertIn(phrase, handoff)

    def test_reporting_and_orchestration_contracts(self) -> None:
        for name in ("structured-threat-assessment.md", "incident-sitrep.md", "executive-brief.md"):
            text = (ROOT / "prompts/reporting" / name).read_text(encoding="utf-8")
            for phrase in ("observed facts", "source claims", "analyst inference", "confidence", "limitations", "intelligence gaps"):
                self.assertIn(phrase, text)
        prompt_readme = (ROOT / "prompts/README.md").read_text(encoding="utf-8")
        self.assertIn("https://github.com/feedly/skills/tree/main/prompts/feedly-complete-cti-prompt-library", prompt_readme)
        self.assertIn("analysis assistance, not ground truth", prompt_readme)
        orchestration = (ROOT / "docs/CTI-PROMPT-ORCHESTRATION.md").read_text(encoding="utf-8")
        self.assertIn("HUNTING-METHODOLOGY.md", orchestration)
        self.assertIn("CTI-NORMALIZATION.md", orchestration)
        self.assertEqual(orchestration.count("## Route "), 3)

    def test_repository_surface_and_ci_are_wired(self) -> None:
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        workflow = (ROOT / ".github/workflows/hunt-contract.yml").read_text(encoding="utf-8")
        self.assertIn("prompts/README.md", readme)
        self.assertIn("docs/CTI-PROMPT-ORCHESTRATION.md", readme)
        self.assertIn("prompts/**/*.md", workflow)
        self.assertIn("prompts/manifest.json", workflow)
        self.assertIn("python -m unittest discover -s tests -p 'test_*.py' -v", workflow)


if __name__ == "__main__":
    unittest.main()
