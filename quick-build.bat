@echo off
echo 🚀 Quick Build - Building Services Individually
echo ===============================================

echo.
echo 🗑️  Cleaning up...
docker-compose -f docker-compose.simple.yml down -v
docker system prune -f

echo.
echo 📦 Starting infrastructure services (no build required)...
docker-compose -f docker-compose.simple.yml up -d postgres redis mongodb minio

echo.
echo ⏳ Waiting for infrastructure to be ready...
timeout /t 10 /nobreak >nul

echo.
echo 🔧 Building API Gateway...
docker-compose -f docker-compose.simple.yml build api-gateway
if %errorlevel% neq 0 (
    echo ❌ API Gateway build failed
    pause
    exit /b 1
)

echo.
echo 🔧 Building Auth Service...
docker-compose -f docker-compose.simple.yml build auth-service
if %errorlevel% neq 0 (
    echo ❌ Auth Service build failed
    pause
    exit /b 1
)

echo.
echo 🔧 Building Student Service...
docker-compose -f docker-compose.simple.yml build student-service
if %errorlevel% neq 0 (
    echo ❌ Student Service build failed
    pause
    exit /b 1
)

echo.
echo 🔧 Building Frontend...
docker-compose -f docker-compose.simple.yml build frontend
if %errorlevel% neq 0 (
    echo ❌ Frontend build failed
    pause
    exit /b 1
)

echo.
echo 🚀 Starting all services...
docker-compose -f docker-compose.simple.yml up -d

echo.
echo ⏳ Waiting for services to start...
timeout /t 30 /nobreak >nul

echo.
echo 📊 Checking service status...
docker-compose -f docker-compose.simple.yml ps

echo.
echo ✅ BUILD COMPLETE!
echo.
echo 🌐 Frontend: http://localhost:3000
echo 🔗 API Gateway: http://localhost:8000
echo 📚 API Documentation: http://localhost:8000/docs
echo.
echo 💡 Services are now running with simple configuration
echo 💡 No complex multi-stage builds that can hang

pause 