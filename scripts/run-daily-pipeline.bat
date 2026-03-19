@echo off
REM Daily Tech Review Pipeline — Task Scheduler 진입점
REM 컴퓨터 wake 후 자동 실행

cd /d C:\dev\01_projects\03_tech-review\blog
echo [%date% %time%] === Pipeline 시작 === >> scripts\_logs\daily-pipeline.log

C:\Users\pauls\AppData\Local\Programs\Python\Python312\python.exe scripts\run-daily-pipeline.py --date %date:~0,4%-%date:~5,2%-%date:~8,2% >> scripts\_logs\daily-pipeline.log 2>&1

echo [%date% %time%] === Pipeline 종료 (exit %errorlevel%) === >> scripts\_logs\daily-pipeline.log
