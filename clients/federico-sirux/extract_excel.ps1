
$sharedStringsPath = "C:/Users/kein-/OneDrive/Desktop/Riqueza Digital/Clientes/Federico - Sirux/crm_logic_unzipped/xl/sharedStrings.xml"
$sheetPath = "C:/Users/kein-/OneDrive/Desktop/Riqueza Digital/Clientes/Federico - Sirux/crm_logic_unzipped/xl/worksheets/sheet2.xml"

if (-not (Test-Path $sharedStringsPath)) { Write-Error "Shared strings not found"; exit }
if (-not (Test-Path $sheetPath)) { Write-Error "Sheet not found"; exit }

[xml]$sharedStrings = Get-Content $sharedStringsPath
[xml]$sheet = Get-Content $sheetPath

$strings = $sharedStrings.sst.si | ForEach-Object { 
    if ($_.t.InnerText) { $_.t.InnerText } 
    elseif ($_.t) { $_.t }
    else { "" }
}

$rows = $sheet.worksheet.sheetData.row
foreach ($row in $rows) {
    $line = @()
    foreach ($cell in $row.c) {
        if ($cell.t -eq 's') {
            $index = [int]$cell.v
            $line += $strings[$index]
        } elseif ($cell.v) {
            $line += $cell.v
        } else {
            $line += ""
        }
    }
    Write-Host ($line -join " | ")
}
