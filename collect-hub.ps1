<#
.SYNOPSIS
    Collect interesting HUB files into one dump.

.PARAMETER Root
    Repo root. Default: current directory.

.PARAMETER Output
    Output file name. Default: hub_dump.txt.

.PARAMETER MaxFileSizeKB
    Max size per file in KB. Bigger files are truncated.
#>

param(
    [string]$Root = ".",
    [string]$Output = "hub_dump.txt",
    [int]$MaxFileSizeKB = 200
)

$ErrorActionPreference = "Stop"

$ExcludeDirs = @(
    '.git', '__pycache__', '.venv', 'venv', 'env',
    'node_modules', 'build', 'dist', '.pytest_cache',
    '.mypy_cache', '.idea', '.vscode', '.vs', 'bin', 'obj',
    'htmlcov', '.tox', '.eggs', 'site-packages'
)

$ExcludeExt = @(
    '.png', '.jpg', '.jpeg', '.gif', '.webp', '.ico', '.bmp',
    '.zip', '.tar', '.gz', '.7z', '.rar',
    '.exe', '.dll', '.so', '.dylib', '.pyc', '.pyo', '.pyd',
    '.woff', '.woff2', '.ttf', '.otf', '.eot',
    '.mp3', '.mp4', '.wav', '.mov', '.avi'
)

$IncludeExt = @(
    '.py', '.yml', '.yaml', '.json', '.md', '.txt',
    '.toml', '.cfg', '.ini', '.sh', '.ps1', '.bat',
    '.sql', '.html', '.js'
)

$IncludeNames = @(
    'README', 'LICENSE', 'Makefile', 'Dockerfile',
    '.gitignore', '.gitattributes', '.editorconfig',
    'Procfile'
)

function Test-ShouldInclude {
    param([System.IO.FileInfo]$File)

    $ext = $File.Extension.ToLowerInvariant()
    if ($ExcludeExt -contains $ext) { return $false }
    if ($IncludeExt -contains $ext) { return $true }

    $nameNoExt = [System.IO.Path]::GetFileNameWithoutExtension($File.Name)
    if ($IncludeNames -contains $nameNoExt) { return $true }
    if ($IncludeNames -contains $File.Name) { return $true }

    return $false
}

function Test-ShouldSkipDir {
    param([string]$Name)
    return $ExcludeDirs -contains $Name
}

$rootItem = Get-Item -LiteralPath $Root
$rootFull = $rootItem.FullName

Write-Host "Scanning: $rootFull" -ForegroundColor Cyan

$files = @()
$stack = New-Object System.Collections.Stack
$stack.Push($rootFull)

while ($stack.Count -gt 0) {
    $dir = $stack.Pop()

    $subdirs = Get-ChildItem -LiteralPath $dir -Directory -ErrorAction SilentlyContinue
    foreach ($sd in $subdirs) {
        if (Test-ShouldSkipDir -Name $sd.Name) { continue }
        $stack.Push($sd.FullName)
    }

    $fs = Get-ChildItem -LiteralPath $dir -File -ErrorAction SilentlyContinue
    foreach ($f in $fs) {
        if (Test-ShouldInclude -File $f) {
            $files += $f
        }
    }
}

Write-Host "Files found: $($files.Count)" -ForegroundColor Cyan

$files = $files | Sort-Object { $_.FullName }

$sb = New-Object System.Text.StringBuilder

[void]$sb.AppendLine("# HUB DUMP")
[void]$sb.AppendLine("# Root: $rootFull")
[void]$sb.AppendLine("# Date: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')")
[void]$sb.AppendLine("# Files: $($files.Count)")
[void]$sb.AppendLine()

[void]$sb.AppendLine("# ---- TABLE OF CONTENTS ----")
foreach ($f in $files) {
    $rel = $f.FullName.Substring($rootFull.Length).TrimStart('\', '/').Replace('\', '/')
    [void]$sb.AppendLine("#   $rel")
}
[void]$sb.AppendLine()

foreach ($f in $files) {
    $rel = $f.FullName.Substring($rootFull.Length).TrimStart('\', '/').Replace('\', '/')
    $sizeKb = [Math]::Round($f.Length / 1KB, 1)

    [void]$sb.AppendLine("// ============ FILE: $rel ============")

    if ($f.Length -gt ($MaxFileSizeKB * 1024)) {
        $bytes = [System.IO.File]::ReadAllBytes($f.FullName)
        $take = $MaxFileSizeKB * 1024
        $slice = $bytes[0..($take - 1)]
        $text = [System.Text.Encoding]::UTF8.GetString($slice)
        [void]$sb.AppendLine($text)
        [void]$sb.AppendLine()
        [void]$sb.AppendLine("// ... (truncated, full size: $sizeKb KB)")
    } else {
        try {
            $text = [System.IO.File]::ReadAllText($f.FullName, [System.Text.Encoding]::UTF8)
        } catch {
            try {
                $text = [System.IO.File]::ReadAllText($f.FullName, [System.Text.Encoding]::GetEncoding('windows-1251'))
            } catch {
                $text = "<failed to read file>"
            }
        }
        [void]$sb.AppendLine($text)
    }

    [void]$sb.AppendLine()
}

$outPath = Join-Path $rootFull $Output
[System.IO.File]::WriteAllText($outPath, $sb.ToString(), [System.Text.UTF8Encoding]::new($false))

Write-Host "Done: $outPath" -ForegroundColor Green
Write-Host "Size: $([Math]::Round((Get-Item $outPath).Length / 1KB, 1)) KB" -ForegroundColor Green