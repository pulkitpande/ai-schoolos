@echo off
echo ========================================
echo AI SchoolOS - Full Stack Starter
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

REM Check if Node.js is available
node --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Node.js is not installed or not in PATH
    echo Please install Node.js 16+ and try again
    pause
    exit /b 1
)

REM Check if npm is available
npm --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: npm is not installed or not in PATH
    echo Please install npm and try again
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

if not exist "frontend" (
    echo ERROR: frontend directory not found!
    echo Please run this script from the project root directory
    pause
    exit /b 1
)

REM Show help if no arguments provided
if "%1"=="" (
    echo Usage:
    echo   start-full-stack.bat [services]
    echo.
    echo Examples:
    echo   start-full-stack.bat
    echo   start-full-stack.bat auth-service student-service
    echo   start-full-stack.bat auth-service student-service ai-service
    echo.
    echo Available backend services:
    echo   api-gateway, auth-service, student-service, staff-service
    echo   ai-service, analytics-service, notification-service
    echo   communication-service, attendance-service, timetable-service
    echo   exam-service, library-service, homework-service
    echo   fee-service, transport-service, config-service, super-admin-service
    echo.
    echo This will start:
    echo   - Backend services (default: auth-service, student-service)
    echo   - Frontend development server (http://localhost:3000)
    echo   - API Gateway (http://localhost:8000)
    echo.
    pause
    exit /b 0
)

REM Run the Python script with arguments
echo 🚀 Starting AI SchoolOS Full Stack...
echo.
python start-full-stack.py --services %*

if errorlevel 1 (
    echo.
    echo An error occurred. Please check the output above.
    pause
    exit /b 1
)

echo.
echo Full stack started successfully!
pause 