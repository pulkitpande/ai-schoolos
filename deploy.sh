#!/bin/bash

# AI SchoolOS Deployment Script for EC2
# This script sets up the complete AI SchoolOS application on an EC2 instance

set -e  # Exit on any error

echo "🚀 Starting AI SchoolOS Deployment..."

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

# Check if running as root
if [ "$EUID" -eq 0 ]; then
    print_error "Please don't run this script as root. Use a regular user with sudo privileges."
    exit 1
fi

# Update system
print_status "Updating system packages..."
sudo apt update && sudo apt upgrade -y

# Install essential packages
print_status "Installing essential packages..."
sudo apt install -y curl wget git unzip software-properties-common apt-transport-https ca-certificates gnupg lsb-release

# Install Docker
print_status "Installing Docker..."
if ! command -v docker &> /dev/null; then
    curl -fsSL https://get.docker.com -o get-docker.sh
    sudo sh get-docker.sh
    sudo usermod -aG docker $USER
    print_success "Docker installed successfully"
else
    print_warning "Docker is already installed"
fi

# Install Docker Compose
print_status "Installing Docker Compose..."
if ! command -v docker-compose &> /dev/null; then
    sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
    sudo chmod +x /usr/local/bin/docker-compose
    print_success "Docker Compose installed successfully"
else
    print_warning "Docker Compose is already installed"
fi

# Start Docker service
print_status "Starting Docker service..."
sudo systemctl start docker
sudo systemctl enable docker

# Create application directory
print_status "Setting up application directory..."
APP_DIR="/opt/ai-schoolos"
sudo mkdir -p $APP_DIR
sudo chown $USER:$USER $APP_DIR

# Clone repository (if not already present)
if [ ! -d "$APP_DIR/.git" ]; then
    print_status "Cloning AI SchoolOS repository..."
    cd $APP_DIR
    # Note: Replace with your actual repository URL
    git clone https://github.com/pulkitpande/ai-schoolos.git .
else
    print_warning "Repository already exists, pulling latest changes..."
    cd $APP_DIR
    git pull origin master
fi

# Set proper permissions
print_status "Setting proper permissions..."
sudo chown -R $USER:$USER $APP_DIR

# Create environment files
print_status "Creating environment files..."
cat > $APP_DIR/.env << EOF
# Database Configuration
DATABASE_URL=postgresql://schoolos:schoolos123@postgres:5432/schoolos
REDIS_URL=redis://redis:6379

# JWT Configuration
JWT_SECRET=your-super-secret-jwt-key-change-this-in-production
JWT_ALGORITHM=HS256
JWT_EXPIRATION=3600

# API Configuration
API_HOST=0.0.0.0
API_PORT=8000

# Environment
ENVIRONMENT=production
DEBUG=false

# CORS
ALLOWED_ORIGINS=http://localhost:3000,http://your-domain.com
EOF

# Create frontend environment
cat > $APP_DIR/frontend/.env.local << EOF
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_APP_NAME=AI SchoolOS
NEXT_PUBLIC_APP_VERSION=1.0.0
EOF

# Build and start services
print_status "Building and starting services..."
cd $APP_DIR

# Clean up any existing containers
docker-compose -f docker-compose.simple.yml down --remove-orphans

# Remove old images to save space
docker system prune -f

# Build and start services
docker-compose -f docker-compose.simple.yml up -d --build

# Wait for services to be ready
print_status "Waiting for services to be ready..."
sleep 30

# Check service status
print_status "Checking service status..."
docker-compose -f docker-compose.simple.yml ps

# Check if services are healthy
print_status "Checking service health..."
for service in frontend api-gateway auth-service student-service; do
    if docker-compose -f docker-compose.simple.yml ps $service | grep -q "Up"; then
        print_success "$service is running"
    else
        print_error "$service failed to start"
    fi
done

# Create systemd service for auto-start
print_status "Creating systemd service for auto-start..."
sudo tee /etc/systemd/system/ai-schoolos.service > /dev/null << EOF
[Unit]
Description=AI SchoolOS Application
Requires=docker.service
After=docker.service

[Service]
Type=oneshot
RemainAfterExit=yes
WorkingDirectory=$APP_DIR
ExecStart=/usr/local/bin/docker-compose -f docker-compose.simple.yml up -d
ExecStop=/usr/local/bin/docker-compose -f docker-compose.simple.yml down
TimeoutStartSec=0

[Install]
WantedBy=multi-user.target
EOF

# Enable and start the service
sudo systemctl enable ai-schoolos.service
sudo systemctl start ai-schoolos.service

# Create monitoring script
print_status "Creating monitoring script..."
cat > $APP_DIR/monitor.sh << 'EOF'
#!/bin/bash
echo "=== AI SchoolOS Service Status ==="
docker-compose -f docker-compose.simple.yml ps
echo ""
echo "=== System Resources ==="
echo "Memory Usage:"
free -h
echo ""
echo "Disk Usage:"
df -h
echo ""
echo "Docker Disk Usage:"
docker system df
EOF

chmod +x $APP_DIR/monitor.sh

# Create update script
print_status "Creating update script..."
cat > $APP_DIR/update.sh << 'EOF'
#!/bin/bash
cd /opt/ai-schoolos
git pull origin master
docker-compose -f docker-compose.simple.yml down
docker-compose -f docker-compose.simple.yml up -d --build
echo "Update completed!"
EOF

chmod +x $APP_DIR/update.sh

# Print final information
print_success "🎉 AI SchoolOS deployment completed!"
echo ""
echo "📋 Application Information:"
echo "   Frontend: http://$(curl -s http://169.254.169.254/latest/meta-data/public-ipv4):3000"
echo "   API Gateway: http://$(curl -s http://169.254.169.254/latest/meta-data/public-ipv4):8000"
echo "   Auth Service: http://$(curl -s http://169.254.169.254/latest/meta-data/public-ipv4):8001"
echo "   Student Service: http://$(curl -s http://169.254.169.254/latest/meta-data/public-ipv4):8002"
echo ""
echo "🔧 Management Commands:"
echo "   Monitor services: $APP_DIR/monitor.sh"
echo "   Update application: $APP_DIR/update.sh"
echo "   View logs: docker-compose -f docker-compose.simple.yml logs"
echo "   Restart services: sudo systemctl restart ai-schoolos"
echo ""
echo "⚠️  Important:"
echo "   - Update your security group to allow ports 3000, 8000, 8001, 8002"
echo "   - Change default passwords in production"
echo "   - Set up SSL certificates for production use"
echo ""
print_success "Deployment completed successfully! 🚀" 