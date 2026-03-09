param(
    [string]$Version = "14.0.0",
    [string]$Organisation = "BIAN",
    [string]$OutputDir,
    [string]$BaseUrl = "https://bian-modelapi-v8.azurewebsites.net",
    [string]$FallbackBaseUrl = "https://bian-modelapi-v4.azurewebsites.net",
    [string]$BearerToken,
    [switch]$Force,
    [switch]$AllowEmpty
)

$ErrorActionPreference = "Stop"
$ProgressPreference = "SilentlyContinue"

if (-not $BearerToken -and $env:BIAN_BEARER_TOKEN) {
    $BearerToken = $env:BIAN_BEARER_TOKEN
}

if (-not $OutputDir) {
    $major = $Version.Split('.')[0]
    $OutputDir = Join-Path $PSScriptRoot ("v" + $major)
}

if (-not (Test-Path $OutputDir)) {
    New-Item -ItemType Directory -Path $OutputDir | Out-Null
}

$bases = @()
if ($BaseUrl) {
    $bases += $BaseUrl.TrimEnd('/')
}
if ($FallbackBaseUrl) {
    $candidate = $FallbackBaseUrl.TrimEnd('/')
    if ($bases -notcontains $candidate) {
        $bases += $candidate
    }
}

if ($bases.Count -eq 0) {
    throw "At least one base URL must be provided."
}

$headers = @{}
if ($BearerToken) {
    $headers["Authorization"] = "Bearer $BearerToken"
}

function Invoke-JsonEndpoint {
    param(
        [string]$Base,
        [string]$Path
    )

    $url = "$Base$Path"
    try {
        if ($headers.Count -gt 0) {
            $resp = Invoke-WebRequest -Uri $url -UseBasicParsing -TimeoutSec 90 -Headers $headers
        }
        else {
            $resp = Invoke-WebRequest -Uri $url -UseBasicParsing -TimeoutSec 90
        }
        $data = $null
        if ($resp.Content -and $resp.Content.Trim().Length -gt 0) {
            $data = $resp.Content | ConvertFrom-Json
        }
        return @{ Url = $url; Data = $data; Error = $null; StatusCode = 200 }
    }
    catch {
        $statusCode = $null
        if ($_.Exception.Response) {
            $statusCode = [int]$_.Exception.Response.StatusCode
        }
        return @{ Url = $url; Data = $null; Error = $_.Exception.Message; StatusCode = $statusCode }
    }
}

function Test-NonEmptyArray {
    param($Value)
    return $Value -is [System.Array] -and $Value.Count -gt 0
}

$targets = @(
    @{
        File      = "BOClassesLite.json"
        Endpoints = @(
            "/BOClassesLite/$Organisation/$Version",
            "/BOClassesBasic/$Organisation/$Version"
        )
    },
    @{
        File      = "BOEnumerationsLite.json"
        Endpoints = @(
            "/BOEnumerationsLite/$Organisation/$Version",
            "/BOEnumerationsBasic/$Organisation/$Version"
        )
    },
    @{
        File      = "BusinessAreas.json"
        Endpoints = @(
            "/BusinessAreas/$Organisation/$Version"
        )
    },
    @{
        File      = "BusinessDomains.json"
        Endpoints = @(
            "/BusinessDomains/$Organisation/$Version",
            "/BusinessDomainsBasic/$Organisation/$Version"
        )
    },
    @{
        File      = "ServiceDomainsBasic.json"
        Endpoints = @(
            "/ServiceDomainsBasic/$Organisation/$Version"
        )
    }
)

$summary = @()

foreach ($target in $targets) {
    $filePath = Join-Path $OutputDir $target.File
    if ((Test-Path $filePath) -and -not $Force) {
        Write-Host "Skipping existing file: $filePath"
        $summary += [pscustomobject]@{ File = $target.File; Status = "skipped"; Source = "existing"; Count = "n/a" }
        continue
    }

    $selected = $null
    $attempts = @()

    foreach ($endpoint in $target.Endpoints) {
        foreach ($base in $bases) {
            $result = Invoke-JsonEndpoint -Base $base -Path $endpoint
            $attempts += $result
            if ($result.Error) {
                continue
            }
            if (Test-NonEmptyArray -Value $result.Data) {
                $selected = $result
                break
            }
            if ($AllowEmpty -and $null -ne $result.Data) {
                $selected = $result
                break
            }
        }
        if ($selected) {
            break
        }
    }

    if (-not $selected) {
        Write-Warning "No usable data for $($target.File). Attempts:"
        foreach ($a in $attempts) {
            if ($a.Error) {
                if ($a.StatusCode) {
                    Write-Warning ("  " + $a.Url + " -> HTTP " + $a.StatusCode + ": " + $a.Error)
                }
                else {
                    Write-Warning ("  " + $a.Url + " -> ERROR: " + $a.Error)
                }
            }
            elseif ($a.Data -is [System.Array]) {
                Write-Warning ("  " + $a.Url + " -> array length " + $a.Data.Count)
            }
            else {
                Write-Warning ("  " + $a.Url + " -> non-array payload")
            }
        }
        $summary += [pscustomobject]@{ File = $target.File; Status = "missing"; Source = "none"; Count = 0 }
        continue
    }

    $selected.Data | ConvertTo-Json -Depth 100 | Set-Content -Path $filePath -Encoding UTF8
    $count = if ($selected.Data -is [System.Array]) { $selected.Data.Count } else { 1 }
    Write-Host "Wrote $filePath ($count records) from $($selected.Url)"
    $summary += [pscustomobject]@{ File = $target.File; Status = "written"; Source = $selected.Url; Count = $count }
}

Write-Host ""
Write-Host "Snapshot Summary"
$summary | Format-Table -AutoSize

if ($BearerToken) {
    Write-Host "Auth mode: bearer token provided"
}
else {
    Write-Host "Auth mode: anonymous (set BIAN_BEARER_TOKEN or -BearerToken for protected endpoints)"
}
Write-Host ("Base URLs tried: " + ($bases -join ", "))

$missing = @($summary | Where-Object { $_.Status -eq "missing" })
if ($missing.Count -gt 0 -and -not $AllowEmpty) {
    throw "One or more required datasets are unavailable. Re-run later or use -AllowEmpty if you want to persist empty payloads."
}
