@echo off
echo ========================================
echo AI SchoolOS - NPM Install Fixer
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

REM Check if Node.js is available
node --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Node.js is not installed or not in PATH
    echo Please install Node.js 16+ and try again
    pause
    exit /b 1
)

REM Check if npm is available
npm --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: npm is not installed or not in PATH
    echo Please install npm and try again
    pause
    exit /b 1
)

REM Check if we're in the right directory
if not exist "frontend" (
    echo ERROR: frontend directory not found!
    echo Please run this script from the project root directory
    pause
    exit /b 1
)

echo This script will fix common npm install issues:
echo - Clear npm cache
echo - Remove node_modules and package-lock.json
echo - Try alternative installation methods
echo - Handle infinite hanging issues
echo.
echo Press any key to continue...
pause

REM Run the Python script
python fix-npm-install.py

if errorlevel 1 (
    echo.
    echo An error occurred. Please check the output above.
    pause
    exit /b 1
)

echo.
echo NPM install fix completed!
pause 