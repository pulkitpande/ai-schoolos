@echo off
echo ========================================
echo AI SchoolOS - FAST START
echo ========================================
echo.

echo [1/4] Checking Docker...
docker --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Docker is not running!
    echo Please start Docker Desktop and run this script again.
    pause
    exit /b 1
)

echo [2/4] Creating frontend environment...
if not exist "frontend\.env.local" (
    echo Creating frontend environment configuration...
    (
        echo NEXT_PUBLIC_API_URL=http://localhost:8000
        echo NEXT_PUBLIC_AUTH_SERVICE_URL=http://localhost:8001
        echo NEXT_PUBLIC_STUDENT_SERVICE_URL=http://localhost:8002
        echo NODE_ENV=development
    ) > frontend\.env.local
)

echo [3/4] Starting Docker services (SKIPPING npm install)...
docker-compose -f docker-compose.simple.yml down --volumes --remove-orphans
docker-compose -f docker-compose.simple.yml up -d --build

echo [4/4] Waiting for services...
timeout /t 15 /nobreak >nul

echo.
echo ========================================
echo 🎉 AI SchoolOS is starting!
echo ========================================
echo.
echo 📱 Frontend: http://localhost:3000
echo 🔌 API Gateway: http://localhost:8000
echo.
echo 📊 Service Status:
docker-compose -f docker-compose.simple.yml ps
echo.
echo 🔍 To view logs: docker-compose -f docker-compose.simple.yml logs -f
echo 🛑 To stop: docker-compose -f docker-compose.simple.yml down
echo.
echo Press any key to open the frontend...
pause >nul
start http://localhost:3000 