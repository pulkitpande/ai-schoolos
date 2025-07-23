@echo off
echo 🚀 Quick Start for AI SchoolOS Frontend

echo Checking if Next.js is available...
npx next --version >nul 2>&1
if %errorlevel% equ 0 (
    echo ✅ Next.js found! Starting development server...
    npx next dev
) else (
    echo ❌ Next.js not found. Installing dependencies...
    echo This may take a few minutes...
    npm install --no-optional --no-audit --silent
    if %errorlevel% equ 0 (
        echo ✅ Installation complete! Starting development server...
        npx next dev
    ) else (
        echo ❌ Installation failed. Please try manually:
        echo cd frontend
        echo npm install
        echo npm run dev
    )
)

pause 