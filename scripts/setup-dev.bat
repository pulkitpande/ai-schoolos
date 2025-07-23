@echo off
REM AI SchoolOS Development Setup Script for Windows

echo 🚀 Setting up AI SchoolOS Development Environment...

REM Check if Docker is running
docker info >nul 2>&1
if errorlevel 1 (
    echo ❌ Docker is not running. Please start Docker Desktop and try again.
    pause
    exit /b 1
)

REM Check if Node.js is installed
node --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Node.js is not installed. Please install Node.js and try again.
    pause
    exit /b 1
)

REM Install root dependencies
echo 📦 Installing root dependencies...
call npm install

REM Install frontend dependencies
echo 📦 Installing frontend dependencies...
cd frontend
call npm install
cd ..

REM Create frontend environment file
echo 🔧 Creating frontend environment configuration...
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

REM Build Docker images
echo 🐳 Building Docker images...
docker-compose build

REM Start backend services
echo 🚀 Starting backend services...
docker-compose up -d

REM Wait for services to be ready
echo ⏳ Waiting for services to be ready...
timeout /t 30 /nobreak >nul

REM Check service health
echo 🔍 Checking service health...
docker-compose ps

echo ✅ Setup complete!
echo.
echo 📋 Available commands:
echo   npm run dev          - Start both frontend and backend
echo   npm run dev:frontend - Start frontend only ^(http://localhost:3000^)
echo   npm run dev:backend  - Start backend services only
echo   npm run docker:up    - Start all Docker services
echo   npm run docker:down  - Stop all Docker services
echo   npm run docker:logs  - View service logs
echo.
echo 🌐 Frontend: http://localhost:3000
echo 🔗 API Gateway: http://localhost:8000
echo 📊 Service Status: docker-compose ps

pause 