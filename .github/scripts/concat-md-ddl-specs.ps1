param(
    [string]$SpecDir = "md-ddl-specification",
    [string]$OutputFileName = "MD-DDL-Complete.md"
)

$repoRoot = (Resolve-Path (Join-Path $PSScriptRoot "..\..")).Path
$specPath = Join-Path $repoRoot $SpecDir
$outputPath = Join-Path $specPath $OutputFileName

# Deterministic section order for MD-DDL spec generation.
$sectionFiles = @(
    "1-Foundation.md",
    "2-Domains.md",
    "3-Entities.md",
    "4-Enumerations.md",
    "5-Relationships.md",
    "6-Events.md",
    "7-Sources.md",
    "8-Transformations.md",
    "9-Data-Products.md",
    "10-Adoption.md"
)

$files = foreach ($name in $sectionFiles) {
    $fullPath = Join-Path $specPath $name
    if (-not (Test-Path $fullPath)) {
        throw "Missing required spec section file: $name"
    }
    Get-Item $fullPath
}

$combined = New-Object System.Collections.Generic.List[string]

for ($i = 0; $i -lt $files.Count; $i++) {
    $file = $files[$i]
    $lines = [System.IO.File]::ReadAllLines($file.FullName)

    if ($lines.Length -lt 3) {
        $body = @()
    }
    else {
        # Keep one global H1 by dropping each section's first two lines in the body.
        $body = [System.Collections.Generic.List[string]]::new()
        foreach ($line in $lines[2..($lines.Length - 1)]) {
            [void]$body.Add($line)
        }

        # Remove optional trailing navigation block: blank lines, '---', blank lines, '...next:' line.
        while ($body.Count -gt 0 -and [string]::IsNullOrWhiteSpace($body[$body.Count - 1])) {
            $body.RemoveAt($body.Count - 1)
        }

        if ($body.Count -gt 0 -and $body[$body.Count - 1] -like "...next:*") {
            $body.RemoveAt($body.Count - 1)
            while ($body.Count -gt 0 -and [string]::IsNullOrWhiteSpace($body[$body.Count - 1])) {
                $body.RemoveAt($body.Count - 1)
            }
            if ($body.Count -gt 0 -and $body[$body.Count - 1] -eq "---") {
                $body.RemoveAt($body.Count - 1)
            }
            while ($body.Count -gt 0 -and [string]::IsNullOrWhiteSpace($body[$body.Count - 1])) {
                $body.RemoveAt($body.Count - 1)
            }
        }
    }

    if ($i -eq 0) {
        # Preserve single top-level title from section 1.
        [void]$combined.Add($lines[0])
        [void]$combined.Add("")
    }

    if ($i -gt 0) {
        [void]$combined.Add("")
    }

    foreach ($line in $body) {
        [void]$combined.Add($line)
    }
}

# Ensure UTF-8 output (without BOM) so punctuation remains stable across toolchains.
$utf8NoBom = New-Object System.Text.UTF8Encoding($false)
[System.IO.File]::WriteAllLines($outputPath, $combined, $utf8NoBom)

Write-Output "Regenerated $OutputFileName from $($files.Count) files in $SpecDir"