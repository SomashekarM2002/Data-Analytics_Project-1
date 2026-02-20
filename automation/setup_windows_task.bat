@echo off
REM ================================================================
REM Consumer360: Windows Task Scheduler Setup Script
REM Week 4: Automation & Handoff
REM ================================================================
REM This script creates a Windows Task Scheduler task to run the
REM Consumer360 pipeline automatically every Sunday at 6:00 AM
REM ================================================================

echo Setting up Consumer360 Automated Task...
echo.

REM Configuration
set TASK_NAME=Consumer360_Weekly_Update
set TASK_DESCRIPTION=Consumer360 Customer Segmentation Pipeline - Weekly Data Update
set SCRIPT_PATH=%~dp0scheduler.py
set PYTHON_PATH=python

REM Get current directory (where this batch file is located)
set WORKING_DIR=%~dp0

echo Task Name: %TASK_NAME%
echo Script Path: %SCRIPT_PATH%
echo Working Directory: %WORKING_DIR%
echo.

REM Delete existing task if it exists
schtasks /Query /TN "%TASK_NAME%" >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    echo Removing existing task...
    schtasks /Delete /TN "%TASK_NAME%" /F
)

REM Create new scheduled task
echo Creating scheduled task...
schtasks /Create ^
    /TN "%TASK_NAME%" ^
    /TR "\"%PYTHON_PATH%\" \"%SCRIPT_PATH%\" --mode once" ^
    /SC WEEKLY ^
    /D SUN ^
    /ST 06:00 ^
    /F ^
    /RL HIGHEST

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ========================================
    echo SUCCESS! Task created successfully.
    echo ========================================
    echo.
    echo Task Details:
    echo   Name: %TASK_NAME%
    echo   Schedule: Every Sunday at 6:00 AM
    echo   Script: %SCRIPT_PATH%
    echo.
    echo To view the task:
    echo   1. Open Task Scheduler (taskschd.msc)
    echo   2. Look for "%TASK_NAME%"
    echo.
    echo To run the task manually:
    echo   schtasks /Run /TN "%TASK_NAME%"
    echo.
    echo To delete the task:
    echo   schtasks /Delete /TN "%TASK_NAME%" /F
    echo.
) else (
    echo.
    echo ERROR: Failed to create scheduled task.
    echo Please run this script as Administrator.
    echo.
)

pause
