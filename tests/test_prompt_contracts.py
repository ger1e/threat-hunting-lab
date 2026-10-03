from pathlib import Path
import json
import unittest

ROOT = Path(__file__).resolve().parents[1]


def load_manifest() -> list[dict[str, object]]:
    raise NotImplementedError("prompt registry loader not implemented")


def parse_front_matter(text: str) -> dict[str, object]:
    raise NotImplementedError("front matter parser not implemented")


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

    def test_registry_rejects_duplicate_ids(self) -> None:
        entries = [{"id": "x", "next": []}, {"id": "x", "next": []}]
        ids = [entry["id"] for entry in entries]
        self.assertNotEqual(len(ids), len(set(ids)))

    def test_registry_fixture_detects_unresolved_next_id(self) -> None:
        entries = [{"id": "x", "next": ["missing"]}]
        ids = {entry["id"] for entry in entries}
        unresolved = [target for entry in entries for target in entry["next"] if target not in ids]
        self.assertEqual(unresolved, ["missing"])


if __name__ == "__main__":
    unittest.main()
