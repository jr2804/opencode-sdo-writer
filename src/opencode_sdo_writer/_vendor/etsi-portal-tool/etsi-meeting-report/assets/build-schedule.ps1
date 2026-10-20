#requires -Version 5.1
<#
.SYNOPSIS
  Renders an ETSI meeting schedule (time x day grid, legend, note row) into a report .docx.

.DESCRIPTION
  Generic and re-runnable. All meeting-specific content lives in the config file passed
  with -Config (start from assets/schedule-config.example.ps1).

  Pipeline:
    1. batch 1 (atomic): remove everything between the heading and the end anchor,
       add the caption (style TH, no table counter)
    2. batch 2 (atomic): grid + legend + spacer, cell fills, hyperlinks, merges, styles
    3. post-step: tables set to AutoFit to Contents (tblW type=auto)
    4. officecli validate

  A failed batch is rolled back by officecli and the script exits with code 1.
  Save this file as UTF-8 with BOM (labels contain en-dashes).

.EXAMPLE
  powershell -ExecutionPolicy Bypass -File build-schedule.ps1 -Config .\<tc><nn>-schedule.ps1
#>
param([Parameter(Mandatory)][string]$Config)

$ErrorActionPreference = 'Stop'

# Config files must be UTF-8 with BOM: Windows PowerShell reads BOM-less files as ANSI,
# which garbles the dashes in labels.
$cfgPath  = (Resolve-Path -LiteralPath $Config).Path
$cfgBytes = [IO.File]::ReadAllBytes($cfgPath)
if ($cfgBytes.Length -lt 3 -or $cfgBytes[0] -ne 0xEF -or $cfgBytes[1] -ne 0xBB -or $cfgBytes[2] -ne 0xBF) {
  throw "Config is not UTF-8 with BOM: $cfgPath. Re-save it with a BOM."
}
. $cfgPath   # defines $Meeting, $Topics, $Slots, $FillMap, $DocCells, $Merges

# ---- defaults (override in the config) ---------------------------------------
if (-not $Meeting.GreyPattern)  { $Meeting.GreyPattern  = '^\(no meeting\)$|break$|^Social event' }
if (-not $Meeting.GreyFill)     { $Meeting.GreyFill     = '#999999' }
if (-not $Meeting.LinkColor)    { $Meeting.LinkColor    = '#00008B' }
if (-not $Meeting.LegendHeader) { $Meeting.LegendHeader = 'Legend' }
if (-not $Merges)               { $Merges = @() }

$doc = $Meeting.Doc
if (-not (Test-Path -LiteralPath $doc)) { throw "Report not found: $doc" }
$W   = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'
$man = Get-Content -Raw -LiteralPath $Meeting.Manifest | ConvertFrom-Json

$nRows = $Slots.Count
$nCols = $Slots[0].Count
for ($i = 0; $i -lt $nRows; $i++) {
  if ($Slots[$i].Count -ne $nCols) { throw "Slot row $($i + 1) has $($Slots[$i].Count) cells, expected $nCols." }
}

# ---- helpers -----------------------------------------------------------------
function Q([string]$s) { '"' + ($s -replace '"', '""') + '"' }
function Rows([object[]]$rows) { ($rows | ForEach-Object { ($_ | ForEach-Object { Q $_ }) -join ',' }) -join ';' }
function Get-Listing { officecli get $doc /body --depth 1 2>&1 | Out-String }
function Find-Line([string[]]$lines, [string]$pattern) {
  for ($i = 0; $i -lt $lines.Count; $i++) { if ($lines[$i] -match $pattern) { return $i } }
  return -1
}
function Get-DocUrl([string]$short) {
  $uid = $Meeting.UidPrefix + $short
  $d = $man.documents | Where-Object { $_.uid -eq $uid } | Select-Object -First 1
  if ($d -and $d.docbox_url) { return [string]$d.docbox_url }
  return $null
}
function Invoke-Batch([System.Collections.Generic.List[object]]$ops, [string]$label) {
  if ($ops.Count -eq 0) { return }
  $json = ConvertTo-Json -InputObject @($ops.ToArray()) -Depth 8
  $tmp  = Join-Path $env:TEMP "schedule-$label.json"
  [IO.File]::WriteAllText($tmp, $json, [Text.UTF8Encoding]::new($false))
  $raw  = officecli batch $doc --input $tmp --json 2>&1 | Out-String
  $resp = $raw | ConvertFrom-Json
  $s    = $resp.data.summary
  Write-Host ("[{0}] success={1} ops={2} failed={3} rolledBack={4}" -f $label, $resp.success, $s.total, $s.failed, $s.atomicRolledBack)
  if (-not $resp.success) { Write-Host "[$label] batch failed; nothing applied:" -ForegroundColor Red; $raw; exit 1 }
}

# ---- merge bookkeeping (horizontal merges must end at the last column) -----
$removed   = @{}   # "r,c" cells absorbed by a colspan (they do not exist after the batch)
$restartOf = @{}   # "r,c" continuation cell of a vertical merge -> "r,c" of its restart cell
$mergeAt   = @{}   # "r,c" restart cell -> merge spec
foreach ($m in $Merges) {
  if (-not $m.RowSpan) { $m.RowSpan = 1 }
  if (-not $m.ColSpan) { $m.ColSpan = 1 }
  if ($m.ColSpan -gt 1 -and $m.Col + $m.ColSpan - 1 -ne $nCols) { throw "Merge at row $($m.Row), col $($m.Col): only horizontal merges ending at the last column are supported." }
  if ($m.Row + $m.RowSpan - 1 -gt $nRows) { throw "Merge at row $($m.Row) exceeds the grid ($nRows rows)." }
  $mergeAt["$($m.Row),$($m.Col)"] = $m
  for ($r = $m.Row; $r -lt $m.Row + $m.RowSpan; $r++) {
    for ($c = $m.Col + 1; $c -lt $m.Col + $m.ColSpan; $c++) { $removed["$r,$c"] = $true }
    if ($r -gt $m.Row) { $restartOf["$r,$($m.Col)"] = "$($m.Row),$($m.Col)" }
  }
}

function Get-Fill([int]$r, [int]$c) {
  $key = "$r,$c"
  if ($FillMap.Contains($key)) { return $Topics[$FillMap[$key]] }
  if ($r -lt $nRows) {
    $label = [string]$Slots[$r - 1][$c - 1]
    if ($label -ne '' -and $label -match $Meeting.GreyPattern) { return @{ fill = $Meeting.GreyFill; text = '#000000' } }
  }
  return $null
}
function Get-CellFill([int]$r, [int]$c) {
  $key = "$r,$c"
  if ($restartOf.ContainsKey($key)) {
    $p = $restartOf[$key].Split(',')
    return Get-Fill ([int]$p[0]) ([int]$p[1])
  }
  return Get-Fill $r $c
}
function FillProps($f) { if ($f) { @{ fill = $f.fill; color = $f.text } } else { @{} } }

# ============================ BATCH 1: clear, caption ========================
$lines = (Get-Listing) -split "`n"
$hLine = Find-Line $lines ([regex]::Escape($Meeting.Heading))
$eLine = Find-Line $lines ([regex]::Escape($Meeting.EndAnchor))
if ($hLine -lt 0) { throw "Heading not found: $($Meeting.Heading)" }
if ($eLine -le $hLine) { throw "End anchor not found after the heading: $($Meeting.EndAnchor)" }
if ($lines[$hLine] -notmatch '^(/body/p\[@paraId=[0-9A-F]+\])') { throw 'Heading path not parsed.' }
$headPath = $Matches[1]

$ops1   = [System.Collections.Generic.List[object]]::new()
$tblIdx = @()
for ($i = $hLine + 1; $i -lt $eLine; $i++) {
  if ($lines[$i] -match '^(/body/p\[@paraId=[0-9A-F]+\]) \(paragraph\)') { $ops1.Add(@{ command = 'remove'; path = $Matches[1] }) }
  elseif ($lines[$i] -match '^/body/tbl\[(\d+)\]') { $tblIdx += [int]$Matches[1] }
}
foreach ($t in ($tblIdx | Sort-Object -Descending)) { $ops1.Add(@{ command = 'remove'; path = "/body/tbl[$t]" }) }
$ops1.Add(@{ command = 'add'; parent = '/body'; type = 'paragraph'; after = $headPath; props = @{ style = 'TH'; text = $Meeting.Caption } })
Invoke-Batch $ops1 'clear'

# ============================ BATCH 2: grid ==================================
$lines = (Get-Listing) -split "`n"
$capLine = -1
for ($i = 0; $i -lt $lines.Count; $i++) {
  if ($lines[$i] -match '^/body/p\[@paraId=' -and $lines[$i].Contains($Meeting.Caption)) { $capLine = $i; break }
}
if ($capLine -lt 0) { throw 'Caption not found after batch 1.' }
$null = $lines[$capLine] -match '^(/body/p\[@paraId=[0-9A-F]+\])'
$capPath = $Matches[1]

$PLAIN = @{ bold = 'false'; italic = 'false'; underline = 'none'; align = 'center'; valign = 'center' }
$ops   = [System.Collections.Generic.List[object]]::new()
function Put([int]$t, [int]$r, [int]$c, [hashtable]$p) {
  $ops.Add(@{ command = 'set'; path = "/body/tbl[$t]/tr[$r]/tc[$c]"; props = $p })
}
function Style([int]$t, [int]$r, [int]$c, [string]$name, [int]$para = 1) {
  $ops.Add(@{ command = 'set'; path = "/body/tbl[$t]/tr[$r]/tc[$c]/p[$para]"; props = @{ style = $name } })
}

# 1. tables and spacer
$legendRows = @( ,@($Meeting.LegendHeader, '') )
foreach ($k in $Topics.Keys) { $legendRows += ,@('', $Topics[$k].label) }
$noteRow = 0
if ($Meeting.LegendNote) { $legendRows += ,@($Meeting.LegendNote, ''); $noteRow = $legendRows.Count }
$ops.Add(@{ command = 'add'; parent = '/body'; type = 'table'; after = $capPath;
            props = @{ rows = $nRows; cols = $nCols; data = (Rows $Slots) } })
$ops.Add(@{ command = 'add'; parent = '/body'; type = 'table'; after = '/body/tbl[2]';
            props = @{ rows = $legendRows.Count; cols = 2; data = (Rows $legendRows) } })
$ops.Add(@{ command = 'add'; parent = '/body'; type = 'paragraph'; after = '/body/tbl[2]'; props = @{ text = '' } })
$ops.Add(@{ command = 'set'; path = '/body/tbl[2]'; props = @{ align = 'center'; layout = 'autofit' } })
$ops.Add(@{ command = 'set'; path = '/body/tbl[3]'; props = @{ align = 'center'; layout = 'autofit' } })

# 2. base formatting and fills (every cell that will exist after the merges)
for ($r = 1; $r -le $nRows; $r++) {
  for ($c = 1; $c -le $nCols; $c++) {
    if ($removed.ContainsKey("$r,$c")) { continue }
    $p = @{} + $PLAIN
    if ($r -eq 1) { $p.bold = 'true' }
    $f = Get-CellFill $r $c
    if ($f) { $p.fill = $f.fill; $p.color = $f.text }
    Put 2 $r $c $p
  }
}

# 3. document links: a cell holds the seed label (keep) or the document numbers only
foreach ($k in $DocCells.Keys) {
  $r, $c = $k -split ','
  $spec = $DocCells[$k]
  $cp   = "/body/tbl[2]/tr[$r]/tc[$c]"
  $ops.Add(@{ command = 'add'; parent = $cp; type = 'paragraph'; props = @{} })
  $h = 0
  for ($i = 0; $i -lt $spec.Docs.Count; $i++) {
    $short = [string]$spec.Docs[$i]
    if ($i -gt 0) { $ops.Add(@{ command = 'add'; parent = "$cp/p[2]"; type = 'run'; props = @{ text = ', ' } }) }
    $url = Get-DocUrl $short
    if ($url) {
      $h++
      $ops.Add(@{ command = 'add'; parent = "$cp/p[2]"; type = 'hyperlink'; props = @{ url = $url; text = "#$short"; rStyle = 'Hyperlink' } })
      $ops.Add(@{ command = 'set'; path = "$cp/p[2]/hyperlink[$h]/r[1]"; props = @{ color = $Meeting.LinkColor } })
    } else {
      $ops.Add(@{ command = 'add'; parent = "$cp/p[2]"; type = 'run'; props = @{ text = "#$short" } })
    }
  }
  if (-not $spec.Keep) { $ops.Add(@{ command = 'remove'; path = "$cp/p[1]" }) }
}

# 4. merges (last: after this, absorbed cells no longer exist)
foreach ($k in $mergeAt.Keys) {
  $m = $mergeAt[$k]
  $rp = @{}
  if ($m.ColSpan -gt 1) { $rp.colspan = [int]$m.ColSpan }
  if ($m.RowSpan -gt 1) { $rp.vmerge = 'restart' }
  if ($rp.Count -gt 0) { Put 2 $m.Row $m.Col $rp }
  $f = Get-Fill $m.Row $m.Col
  for ($r = $m.Row + 1; $r -lt $m.Row + $m.RowSpan; $r++) {
    $cp = @{ text = ''; vmerge = 'continue'; hideMark = 'true' } + (FillProps $f)
    if ($m.ColSpan -gt 1) { $cp.colspan = [int]$m.ColSpan }
    Put 2 $r $m.Col $cp
  }
}

# 5. paragraph styles on surviving cells (after the merges)
for ($r = 1; $r -le $nRows; $r++) {
  for ($c = 1; $c -le $nCols; $c++) {
    if ($removed.ContainsKey("$r,$c")) { continue }
    $name = if ($r -eq 1) { 'TAH' } elseif ($r -eq $nRows) { 'TAN' } else { 'TAC' }
    Style 2 $r $c $name
  }
}
foreach ($k in $DocCells.Keys) {
  if ($DocCells[$k].Keep) { $r, $c = $k -split ','; Style 2 ([int]$r) ([int]$c) 'TAC' 2 }
}

# 6. legend: header spanning both columns, swatch per topic, label per topic
Put 3 1 1 @{ colspan = 2; bold = 'true'; align = 'center'; valign = 'center' }
Style 3 1 1 'TAH'
$i = 0
foreach ($k in $Topics.Keys) {
  $r = $i + 2
  Put 3 $r 1 (@{ fill = $Topics[$k].fill } + $PLAIN)
  Put 3 $r 2 @{ bold = 'false'; italic = 'false'; underline = 'none'; align = 'left'; valign = 'center' }
  Style 3 $r 1 'TAC'
  Style 3 $r 2 'TAC'
  $i++
}

if ($noteRow -gt 0) {
  Put 3 $noteRow 1 @{ colspan = 2; bold = 'false'; italic = 'false'; underline = 'none'; align = 'center'; valign = 'center' }
  Style 3 $noteRow 1 'TAN'
}

Invoke-Batch $ops 'grid'

# ============================ POST: AutoFit to Contents ======================
officecli close $doc 2>&1 | Out-Null
Add-Type -AssemblyName System.IO.Compression
Add-Type -AssemblyName System.IO.Compression.FileSystem
$zip = [IO.Compression.ZipFile]::Open($doc, 'Update')
try {
  $entry = $zip.GetEntry('word/document.xml')
  $sr = New-Object IO.StreamReader($entry.Open())
  [xml]$x = $sr.ReadToEnd()
  $sr.Close()
  $bodyNode = $x.DocumentElement.SelectSingleNode("//*[local-name()='body']")
  $afterCaption = $false; $patched = 0
  foreach ($node in $bodyNode.ChildNodes) {
    if (-not $afterCaption) {
      if ($node.LocalName -eq 'p' -and $node.InnerText -eq $Meeting.Caption) { $afterCaption = $true }
      continue
    }
    if ($node.LocalName -eq 'tbl') {
      $tblW = $node.SelectSingleNode("./*[local-name()='tblPr']/*[local-name()='tblW']")
      $tblW.SetAttribute('w', $W, '0')
      $tblW.SetAttribute('type', $W, 'auto')
      $patched++
      if ($patched -eq 2) { break }
    }
  }
  if ($patched -ne 2) { throw "Expected 2 tables after the caption, patched $patched." }
  $ms = New-Object IO.MemoryStream
  $x.Save($ms)
  $entry.Delete()
  $new = $zip.CreateEntry('word/document.xml')
  $ws  = $new.Open(); $bytes = $ms.ToArray(); $ws.Write($bytes, 0, $bytes.Length); $ws.Close()
  Write-Host 'AutoFit to Contents set on 2 tables.'
} finally {
  $zip.Dispose()
}
officecli validate $doc
