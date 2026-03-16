# === 구형 스케줄러 삭제 ===
Unregister-ScheduledTask -TaskName 'TechReview-BookmarkProcessor' -Confirm:$false -ErrorAction SilentlyContinue
Write-Host "삭제: TechReview-BookmarkProcessor (구형)"
Unregister-ScheduledTask -TaskName 'TechReview-TwitterBookmark' -Confirm:$false -ErrorAction SilentlyContinue
Write-Host "삭제: TechReview-TwitterBookmark (구형)"
Unregister-ScheduledTask -TaskName 'TechReview-TwitterBookmarkFetch' -Confirm:$false -ErrorAction SilentlyContinue
Write-Host "삭제: TechReview-TwitterBookmarkFetch (구형, 파이프라인으로 통합)"

# === 통합 파이프라인 등록 ===
$action = New-ScheduledTaskAction `
  -Execute 'python' `
  -Argument 'C:\dev\01_projects\03_tech-review\blog\scripts\run-twitter-pipeline.py' `
  -WorkingDirectory 'C:\dev\01_projects\03_tech-review\blog'

$trigger = New-ScheduledTaskTrigger -Daily -At '10:00AM'

$settings = New-ScheduledTaskSettingsSet `
  -ExecutionTimeLimit (New-TimeSpan -Minutes 15) `
  -StartWhenAvailable

Register-ScheduledTask `
  -TaskName 'TechReview-TwitterPipeline' `
  -Action $action `
  -Trigger $trigger `
  -Settings $settings `
  -Force

Write-Host "등록: TechReview-TwitterPipeline (매일 10:00, 전체 체인)"

# === CDP Chrome 시작 프로그램 등록 ===
$WshShell = New-Object -ComObject WScript.Shell
$startup = [Environment]::GetFolderPath('Startup')
$Shortcut = $WshShell.CreateShortcut("$startup\Chrome - Twitter Auto.lnk")
$Shortcut.TargetPath = "C:\Program Files\Google\Chrome\Application\chrome.exe"
$Shortcut.Arguments = '--remote-debugging-port=9222 --user-data-dir="C:\Users\pauls\.chrome-twitter-auto"'
$Shortcut.WorkingDirectory = "C:\Program Files\Google\Chrome\Application"
$Shortcut.IconLocation = "C:\Users\pauls\.chrome-twitter-auto\x-icon.ico,0"
$Shortcut.WindowStyle = 7  # 최소화 상태로 시작
$Shortcut.Save()
Write-Host "시작 프로그램 등록: $startup\Chrome - Twitter Auto.lnk (최소화)"
