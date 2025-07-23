@echo off
REM AI SchoolOS Deployment Script for Windows
REM This script helps deploy the complete AI SchoolOS microservices system

setlocal enabledelayedexpansion

REM Colors for output (Windows doesn't support ANSI colors in batch)
set "RED=[ERROR]"
set "GREEN=[SUCCESS]"
set "YELLOW=[WARNING]"
set "BLUE=[INFO]"

REM Function to print colored output
:print_status
echo %BLUE% %~1
goto :eof

:print_success
echo %GREEN% %~1
goto :eof

:print_warning
echo %YELLOW% %~1
goto :eof

:print_error
echo %RED% %~1
goto :eof

REM Function to check if Docker is installed
:check_docker
docker --version >nul 2>&1
if errorlevel 1 (
    call :print_error "Docker is not installed. Please install Docker Desktop first."
    exit /b 1
)

docker-compose --version >nul 2>&1
if errorlevel 1 (
    call :print_error "Docker Compose is not installed. Please install Docker Compose first."
    exit /b 1
)

call :print_success "Docker and Docker Compose are installed"
goto :eof

REM Function to check if ports are available
:check_ports
set "ports=8000 8001 8002 8003 8004 8005 8006 8007 8008 8009 8010 8011 8012 8013 8014 8015 5432 6379 27017 9000"
for %%p in (%ports%) do (
    netstat -an | find "%%p" | find "LISTENING" >nul
    if not errorlevel 1 (
        call :print_warning "Port %%p is already in use. Please free up the port or change the configuration."
    )
)
goto :eof

REM Function to create environment file
:create_env_file
if not exist .env (
    call :print_status "Creating .env file with default values..."
    (
        echo # Database Configuration
        echo DATABASE_URL=postgresql://postgres:postgres@postgres:5432/schoolos
        echo POSTGRES_DB=schoolos
        echo POSTGRES_USER=postgres
        echo POSTGRES_PASSWORD=postgres
        echo.
        echo # Redis Configuration
        echo REDIS_URL=redis://redis:6379
        echo.
        echo # MongoDB Configuration
        echo MONGODB_URL=mongodb://admin:admin@mongodb:27017
        echo MONGO_INITDB_ROOT_USERNAME=admin
        echo MONGO_INITDB_ROOT_PASSWORD=admin
        echo MONGO_INITDB_DATABASE=schoolos
        echo.
        echo # MinIO Configuration
        echo MINIO_ROOT_USER=minioadmin
        echo MINIO_ROOT_PASSWORD=minioadmin
        echo.
        echo # JWT Configuration
        echo JWT_SECRET=your-super-secret-jwt-key-change-in-production
        echo.
        echo # Logging
        echo LOG_LEVEL=INFO
        echo DEBUG=false
        echo.
        echo # Service URLs
        echo AUTH_SERVICE_URL=http://auth-service:8001
        echo STUDENT_SERVICE_URL=http://student-service:8002
        echo STAFF_SERVICE_URL=http://staff-service:8003
        echo FEE_SERVICE_URL=http://fee-service:8004
        echo EXAM_SERVICE_URL=http://exam-service:8005
        echo ATTENDANCE_SERVICE_URL=http://attendance-service:8006
        echo HOMEWORK_SERVICE_URL=http://homework-service:8007
        echo TIMETABLE_SERVICE_URL=http://timetable-service:8008
        echo LIBRARY_SERVICE_URL=http://library-service:8009
        echo TRANSPORT_SERVICE_URL=http://transport-service:8010
        echo COMMUNICATION_SERVICE_URL=http://communication-service:8011
        echo ANALYTICS_SERVICE_URL=http://analytics-service:8012
        echo NOTIFICATION_SERVICE_URL=http://notification-service:8013
        echo CONFIG_SERVICE_URL=http://config-service:8014
        echo SUPER_ADMIN_SERVICE_URL=http://super-admin-service:8015
    ) > .env
    call :print_success "Created .env file"
) else (
    call :print_status ".env file already exists"
)
goto :eof

REM Function to build and start services
:deploy_services
set "mode=%~1"
if "%mode%"=="" set "mode=development"

call :print_status "Building and starting AI SchoolOS services..."

if "%mode%"=="production" (
    docker-compose -f docker-compose.prod.yml up -d --build
) else (
    docker-compose up -d --build
)

if errorlevel 1 (
    call :print_error "Failed to start services"
    exit /b 1
)

call :print_success "Services started successfully"
goto :eof

REM Function to wait for services to be ready
:wait_for_services
call :print_status "Waiting for services to be ready..."

REM Wait for database
call :print_status "Waiting for PostgreSQL..."
:wait_postgres
docker-compose exec -T postgres pg_isready -U postgres -d schoolos >nul 2>&1
if errorlevel 1 (
    timeout /t 2 /nobreak >nul
    goto wait_postgres
)
call :print_success "PostgreSQL is ready"

REM Wait for Redis
call :print_status "Waiting for Redis..."
:wait_redis
docker-compose exec -T redis redis-cli ping >nul 2>&1
if errorlevel 1 (
    timeout /t 2 /nobreak >nul
    goto wait_redis
)
call :print_success "Redis is ready"

REM Wait for MongoDB
call :print_status "Waiting for MongoDB..."
:wait_mongodb
docker-compose exec -T mongodb mongosh --eval "db.adminCommand('ping')" >nul 2>&1
if errorlevel 1 (
    timeout /t 2 /nobreak >nul
    goto wait_mongodb
)
call :print_success "MongoDB is ready"

REM Wait for API Gateway
call :print_status "Waiting for API Gateway..."
:wait_gateway
curl -f http://localhost:8000/health >nul 2>&1
if errorlevel 1 (
    timeout /t 5 /nobreak >nul
    goto wait_gateway
)
call :print_success "API Gateway is ready"
goto :eof

REM Function to check service health
:check_service_health
call :print_status "Checking service health..."

set "health_url=http://localhost:8000/services/health"
set "max_attempts=30"
set "attempt=1"

:health_check_loop
curl -s "%health_url%" 2>nul | find "healthy" >nul
if not errorlevel 1 (
    call :print_success "All services are healthy"
    goto :eof
)

call :print_status "Attempt %attempt%/%max_attempts% - Waiting for services to be healthy..."
timeout /t 10 /nobreak >nul
set /a attempt+=1
if %attempt% leq %max_attempts% goto health_check_loop

call :print_error "Some services are not healthy after %max_attempts% attempts"
call :print_status "Check service logs with: docker-compose logs"
exit /b 1

REM Function to show service status
:show_status
call :print_status "Service Status:"
echo ==================

REM Show running containers
docker-compose ps

echo.
call :print_status "Service URLs:"
echo ================
echo API Gateway: http://localhost:8000
echo API Documentation: http://localhost:8000/docs
echo Service Health: http://localhost:8000/services/health
echo.
echo Individual Services:
echo Auth Service: http://localhost:8001
echo Student Service: http://localhost:8002
echo Staff Service: http://localhost:8003
echo Fee Service: http://localhost:8004
echo Exam Service: http://localhost:8005
echo Attendance Service: http://localhost:8006
echo Homework Service: http://localhost:8007
echo Timetable Service: http://localhost:8008
echo Library Service: http://localhost:8009
echo Transport Service: http://localhost:8010
echo Communication Service: http://localhost:8011
echo Analytics Service: http://localhost:8012
echo Notification Service: http://localhost:8013
echo Config Service: http://localhost:8014
echo Super Admin Service: http://localhost:8015
goto :eof

REM Function to stop services
:stop_services
call :print_status "Stopping AI SchoolOS services..."
docker-compose down
call :print_success "Services stopped"
goto :eof

REM Function to restart services
:restart_services
call :print_status "Restarting AI SchoolOS services..."
docker-compose restart
call :print_success "Services restarted"
goto :eof

REM Function to view logs
:view_logs
set "service=%~1"
if "%service%"=="" (
    call :print_status "Showing logs for all services..."
    docker-compose logs -f
) else (
    call :print_status "Showing logs for %service%..."
    docker-compose logs -f "%service%"
)
goto :eof

REM Function to clean up
:cleanup
call :print_warning "This will remove all containers, volumes, and networks. Are you sure? (y/N)"
set /p "response="
if /i "%response%"=="y" (
    call :print_status "Cleaning up AI SchoolOS..."
    docker-compose down -v --remove-orphans
    docker system prune -f
    call :print_success "Cleanup completed"
) else (
    call :print_status "Cleanup cancelled"
)
goto :eof

REM Function to show help
:show_help
echo AI SchoolOS Deployment Script for Windows
echo ========================================
echo.
echo Usage: %0 [COMMAND]
echo.
echo Commands:
echo   deploy [mode]     Deploy the system (development/production)
echo   start             Start all services
echo   stop              Stop all services
echo   restart           Restart all services
echo   status            Show service status
echo   health            Check service health
echo   logs [service]    View logs (all services or specific service)
echo   cleanup           Remove all containers and volumes
echo   help              Show this help message
echo.
echo Examples:
echo   %0 deploy development
echo   %0 deploy production
echo   %0 logs auth-service
echo   %0 health
goto :eof

REM Main script logic
set "command=%~1"
if "%command%"=="" set "command=help"

if "%command%"=="deploy" (
    call :check_docker
    call :check_ports
    call :create_env_file
    call :deploy_services "%~2"
    call :wait_for_services
    call :check_service_health
    call :show_status
) else if "%command%"=="start" (
    call :check_docker
    call :deploy_services
    call :wait_for_services
    call :show_status
) else if "%command%"=="stop" (
    call :stop_services
) else if "%command%"=="restart" (
    call :restart_services
    call :wait_for_services
) else if "%command%"=="status" (
    call :show_status
) else if "%command%"=="health" (
    call :check_service_health
) else if "%command%"=="logs" (
    call :view_logs "%~2"
) else if "%command%"=="cleanup" (
    call :cleanup
) else (
    call :show_help
)

endlocal 