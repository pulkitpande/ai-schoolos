@echo off
echo 🚀 Starting AI SchoolOS Development Environment...

echo 📦 Starting backend services...
docker-compose up -d

echo ⏳ Waiting for backend services to start...
timeout /t 10 /nobreak >nul

echo 🌐 Starting frontend development server...
cd frontend
start "Frontend Dev Server" cmd /k "npm run dev"

echo ✅ Development environment started!
echo.
echo 🌐 Frontend: http://localhost:3000
echo 🔗 API Gateway: http://localhost:8000
echo.
echo Press any key to stop all services...
pause

echo 🛑 Stopping services...
docker-compose down
echo ✅ All services stopped. 