#!/bin/bash

# AI SchoolOS Development Setup Script

echo "🚀 Setting up AI SchoolOS Development Environment..."

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker and try again."
    exit 1
fi

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed. Please install Node.js and try again."
    exit 1
fi

# Install root dependencies
echo "📦 Installing root dependencies..."
npm install

# Install frontend dependencies
echo "📦 Installing frontend dependencies..."
cd frontend
npm install
cd ..

# Create frontend environment file
echo "🔧 Creating frontend environment configuration..."
cat > frontend/.env.local << EOF
# API Gateway
NEXT_PUBLIC_API_URL=http://localhost:8000

# Service URLs
NEXT_PUBLIC_AUTH_SERVICE_URL=http://localhost:8001
NEXT_PUBLIC_STUDENT_SERVICE_URL=http://localhost:8002
NEXT_PUBLIC_STAFF_SERVICE_URL=http://localhost:8003
NEXT_PUBLIC_FEE_SERVICE_URL=http://localhost:8004
NEXT_PUBLIC_HOMEWORK_SERVICE_URL=http://localhost:8005
NEXT_PUBLIC_LIBRARY_SERVICE_URL=http://localhost:8006
NEXT_PUBLIC_EXAM_SERVICE_URL=http://localhost:8007
NEXT_PUBLIC_TIMETABLE_SERVICE_URL=http://localhost:8008
NEXT_PUBLIC_ATTENDANCE_SERVICE_URL=http://localhost:8009
NEXT_PUBLIC_TRANSPORT_SERVICE_URL=http://localhost:8010
NEXT_PUBLIC_COMMUNICATION_SERVICE_URL=http://localhost:8011
NEXT_PUBLIC_ANALYTICS_SERVICE_URL=http://localhost:8012
NEXT_PUBLIC_NOTIFICATION_SERVICE_URL=http://localhost:8013
NEXT_PUBLIC_CONFIG_SERVICE_URL=http://localhost:8014
NEXT_PUBLIC_SUPER_ADMIN_SERVICE_URL=http://localhost:8015
NEXT_PUBLIC_AI_SERVICE_URL=http://localhost:8016
NEXT_PUBLIC_AI_ANALYTICS_SERVICE_URL=http://localhost:8017

# Development settings
NODE_ENV=development
EOF

# Build Docker images
echo "🐳 Building Docker images..."
docker-compose build

# Start backend services
echo "🚀 Starting backend services..."
docker-compose up -d

# Wait for services to be ready
echo "⏳ Waiting for services to be ready..."
sleep 30

# Check service health
echo "🔍 Checking service health..."
docker-compose ps

echo "✅ Setup complete!"
echo ""
echo "📋 Available commands:"
echo "  npm run dev          - Start both frontend and backend"
echo "  npm run dev:frontend - Start frontend only (http://localhost:3000)"
echo "  npm run dev:backend  - Start backend services only"
echo "  npm run docker:up    - Start all Docker services"
echo "  npm run docker:down  - Stop all Docker services"
echo "  npm run docker:logs  - View service logs"
echo ""
echo "🌐 Frontend: http://localhost:3000"
echo "🔗 API Gateway: http://localhost:8000"
echo "📊 Service Status: docker-compose ps" 