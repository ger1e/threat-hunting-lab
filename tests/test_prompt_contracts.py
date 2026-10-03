from pathlib import Path
import json
import unittest

ROOT = Path(__file__).resolve().parents[1]


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
    def test_empty_registry_is_valid(self) -> None:
        self.assertEqual(load_manifest(), [])

    def test_duplicate_ids_are_rejected_by_contract(self) -> None:
        entries = [{"id": "x"}, {"id": "x"}]
        ids = [entry["id"] for entry in entries]
        self.assertNotEqual(len(ids), len(set(ids)))

    def test_unresolved_next_ids_are_detectable(self) -> None:
        entries = [{"id": "x", "next": ["missing"]}]
        ids = {entry["id"] for entry in entries}
        unresolved = [target for entry in entries for target in entry["next"] if target not in ids]
        self.assertEqual(unresolved, ["missing"])


if __name__ == "__main__":
    unittest.main()
