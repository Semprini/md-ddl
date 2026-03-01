param(
    [string]$SpecDir = "md-ddl-specification",
    [string]$OutputFileName = "MD-DDL-Complete.md"
)

$repoRoot = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
$specPath = Join-Path $repoRoot $SpecDir
$outputPath = Join-Path $specPath $OutputFileName

$files = Get-ChildItem -Path $specPath -File -Filter "*.md" |
Where-Object { $_.Name -ne $OutputFileName } |
Sort-Object Name

$combined = New-Object System.Collections.Generic.List[string]

for ($i = 0; $i -lt $files.Count; $i++) {
    $file = $files[$i]
    $lines = [System.IO.File]::ReadAllLines($file.FullName)

    $startIndex = if ($i -eq 0) { 0 } else { 2 }
    $endIndex = $lines.Length - 3

    $trimmed = if ($endIndex -ge $startIndex) {
        $lines[$startIndex..$endIndex]
    }
    else {
        @()
    }

    if ($i -gt 0) {
        $combined.Add("")
    }

    foreach ($line in $trimmed) {
        $combined.Add($line)
    }
}

[System.IO.File]::WriteAllLines($outputPath, $combined)

Write-Output "Regenerated $OutputFileName from $($files.Count) files in $SpecDir"