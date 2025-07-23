#!/bin/bash

# AI SchoolOS Production Deployment Script
# Perfect for scaling and production use

set -e

echo "🚀 AI SchoolOS Production Deployment"
echo "====================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if running as root (for port 80)
if [ "$EUID" -ne 0 ]; then
    print_warning "Running without sudo. Port 80 may not be accessible."
    print_warning "Consider running with: sudo ./deploy-production.sh"
fi

# Check Docker
print_status "Checking Docker installation..."
if ! command -v docker &> /dev/null; then
    print_error "Docker is not installed. Please install Docker first."
    exit 1
fi

if ! docker info &> /dev/null; then
    print_error "Docker is not running. Please start Docker first."
    exit 1
fi

# Check Docker Compose
print_status "Checking Docker Compose..."
if ! command -v docker-compose &> /dev/null; then
    print_error "Docker Compose is not installed. Please install Docker Compose first."
    exit 1
fi

# Stop any existing containers
print_status "Stopping existing containers..."
docker-compose -f docker-compose.production.yml down --volumes --remove-orphans 2>/dev/null || true

# Clean up old images (optional)
read -p "Do you want to clean up old Docker images? (y/N): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    print_status "Cleaning up old images..."
    docker system prune -f
fi

# Build production images
print_status "Building production images..."
docker-compose -f docker-compose.production.yml build --no-cache

# Start production services
print_status "Starting production services..."
docker-compose -f docker-compose.production.yml up -d

# Wait for services to be ready
print_status "Waiting for services to be ready..."
sleep 30

# Check service health
print_status "Checking service health..."
docker-compose -f docker-compose.production.yml ps

# Test the application
print_status "Testing application endpoints..."

# Test nginx
if curl -f http://localhost/health &> /dev/null; then
    print_status "✅ Nginx is running and healthy"
else
    print_warning "⚠️  Nginx health check failed"
fi

# Test frontend
if curl -f http://localhost &> /dev/null; then
    print_status "✅ Frontend is accessible"
else
    print_warning "⚠️  Frontend is not accessible"
fi

# Test API
if curl -f http://localhost/api/health &> /dev/null; then
    print_status "✅ API Gateway is accessible"
else
    print_warning "⚠️  API Gateway is not accessible"
fi

# Get container logs for debugging
print_status "Recent container logs:"
docker-compose -f docker-compose.production.yml logs --tail=20

echo ""
echo "🎉 Production Deployment Complete!"
echo "================================="
echo ""
echo "📱 Application URLs:"
echo "   Frontend: http://localhost"
echo "   API Health: http://localhost/health"
echo "   API Gateway: http://localhost/api/"
echo "   Auth Service: http://localhost/auth/"
echo "   Student Service: http://localhost/students/"
echo ""
echo "🔧 Management Commands:"
echo "   View logs: docker-compose -f docker-compose.production.yml logs -f"
echo "   Stop services: docker-compose -f docker-compose.production.yml down"
echo "   Restart services: docker-compose -f docker-compose.production.yml restart"
echo "   Update services: docker-compose -f docker-compose.production.yml up -d --build"
echo ""
echo "🌐 For external access:"
echo "   - Configure your domain to point to this server"
echo "   - Set up SSL certificate (recommended for production)"
echo "   - Configure firewall to allow port 80"
echo ""

# Check if running on EC2
if curl -s http://169.254.169.254/latest/meta-data/public-ipv4 &> /dev/null; then
    PUBLIC_IP=$(curl -s http://169.254.169.254/latest/meta-data/public-ipv4)
    echo "🌍 EC2 Public IP: $PUBLIC_IP"
    echo "   External URL: http://$PUBLIC_IP"
    echo ""
    echo "⚠️  Remember to configure EC2 Security Group:"
    echo "   - Allow inbound traffic on port 80 (HTTP)"
    echo "   - Allow inbound traffic on port 443 (HTTPS) if using SSL"
fi

print_status "Deployment completed successfully!" 