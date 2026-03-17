$yf = "C:\dev\01_projects\03_tech-review\blog\_data\analyze-status.json"
$tf = "C:\dev\01_projects\03_tech-review\blog\_data\bookmarks.json"
while ($true) {
    cls
    $y = Get-Content $yf -Encoding UTF8 | ConvertFrom-Json
    $t = (Get-Content $tf -Encoding UTF8 | ConvertFrom-Json).Count
    Write-Host "[YouTube] $($y.done)/$($y.total) - $($y.step): $($y.video)" -F Cyan
    Write-Host "[Twitter] $t/52" -F Yellow
    Start-Sleep 5
}
