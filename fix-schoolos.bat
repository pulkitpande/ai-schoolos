@echo off
echo ========================================
echo AI SchoolOS - Complete Fix Script
echo ========================================
echo.

echo [1/8] Checking Docker Desktop status...
docker --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Docker is not running or not installed!
    echo Please start Docker Desktop and run this script again.
    pause
    exit /b 1
)

echo [2/8] Creating frontend environment file...
if not exist "frontend\.env.local" (
    echo Creating frontend environment configuration...
    (
        echo # API Gateway
        echo NEXT_PUBLIC_API_URL=http://localhost:8000
        echo.
        echo # Service URLs
        echo NEXT_PUBLIC_AUTH_SERVICE_URL=http://localhost:8001
        echo NEXT_PUBLIC_STUDENT_SERVICE_URL=http://localhost:8002
        echo NEXT_PUBLIC_STAFF_SERVICE_URL=http://localhost:8003
        echo NEXT_PUBLIC_FEE_SERVICE_URL=http://localhost:8004
        echo NEXT_PUBLIC_HOMEWORK_SERVICE_URL=http://localhost:8005
        echo NEXT_PUBLIC_LIBRARY_SERVICE_URL=http://localhost:8006
        echo NEXT_PUBLIC_EXAM_SERVICE_URL=http://localhost:8007
        echo NEXT_PUBLIC_TIMETABLE_SERVICE_URL=http://localhost:8008
        echo NEXT_PUBLIC_ATTENDANCE_SERVICE_URL=http://localhost:8009
        echo NEXT_PUBLIC_TRANSPORT_SERVICE_URL=http://localhost:8010
        echo NEXT_PUBLIC_COMMUNICATION_SERVICE_URL=http://localhost:8011
        echo NEXT_PUBLIC_ANALYTICS_SERVICE_URL=http://localhost:8012
        echo NEXT_PUBLIC_NOTIFICATION_SERVICE_URL=http://localhost:8013
        echo NEXT_PUBLIC_CONFIG_SERVICE_URL=http://localhost:8014
        echo NEXT_PUBLIC_SUPER_ADMIN_SERVICE_URL=http://localhost:8015
        echo NEXT_PUBLIC_AI_SERVICE_URL=http://localhost:8016
        echo NEXT_PUBLIC_AI_ANALYTICS_SERVICE_URL=http://localhost:8017
        echo.
        echo # Development settings
        echo NODE_ENV=development
    ) > frontend\.env.local
    echo ✓ Frontend environment file created
) else (
    echo ✓ Frontend environment file already exists
)

echo [3/8] Installing frontend dependencies...
cd frontend
call npm install
if %errorlevel% neq 0 (
    echo ERROR: Failed to install frontend dependencies
    pause
    exit /b 1
)
cd ..
echo ✓ Frontend dependencies installed

echo [4/8] Installing root dependencies...
call npm install
if %errorlevel% neq 0 (
    echo ERROR: Failed to install root dependencies
    pause
    exit /b 1
)
echo ✓ Root dependencies installed

echo [5/8] Stopping any existing containers...
docker-compose down --volumes --remove-orphans
echo ✓ Existing containers stopped

echo [6/8] Building Docker images...
docker-compose build --no-cache
if %errorlevel% neq 0 (
    echo ERROR: Docker build failed
    echo Check the error messages above and fix any issues
    pause
    exit /b 1
)
echo ✓ Docker images built successfully

echo [7/8] Starting all services...
docker-compose up -d
if %errorlevel% neq 0 (
    echo ERROR: Failed to start services
    echo Check Docker logs: docker-compose logs
    pause
    exit /b 1
)
echo ✓ All services started

echo [8/8] Waiting for services to be ready...
timeout /t 30 /nobreak >nul

echo.
echo ========================================
echo 🎉 AI SchoolOS is now running!
echo ========================================
echo.
echo 📱 Frontend: http://localhost:3000
echo 🔌 API Gateway: http://localhost:8000
echo.
echo 📊 Service Status:
docker-compose ps
echo.
echo 🔍 To view logs: docker-compose logs -f
echo 🛑 To stop: docker-compose down
echo.
echo Press any key to open the frontend...
pause >nul
start http://localhost:3000 