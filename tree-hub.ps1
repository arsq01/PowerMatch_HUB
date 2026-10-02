<#
.SYNOPSIS
    Build repository tree for HUB.

.PARAMETER Root
    Repo root. Default: current directory.

.PARAMETER Output
    Output file name. Default: hub_tree.txt.

.PARAMETER MaxDepth
    Max traversal depth. Default: 5.

.PARAMETER CollapseAt
    If a folder has more items - show first 5 + "... (+N more)".
    Default: 15.

.PARAMETER Ascii
    Use ASCII connectors instead of Unicode.
#>

param(
    [string]$Root = ".",
    [string]$Output = "hub_tree.txt",
    [int]$MaxDepth = 5,
    [int]$CollapseAt = 15,
    [switch]$Ascii
)

$ErrorActionPreference = "Stop"

$ExcludeDirs = @(
    '.git', '__pycache__', '.venv', 'venv', 'env',
    'node_modules', 'build', 'dist', '.pytest_cache',
    '.mypy_cache', '.idea', '.vscode', '.vs', 'bin', 'obj',
    'htmlcov', '.tox', '.eggs', 'site-packages'
)

if ($Ascii) {
    $Branch = '|-- '
    $Last   = '\-- '
    $Pipe   = '|   '
    $Space  = '    '
} else {
    $Branch = [char]0x251C + [char]0x2500 + [char]0x2500 + ' '
    $Last   = [char]0x2514 + [char]0x2500 + [char]0x2500 + ' '
    $Pipe   = [char]0x2502 + '   '
    $Space  = '    '
}

$rootItem = Get-Item -LiteralPath $Root
$rootFull = $rootItem.FullName

$sb = New-Object System.Text.StringBuilder
[void]$sb.AppendLine("# HUB TREE")
[void]$sb.AppendLine("# Root: $rootFull")
[void]$sb.AppendLine("# Date: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')")
[void]$sb.AppendLine("# MaxDepth: $MaxDepth, CollapseAt: $CollapseAt")
[void]$sb.AppendLine()
[void]$sb.AppendLine("$($rootItem.Name)/")

function Write-Tree {
    param(
        [string]$DirPath,
        [string]$Prefix,
        [int]$Depth
    )

    if ($Depth -ge $MaxDepth) {
        [void]$sb.AppendLine("$Prefix$Last...")
        return
    }

    $dirs = Get-ChildItem -LiteralPath $DirPath -Directory -ErrorAction SilentlyContinue |
        Where-Object { $ExcludeDirs -notcontains $_.Name } |
        Sort-Object Name
    $files = Get-ChildItem -LiteralPath $DirPath -File -ErrorAction SilentlyContinue |
        Sort-Object Name

    $all = @()
    foreach ($d in $dirs)  { $all += [pscustomobject]@{ Item = $d; IsDir = $true } }
    foreach ($f in $files) { $all += [pscustomobject]@{ Item = $f; IsDir = $false } }

    $total = $all.Count
    $collapse = $total -gt $CollapseAt

    if ($collapse) {
        $show = @()
        $showDirs  = $dirs  | Select-Object -First 5
        $showFiles = $files | Select-Object -First 5
        foreach ($d in $showDirs)  { $show += [pscustomobject]@{ Item = $d; IsDir = $true } }
        foreach ($f in $showFiles) { $show += [pscustomobject]@{ Item = $f; IsDir = $false } }
        $hidden = $total - $show.Count
        $all = $show
    } else {
        $hidden = 0
    }

    for ($i = 0; $i -lt $all.Count; $i++) {
        $entry = $all[$i]
        $isLast = ($i -eq ($all.Count - 1)) -and ($hidden -eq 0)

        $connector = if ($isLast) { $Last } else { $Branch }

        if ($entry.IsDir) {
            [void]$sb.AppendLine("$Prefix$connector$($entry.Item.Name)/")
            $nextPrefix = $Prefix + ($(if ($isLast) { $Space } else { $Pipe }))
            Write-Tree -DirPath $entry.Item.FullName -Prefix $nextPrefix -Depth ($Depth + 1)
        } else {
            [void]$sb.AppendLine("$Prefix$connector$($entry.Item.Name)")
        }
    }

    if ($hidden -gt 0) {
        [void]$sb.AppendLine("$Prefix$Last... (+$hidden more)")
    }
}

Write-Tree -DirPath $rootFull -Prefix '' -Depth 0

$outPath = Join-Path $rootFull $Output
[System.IO.File]::WriteAllText($outPath, $sb.ToString(), [System.Text.UTF8Encoding]::new($false))

Write-Host "Done: $outPath" -ForegroundColor Green