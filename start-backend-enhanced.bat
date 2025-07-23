@echo off
echo ========================================
echo AI SchoolOS - Enhanced Backend Starter
echo ========================================
echo.

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.7+ and try again
    pause
    exit /b 1
)

REM Check if we're in the right directory
if not exist "backend" (
    echo ERROR: backend directory not found!
    echo Please run this script from the project root directory
    pause
    exit /b 1
)

REM Show help if no arguments provided
if "%1"=="" (
    echo Usage:
    echo   start-backend-enhanced.bat install [services]
    echo   start-backend-enhanced.bat start [services]
    echo   start-backend-enhanced.bat check
    echo   start-backend-enhanced.bat setup
    echo.
    echo Examples:
    echo   start-backend-enhanced.bat install
    echo   start-backend-enhanced.bat install auth-service student-service
    echo   start-backend-enhanced.bat start auth-service student-service
    echo   start-backend-enhanced.bat check
    echo.
    echo Available services:
    echo   api-gateway, auth-service, student-service, staff-service
    echo   ai-service, analytics-service, notification-service
    echo   communication-service, attendance-service, timetable-service
    echo   exam-service, library-service, homework-service
    echo   fee-service, transport-service, config-service, super-admin-service
    echo.
    pause
    exit /b 0
)

REM Run the Python script with arguments
python start-backend-simple.py %*

if errorlevel 1 (
    echo.
    echo An error occurred. Please check the output above.
    pause
    exit /b 1
)

echo.
echo Operation completed successfully!
pause 