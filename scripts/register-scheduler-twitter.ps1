# Chrome CDP 자동화 전용 프로필로 북마크 수집
# 사전 조건: Chrome이 --remote-debugging-port=9222 --user-data-dir="C:\Users\pauls\.chrome-twitter-auto" 로 실행 중

$action = New-ScheduledTaskAction `
  -Execute 'python' `
  -Argument 'C:\dev\01_projects\03_tech-review\blog\scripts\fetch-twitter-pw.py' `
  -WorkingDirectory 'C:\dev\01_projects\03_tech-review\blog'

$trigger = New-ScheduledTaskTrigger -Daily -At '10:00AM'

$settings = New-ScheduledTaskSettingsSet `
  -ExecutionTimeLimit (New-TimeSpan -Minutes 10) `
  -StartWhenAvailable

Register-ScheduledTask `
  -TaskName 'TechReview-TwitterBookmarkFetch' `
  -Action $action `
  -Trigger $trigger `
  -Settings $settings `
  -Force

Write-Host "등록 완료: TechReview-TwitterBookmarkFetch (매일 10:00)"
