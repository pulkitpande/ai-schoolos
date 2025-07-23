@echo off
echo ========================================
echo AI SchoolOS - Diagnostic Script
echo ========================================
echo.

echo [1/6] Checking Docker status...
docker --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ ERROR: Docker is not running or not installed!
    echo Please start Docker Desktop and run this script again.
    pause
    exit /b 1
) else (
    echo ✅ Docker is running
)

echo [2/6] Checking Docker Compose...
docker-compose --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ ERROR: Docker Compose is not available!
    pause
    exit /b 1
) else (
    echo ✅ Docker Compose is available
)

echo [3/6] Checking Node.js...
node --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ ERROR: Node.js is not installed!
    echo Please install Node.js v18 or higher
    pause
    exit /b 1
) else (
    echo ✅ Node.js is installed
    node --version
)

echo [4/6] Checking frontend dependencies...
if exist "frontend\node_modules" (
    echo ✅ Frontend dependencies are installed
) else (
    echo ⚠️  Frontend dependencies are missing
    echo Run: cd frontend && npm install
)

echo [5/6] Checking environment files...
if exist "frontend\.env.local" (
    echo ✅ Frontend environment file exists
) else (
    echo ⚠️  Frontend environment file is missing
    echo Run: fix-schoolos.bat to create it
)

echo [6/6] Checking Docker containers...
docker ps -a --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"
echo.

echo ========================================
echo Diagnostic Complete
echo ========================================
echo.
echo If you see any ❌ errors above, fix them first.
echo If you see any ⚠️  warnings, consider addressing them.
echo.
echo To start the application:
echo 1. Run: fix-schoolos.bat
echo 2. Or run: docker-compose -f docker-compose.simple.yml up -d
echo.
pause 