@echo off
echo ========================================
echo AI SchoolOS - EC2 + Nginx Configuration
echo ========================================
echo.

echo This script will create the environment configuration for EC2 with Nginx routing.
echo With Nginx, all API calls go through port 80/443, not individual service ports.
echo.

set /p EC2_IP="Enter your EC2 instance public IP address: "
set /p EC2_PORT="Enter your Nginx port (default: 80): "

if "%EC2_PORT%"=="" set EC2_PORT=80

echo.
echo Creating production environment configuration for EC2 + Nginx...
echo EC2 IP: %EC2_IP%
echo Nginx Port: %EC2_PORT%
echo.

REM Create production environment file
(
echo # Production Environment Configuration for EC2 + Nginx
echo # Generated on: %date% %time%
echo.
echo # API Gateway - EC2 + Nginx Configuration
echo # All API calls go through Nginx on port %EC2_PORT%
echo NEXT_PUBLIC_API_URL=http://%EC2_IP%:%EC2_PORT%
echo.
echo # Service URLs - All routed through Nginx
echo # Nginx routes /api/* to API Gateway, /auth/* to Auth Service, etc.
echo NEXT_PUBLIC_AUTH_SERVICE_URL=http://%EC2_IP%:%EC2_PORT%
echo NEXT_PUBLIC_STUDENT_SERVICE_URL=http://%EC2_IP%:%EC2_PORT%
echo NEXT_PUBLIC_STAFF_SERVICE_URL=http://%EC2_IP%:%EC2_PORT%
echo NEXT_PUBLIC_FEE_SERVICE_URL=http://%EC2_IP%:%EC2_PORT%
echo NEXT_PUBLIC_HOMEWORK_SERVICE_URL=http://%EC2_IP%:%EC2_PORT%
echo NEXT_PUBLIC_LIBRARY_SERVICE_URL=http://%EC2_IP%:%EC2_PORT%
echo NEXT_PUBLIC_EXAM_SERVICE_URL=http://%EC2_IP%:%EC2_PORT%
echo NEXT_PUBLIC_TIMETABLE_SERVICE_URL=http://%EC2_IP%:%EC2_PORT%
echo NEXT_PUBLIC_ATTENDANCE_SERVICE_URL=http://%EC2_IP%:%EC2_PORT%
echo NEXT_PUBLIC_TRANSPORT_SERVICE_URL=http://%EC2_IP%:%EC2_PORT%
echo NEXT_PUBLIC_COMMUNICATION_SERVICE_URL=http://%EC2_IP%:%EC2_PORT%
echo NEXT_PUBLIC_ANALYTICS_SERVICE_URL=http://%EC2_IP%:%EC2_PORT%
echo NEXT_PUBLIC_NOTIFICATION_SERVICE_URL=http://%EC2_IP%:%EC2_PORT%
echo NEXT_PUBLIC_CONFIG_SERVICE_URL=http://%EC2_IP%:%EC2_PORT%
echo NEXT_PUBLIC_SUPER_ADMIN_SERVICE_URL=http://%EC2_IP%:%EC2_PORT%
echo NEXT_PUBLIC_AI_SERVICE_URL=http://%EC2_IP%:%EC2_PORT%
echo NEXT_PUBLIC_AI_ANALYTICS_SERVICE_URL=http://%EC2_IP%:%EC2_PORT%
echo.
echo # Production settings
echo NODE_ENV=production
) > frontend\.env.production

echo ✓ Production environment file created: frontend\.env.production
echo.
echo Nginx Routing Configuration:
echo - Frontend: http://%EC2_IP%:%EC2_PORT%/
echo - API Gateway: http://%EC2_IP%:%EC2_PORT%/api/
echo - Auth Service: http://%EC2_IP%:%EC2_PORT%/auth/
echo - Student Service: http://%EC2_IP%:%EC2_PORT%/students/
echo.
echo Next steps:
echo 1. Commit this file to your repository: git add frontend\.env.production
echo 2. Push to GitHub: git push origin main
echo 3. Pull on your EC2 instance: git pull origin main
echo 4. Rebuild and deploy your frontend
echo.
echo Note: Only port %EC2_PORT% needs to be open in EC2 security groups!
echo.
pause 