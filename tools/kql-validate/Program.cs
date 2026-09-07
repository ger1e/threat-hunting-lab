using System.Text;
using Kusto.Language;

if (args.Length != 1)
{
    Console.Error.WriteLine("usage: KqlValidate <hunts-directory>");
    return 2;
}

var huntsRoot = Path.GetFullPath(args[0]);
if (!Directory.Exists(huntsRoot))
{
    Console.Error.WriteLine($"Hunt directory not found: {huntsRoot}");
    return 2;
}

var files = Directory.EnumerateFiles(huntsRoot, "*.kql", SearchOption.AllDirectories)
    .OrderBy(path => path, StringComparer.Ordinal)
    .ToArray();

if (files.Length == 0)
{
    Console.Error.WriteLine("No KQL hunts found.");
    return 2;
}

var failed = false;
foreach (var file in files)
{
    var query = File.ReadAllText(file, Encoding.UTF8);
    var diagnostics = KustoCode.Parse(query)
        .GetDiagnostics()
        .Where(diagnostic => string.Equals(
            diagnostic.Severity,
            DiagnosticSeverity.Error,
            StringComparison.Ordinal))
        .ToArray();

    var relative = Path.GetRelativePath(Directory.GetCurrentDirectory(), file)
        .Replace(Path.DirectorySeparatorChar, '/');

    if (diagnostics.Length == 0)
    {
        Console.WriteLine($"KQL syntax: PASS {relative}");
        continue;
    }

    failed = true;
    foreach (var diagnostic in diagnostics)
    {
        Console.Error.WriteLine(
            $"::error file={relative}::{Escape(diagnostic.Code)}: {Escape(diagnostic.Message)}");
    }
}

return failed ? 1 : 0;

static string Escape(string value) => value
    .Replace("%", "%25", StringComparison.Ordinal)
    .Replace("\r", "%0D", StringComparison.Ordinal)
    .Replace("\n", "%0A", StringComparison.Ordinal);
