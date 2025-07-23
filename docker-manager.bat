@echo off
echo ========================================
echo AI SchoolOS - Docker Manager
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

REM Check if Docker is available
docker --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Docker is not installed or not in PATH
    echo Please install Docker Desktop and try again
    pause
    exit /b 1
)

REM Check if Docker Compose is available
docker-compose --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Docker Compose is not installed or not in PATH
    echo Please install Docker Compose and try again
    pause
    exit /b 1
)

REM Check if we're in the right directory
if not exist "docker-compose.development.yml" (
    echo ERROR: docker-compose.development.yml not found!
    echo Please run this script from the project root directory
    pause
    exit /b 1
)

if not exist "docker-compose.production.yml" (
    echo ERROR: docker-compose.production.yml not found!
    echo Please run this script from the project root directory
    pause
    exit /b 1
)

REM Show help if no arguments provided
if "%1"=="" (
    echo Usage:
    echo   docker-manager.bat [command] [options]
    echo.
    echo Commands:
    echo   run                    - Start full stack (development)
    echo   run --production       - Start full stack (production)
    echo   build                  - Build images (development)
    echo   build --production     - Build images (production)
    echo   start                  - Start services (development)
    echo   start --production     - Start services (production)
    echo   stop                   - Stop services (development)
    echo   stop --production      - Stop services (production)
    echo   restart                - Restart services (development)
    echo   restart --production   - Restart services (production)
    echo   status                 - Show service status (development)
    echo   status --production    - Show service status (production)
    echo   logs                   - Show logs (development)
    echo   logs --production      - Show logs (production)
    echo   health                 - Check service health (development)
    echo   health --production    - Check service health (production)
    echo   clean                  - Clean up resources (development)
    echo   clean --production     - Clean up resources (production)
    echo.
    echo Examples:
    echo   docker-manager.bat run
    echo   docker-manager.bat run --production
    echo   docker-manager.bat status
    echo   docker-manager.bat logs --follow
    echo   docker-manager.bat health --production
    echo.
    pause
    exit /b 0
)

REM Parse arguments
set COMMAND=%1
set ENVIRONMENT=development

if "%2"=="--production" (
    set ENVIRONMENT=production
)

REM Run the Python script with arguments
echo 🚀 Running Docker Manager...
echo Command: %COMMAND%
echo Environment: %ENVIRONMENT%
echo.

python docker-manager.py %COMMAND% --environment %ENVIRONMENT%

if errorlevel 1 (
    echo.
    echo An error occurred. Please check the output above.
    pause
    exit /b 1
)

echo.
echo Docker Manager operation completed successfully!
pause 