from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
WORKFLOW = ROOT / ".github" / "workflows" / "hunt-contract.yml"
PROJECT = ROOT / "tools" / "kql-validate" / "KqlValidate.csproj"
PROGRAM = ROOT / "tools" / "kql-validate" / "Program.cs"


class KqlParserGateTests(unittest.TestCase):
    def test_validator_uses_pinned_official_kusto_language_parser(self) -> None:
        self.assertTrue(PROJECT.is_file(), "KQL validator project must exist")
        project = PROJECT.read_text(encoding="utf-8")
        self.assertIn('PackageReference Include="Microsoft.Azure.Kusto.Language" Version="12.4.1"', project)

    def test_validator_parses_each_kql_and_fails_on_syntax_diagnostics(self) -> None:
        self.assertTrue(PROGRAM.is_file(), "KQL validator program must exist")
        source = PROGRAM.read_text(encoding="utf-8")
        self.assertIn("KustoCode.Parse", source)
        self.assertIn("GetDiagnostics", source)
        self.assertIn('Directory.EnumerateFiles(huntsRoot, "*.kql", SearchOption.AllDirectories)', source)
        self.assertIn("return failed ? 1 : 0", source)

    def test_quality_gate_executes_validator(self) -> None:
        workflow = WORKFLOW.read_text(encoding="utf-8")
        self.assertIn("actions/setup-dotnet@", workflow)
        self.assertIn("dotnet run --project tools/kql-validate/KqlValidate.csproj -- hunts", workflow)


if __name__ == "__main__":
    unittest.main()
