$action = New-ScheduledTaskAction `
  -Execute 'python' `
  -Argument 'C:\dev\01_projects\03_tech-review\blog\scripts\analyze-youtube.py' `
  -WorkingDirectory 'C:\dev\01_projects\03_tech-review\blog'

$trigger = New-ScheduledTaskTrigger -Daily -At '09:00AM'

$settings = New-ScheduledTaskSettingsSet `
  -ExecutionTimeLimit (New-TimeSpan -Minutes 15) `
  -StartWhenAvailable

Register-ScheduledTask `
  -TaskName 'TechReview-YoutubeAnalyzer' `
  -Action $action `
  -Trigger $trigger `
  -Settings $settings `
  -Force

Write-Host "등록 완료: TechReview-YoutubeAnalyzer (매일 09:00)"
