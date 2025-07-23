@echo off
echo ========================================
echo AI SchoolOS - START NOW (No Docker)
echo ========================================
echo.

echo [1/3] Creating frontend environment...
if not exist "frontend\.env.local" (
    echo Creating frontend environment configuration...
    (
        echo NEXT_PUBLIC_API_URL=http://localhost:8000
        echo NEXT_PUBLIC_AUTH_SERVICE_URL=http://localhost:8001
        echo NEXT_PUBLIC_STUDENT_SERVICE_URL=http://localhost:8002
        echo NODE_ENV=development
    ) > frontend\.env.local
)

echo [2/3] Using minimal dependencies...
cd frontend
copy package-minimal.json package.json >nul
echo ✓ Using minimal package.json

echo [3/3] Starting frontend development server...
echo.
echo 🚀 Starting AI SchoolOS Frontend...
echo 📱 Frontend will be available at: http://localhost:3000
echo.
echo Press Ctrl+C to stop the server
echo.
npm run dev 