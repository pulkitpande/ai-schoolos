#!/bin/bash

# AI SchoolOS Deployment Script
# This script helps deploy the complete AI SchoolOS microservices system

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Function to check if Docker is installed
check_docker() {
    if ! command -v docker &> /dev/null; then
        print_error "Docker is not installed. Please install Docker first."
        exit 1
    fi
    
    if ! command -v docker-compose &> /dev/null; then
        print_error "Docker Compose is not installed. Please install Docker Compose first."
        exit 1
    fi
    
    print_success "Docker and Docker Compose are installed"
}

# Function to check if ports are available
check_ports() {
    local ports=(8000 8001 8002 8003 8004 8005 8006 8007 8008 8009 8010 8011 8012 8013 8014 8015 5432 6379 27017 9000)
    
    for port in "${ports[@]}"; do
        if lsof -Pi :$port -sTCP:LISTEN -t >/dev/null 2>&1; then
            print_warning "Port $port is already in use. Please free up the port or change the configuration."
        fi
    done
}

# Function to create environment file
create_env_file() {
    if [ ! -f .env ]; then
        print_status "Creating .env file with default values..."
        cat > .env << EOF
# Database Configuration
DATABASE_URL=postgresql://postgres:postgres@postgres:5432/schoolos
POSTGRES_DB=schoolos
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres

# Redis Configuration
REDIS_URL=redis://redis:6379

# MongoDB Configuration
MONGODB_URL=mongodb://admin:admin@mongodb:27017
MONGO_INITDB_ROOT_USERNAME=admin
MONGO_INITDB_ROOT_PASSWORD=admin
MONGO_INITDB_DATABASE=schoolos

# MinIO Configuration
MINIO_ROOT_USER=minioadmin
MINIO_ROOT_PASSWORD=minioadmin

# JWT Configuration
JWT_SECRET=your-super-secret-jwt-key-change-in-production

# Logging
LOG_LEVEL=INFO
DEBUG=false

# Service URLs
AUTH_SERVICE_URL=http://auth-service:8001
STUDENT_SERVICE_URL=http://student-service:8002
STAFF_SERVICE_URL=http://staff-service:8003
FEE_SERVICE_URL=http://fee-service:8004
EXAM_SERVICE_URL=http://exam-service:8005
ATTENDANCE_SERVICE_URL=http://attendance-service:8006
HOMEWORK_SERVICE_URL=http://homework-service:8007
TIMETABLE_SERVICE_URL=http://timetable-service:8008
LIBRARY_SERVICE_URL=http://library-service:8009
TRANSPORT_SERVICE_URL=http://transport-service:8010
COMMUNICATION_SERVICE_URL=http://communication-service:8011
ANALYTICS_SERVICE_URL=http://analytics-service:8012
NOTIFICATION_SERVICE_URL=http://notification-service:8013
CONFIG_SERVICE_URL=http://config-service:8014
SUPER_ADMIN_SERVICE_URL=http://super-admin-service:8015
EOF
        print_success "Created .env file"
    else
        print_status ".env file already exists"
    fi
}

# Function to build and start services
deploy_services() {
    local mode=$1
    
    print_status "Building and starting AI SchoolOS services..."
    
    if [ "$mode" = "production" ]; then
        docker-compose -f docker-compose.prod.yml up -d --build
    else
        docker-compose up -d --build
    fi
    
    print_success "Services started successfully"
}

# Function to wait for services to be ready
wait_for_services() {
    print_status "Waiting for services to be ready..."
    
    # Wait for database
    print_status "Waiting for PostgreSQL..."
    until docker-compose exec -T postgres pg_isready -U postgres -d schoolos; do
        sleep 2
    done
    print_success "PostgreSQL is ready"
    
    # Wait for Redis
    print_status "Waiting for Redis..."
    until docker-compose exec -T redis redis-cli ping; do
        sleep 2
    done
    print_success "Redis is ready"
    
    # Wait for MongoDB
    print_status "Waiting for MongoDB..."
    until docker-compose exec -T mongodb mongosh --eval "db.adminCommand('ping')" > /dev/null 2>&1; do
        sleep 2
    done
    print_success "MongoDB is ready"
    
    # Wait for API Gateway
    print_status "Waiting for API Gateway..."
    until curl -f http://localhost:8000/health > /dev/null 2>&1; do
        sleep 5
    done
    print_success "API Gateway is ready"
}

# Function to check service health
check_service_health() {
    print_status "Checking service health..."
    
    local health_url="http://localhost:8000/services/health"
    local max_attempts=30
    local attempt=1
    
    while [ $attempt -le $max_attempts ]; do
        local response=$(curl -s "$health_url" 2>/dev/null || echo "{}")
        
        if echo "$response" | grep -q "healthy"; then
            print_success "All services are healthy"
            return 0
        fi
        
        print_status "Attempt $attempt/$max_attempts - Waiting for services to be healthy..."
        sleep 10
        ((attempt++))
    done
    
    print_error "Some services are not healthy after $max_attempts attempts"
    print_status "Check service logs with: docker-compose logs"
    return 1
}

# Function to show service status
show_status() {
    print_status "Service Status:"
    echo "=================="
    
    # Show running containers
    docker-compose ps
    
    echo ""
    print_status "Service URLs:"
    echo "================"
    echo "API Gateway: http://localhost:8000"
    echo "API Documentation: http://localhost:8000/docs"
    echo "Service Health: http://localhost:8000/services/health"
    echo ""
    echo "Individual Services:"
    echo "Auth Service: http://localhost:8001"
    echo "Student Service: http://localhost:8002"
    echo "Staff Service: http://localhost:8003"
    echo "Fee Service: http://localhost:8004"
    echo "Exam Service: http://localhost:8005"
    echo "Attendance Service: http://localhost:8006"
    echo "Homework Service: http://localhost:8007"
    echo "Timetable Service: http://localhost:8008"
    echo "Library Service: http://localhost:8009"
    echo "Transport Service: http://localhost:8010"
    echo "Communication Service: http://localhost:8011"
    echo "Analytics Service: http://localhost:8012"
    echo "Notification Service: http://localhost:8013"
    echo "Config Service: http://localhost:8014"
    echo "Super Admin Service: http://localhost:8015"
}

# Function to stop services
stop_services() {
    print_status "Stopping AI SchoolOS services..."
    docker-compose down
    print_success "Services stopped"
}

# Function to restart services
restart_services() {
    print_status "Restarting AI SchoolOS services..."
    docker-compose restart
    print_success "Services restarted"
}

# Function to view logs
view_logs() {
    local service=$1
    
    if [ -z "$service" ]; then
        print_status "Showing logs for all services..."
        docker-compose logs -f
    else
        print_status "Showing logs for $service..."
        docker-compose logs -f "$service"
    fi
}

# Function to clean up
cleanup() {
    print_warning "This will remove all containers, volumes, and networks. Are you sure? (y/N)"
    read -r response
    
    if [[ "$response" =~ ^([yY][eE][sS]|[yY])$ ]]; then
        print_status "Cleaning up AI SchoolOS..."
        docker-compose down -v --remove-orphans
        docker system prune -f
        print_success "Cleanup completed"
    else
        print_status "Cleanup cancelled"
    fi
}

# Function to show help
show_help() {
    echo "AI SchoolOS Deployment Script"
    echo "============================"
    echo ""
    echo "Usage: $0 [COMMAND]"
    echo ""
    echo "Commands:"
    echo "  deploy [mode]     Deploy the system (development/production)"
    echo "  start             Start all services"
    echo "  stop              Stop all services"
    echo "  restart           Restart all services"
    echo "  status            Show service status"
    echo "  health            Check service health"
    echo "  logs [service]    View logs (all services or specific service)"
    echo "  cleanup           Remove all containers and volumes"
    echo "  help              Show this help message"
    echo ""
    echo "Examples:"
    echo "  $0 deploy development"
    echo "  $0 deploy production"
    echo "  $0 logs auth-service"
    echo "  $0 health"
}

# Main script logic
case "${1:-help}" in
    "deploy")
        check_docker
        check_ports
        create_env_file
        deploy_services "${2:-development}"
        wait_for_services
        check_service_health
        show_status
        ;;
    "start")
        check_docker
        deploy_services
        wait_for_services
        show_status
        ;;
    "stop")
        stop_services
        ;;
    "restart")
        restart_services
        wait_for_services
        ;;
    "status")
        show_status
        ;;
    "health")
        check_service_health
        ;;
    "logs")
        view_logs "$2"
        ;;
    "cleanup")
        cleanup
        ;;
    "help"|*)
        show_help
        ;;
esac 