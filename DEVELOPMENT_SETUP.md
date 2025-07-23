# AI SchoolOS Development Setup Guide

## 🚀 Quick Start

### Prerequisites
- **Docker Desktop** - [Download here](https://www.docker.com/products/docker-desktop/)
- **Node.js** (v18 or higher) - [Download here](https://nodejs.org/)
- **Git** - [Download here](https://git-scm.com/)

### Automatic Setup (Recommended)

#### Windows
```bash
# Run the Windows setup script
scripts\setup-dev.bat
```

#### Linux/macOS
```bash
# Make the script executable and run it
chmod +x scripts/setup-dev.sh
./scripts/setup-dev.sh
```

### Manual Setup

1. **Install Dependencies**
   ```bash
   # Install root dependencies
   npm install
   
   # Install frontend dependencies
   cd frontend
   npm install
   cd ..
   ```

2. **Create Environment Configuration**
   ```bash
   # Create frontend environment file
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
   ```

3. **Start Backend Services**
   ```bash
   # Build and start all backend services
   docker-compose up -d
   
   # Check service status
   docker-compose ps
   ```

4. **Start Frontend Development Server**
   ```bash
   # Start frontend (in a new terminal)
   npm run dev:frontend
   # OR
   cd frontend && npm run dev
   ```

## 📋 Available Commands

### Root Directory Commands
```bash
npm run dev              # Start both frontend and backend
npm run dev:frontend     # Start frontend only
npm run dev:backend      # Start backend services only
npm run docker:up        # Start all Docker services
npm run docker:down      # Stop all Docker services
npm run docker:build     # Build all Docker images
npm run docker:logs      # View service logs
npm run install:all      # Install all dependencies
npm run clean            # Clean up Docker volumes and node_modules
```

### Frontend Directory Commands
```bash
cd frontend
npm run dev              # Start development server
npm run build            # Build for production
npm run start            # Start production server
npm run lint             # Run ESLint
npm run type-check       # Run TypeScript type checking
```

## 🌐 Service URLs

| Service | URL | Port |
|---------|-----|------|
| **Frontend** | http://localhost:3000 | 3000 |
| **API Gateway** | http://localhost:8000 | 8000 |
| **Auth Service** | http://localhost:8001 | 8001 |
| **Student Service** | http://localhost:8002 | 8002 |
| **Staff Service** | http://localhost:8003 | 8003 |
| **Fee Service** | http://localhost:8004 | 8004 |
| **Homework Service** | http://localhost:8005 | 8005 |
| **Library Service** | http://localhost:8006 | 8006 |
| **Exam Service** | http://localhost:8007 | 8007 |
| **Timetable Service** | http://localhost:8008 | 8008 |
| **Attendance Service** | http://localhost:8009 | 8009 |
| **Transport Service** | http://localhost:8010 | 8010 |
| **Communication Service** | http://localhost:8011 | 8011 |
| **Analytics Service** | http://localhost:8012 | 8012 |
| **Notification Service** | http://localhost:8013 | 8013 |
| **Config Service** | http://localhost:8014 | 8014 |
| **Super Admin Service** | http://localhost:8015 | 8015 |
| **AI Service** | http://localhost:8016 | 8016 |
| **AI Analytics Service** | http://localhost:8017 | 8017 |

## 🗄️ Database Services

| Service | URL | Port |
|---------|-----|------|
| **PostgreSQL** | localhost:5432 | 5432 |
| **Redis** | localhost:6379 | 6379 |
| **MongoDB** | localhost:27017 | 27017 |
| **MinIO** | localhost:9000 | 9000 |

## 🔧 Troubleshooting

### Common Issues

1. **Port Already in Use**
   ```bash
   # Check what's using the port
   netstat -ano | findstr :3000
   
   # Kill the process
   taskkill /PID <PID> /F
   ```

2. **Docker Services Not Starting**
   ```bash
   # Check Docker logs
   docker-compose logs
   
   # Restart Docker Desktop
   # Then try again
   docker-compose up -d
   ```

3. **Frontend Can't Connect to Backend**
   - Ensure backend services are running: `docker-compose ps`
   - Check if `.env.local` file exists in frontend directory
   - Verify service URLs in the environment file

4. **Node Modules Issues**
   ```bash
   # Clean and reinstall
   rm -rf node_modules package-lock.json
   npm install
   ```

### Service Health Checks

```bash
# Check all service status
docker-compose ps

# Check specific service logs
docker-compose logs api-gateway
docker-compose logs auth-service
docker-compose logs frontend

# Check service health endpoints
curl http://localhost:8000/health
curl http://localhost:8001/health
```

## 🏗️ Architecture Overview

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │   API Gateway   │    │   Microservices │
│   (Next.js)     │◄──►│   (FastAPI)     │◄──►│   (FastAPI)     │
│   Port: 3000    │    │   Port: 8000    │    │   Ports: 8001+  │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                              │
                              ▼
                       ┌─────────────────┐
                       │   Databases     │
                       │   PostgreSQL    │
                       │   Redis         │
                       │   MongoDB       │
                       │   MinIO         │
                       └─────────────────┘
```

## 📝 Development Workflow

1. **Start Development Environment**
   ```bash
   npm run dev
   ```

2. **Make Changes**
   - Frontend changes auto-reload
   - Backend changes require service restart

3. **Test Changes**
   - Frontend: http://localhost:3000
   - API Gateway: http://localhost:8000/docs

4. **Stop Development**
   ```bash
   npm run docker:down
   ```

## 🚀 Production Deployment

For production deployment, see the main README.md file for detailed instructions.

## 📞 Support

If you encounter issues:
1. Check the troubleshooting section above
2. Review service logs: `docker-compose logs`
3. Ensure all prerequisites are installed
4. Try the automatic setup script first 