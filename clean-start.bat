@echo off
echo 🧹 COMPLETE CLEANUP AND OPTIMIZED START
echo ========================================

echo.
echo 🗑️  Stopping all containers...
docker-compose down -v

echo.
echo 🧹 Cleaning Docker system...
docker system prune -a --volumes --force

echo.
echo 📁 Removing local node_modules and build files...
if exist "frontend\node_modules" rmdir /s /q "frontend\node_modules"
if exist "frontend\.next" rmdir /s /q "frontend\.next"
if exist "frontend\package-lock.json" del "frontend\package-lock.json"

echo.
echo 🔧 Generating optimized Dockerfiles...
python scripts\generate-optimized-dockerfiles.py

echo.
echo 🐳 Building optimized containers (no local storage)...
docker-compose -f docker-compose.optimized.yml build --no-cache

echo.
echo 🚀 Starting optimized services...
docker-compose -f docker-compose.optimized.yml up -d

echo.
echo ⏳ Waiting for services to start...
timeout /t 30 /nobreak >nul

echo.
echo 📊 Checking service status...
docker-compose -f docker-compose.optimized.yml ps

echo.
echo ✅ OPTIMIZED SETUP COMPLETE!
echo.
echo 🌐 Frontend: http://localhost:3000
echo 🔗 API Gateway: http://localhost:8000
echo 📊 Service Status: docker-compose -f docker-compose.optimized.yml ps
echo.
echo 💡 All data is ephemeral - containers restart fresh each time
echo 💡 No local storage used - everything runs in containers
echo 💡 Optimized builds - minimal image sizes

pause 