@echo off
REM Tech Review Master Pipeline — Task Scheduler 진입점
REM Daily + YouTube + Twitter 순차 실행
REM 노트북이 켜져있는 한 자동 실행

cd /d C:\dev\01_projects\03_tech-review\blog

C:\Users\pauls\AppData\Local\Programs\Python\Python312\python.exe scripts\run-all-pipelines.py

exit /b %errorlevel%
