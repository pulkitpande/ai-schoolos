# AI SchoolOS - Docker Deployment Guide

## 🐳 Complete Docker Solution

This guide provides a comprehensive Docker solution that addresses npm install issues and ensures production-ready deployment of the AI SchoolOS application.

## 🎯 Benefits of Docker Solution

### ✅ **Solves npm Install Issues**
- **Consistent Environment**: Same environment across development and production
- **No Local Dependencies**: No need to install Node.js, npm, or Python locally
- **Isolated Containers**: Each service runs in its own container
- **Reproducible Builds**: Same result every time

### ✅ **Production Ready**
- **Multi-stage Builds**: Optimized images for production
- **Health Checks**: Automatic monitoring of service health
- **Resource Management**: Proper resource allocation and limits
- **Security**: Non-root users and minimal attack surface

### ✅ **Development Friendly**
- **Hot Reloading**: Code changes reflect immediately
- **Volume Mounting**: Local development with containerized services
- **Easy Debugging**: Access to logs and container shells
- **Fast Iteration**: Quick rebuild and restart cycles

## 📁 File Structure

```
ai-schoolos/
├── frontend/
│   ├── Dockerfile.production      # Production frontend image
│   ├── Dockerfile.development     # Development frontend image
│   └── package.json
├── backend/
│   ├── Dockerfile.api-gateway     # API Gateway image
│   ├── Dockerfile.service         # Generic service image
│   └── services/
│       ├── auth-service/
│       ├── student-service/
│       └── ... (other services)
├── docker-compose.production.yml  # Production stack
├── docker-compose.development.yml # Development stack
├── docker-manager.py              # Docker management script
└── DOCKER_DEPLOYMENT_GUIDE.md    # This documentation
```

## 🚀 Quick Start

### **Option 1: Using Docker Manager Script**
```bash
# Start development environment
python docker-manager.py run --environment development

# Start production environment
python docker-manager.py run --environment production

# Check status
python docker-manager.py status --environment development

# View logs
python docker-manager.py logs --environment development --follow

# Stop services
python docker-manager.py stop --environment development
```

### **Option 2: Direct Docker Compose**
```bash
# Development
docker-compose -f docker-compose.development.yml up -d

# Production
docker-compose -f docker-compose.production.yml up -d

# Check status
docker-compose -f docker-compose.development.yml ps

# View logs
docker-compose -f docker-compose.development.yml logs -f

# Stop services
docker-compose -f docker-compose.development.yml down
```

## 🔧 Docker Manager Commands

### **Build Images**
```bash
# Build all images for development
python docker-manager.py build --environment development

# Build specific services
python docker-manager.py build --environment development --services frontend api-gateway

# Build production images
python docker-manager.py build --environment production
```

### **Start Services**
```bash
# Start all services
python docker-manager.py start --environment development

# Start specific services
python docker-manager.py start --environment development --services frontend auth-service
```

### **Monitor Services**
```bash
# Check service status
python docker-manager.py status --environment development

# View logs
python docker-manager.py logs --environment development

# Follow logs in real-time
python docker-manager.py logs --environment development --follow

# Check service health
python docker-manager.py health --environment development
```

### **Manage Services**
```bash
# Restart all services
python docker-manager.py restart --environment development

# Stop all services
python docker-manager.py stop --environment development

# Clean up resources
python docker-manager.py clean --environment development
```

## 🏗️ Dockerfile Details

### **Frontend Production (`frontend/Dockerfile.production`)**
- **Multi-stage build** for optimized production image
- **Alpine Linux** base for smaller image size
- **Multiple npm install fallbacks** to handle npm issues
- **Non-root user** for security
- **Health checks** for monitoring
- **Standalone output** for Next.js optimization

### **Frontend Development (`frontend/Dockerfile.development`)**
- **Hot reloading** support
- **Volume mounting** for live code changes
- **Development dependencies** included
- **Multiple npm install methods** for reliability

### **Backend API Gateway (`backend/Dockerfile.api-gateway`)**
- **Python 3.11** base image
- **Shared dependencies** installation
- **Non-root user** for security
- **Health checks** for monitoring
- **Optimized for API Gateway** specific needs

### **Backend Services (`backend/Dockerfile.service`)**
- **Generic template** for all microservices
- **Build arguments** for service-specific configuration
- **Shared dependencies** and service-specific dependencies
- **Port configuration** via build arguments
- **Health checks** for each service

## 🌐 Service Ports

| Service | Port | Description |
|---------|------|-------------|
| Frontend | 3000 | Next.js development/production server |
| API Gateway | 8000 | Main API entry point |
| Auth Service | 8001 | Authentication and authorization |
| Student Service | 8002 | Student management |
| Staff Service | 8003 | Staff management |
| AI Service | 8004 | AI/ML functionality |
| Analytics Service | 8005 | Analytics and reporting |
| Notification Service | 8006 | Push notifications |
| Communication Service | 8007 | Messaging and communication |
| Attendance Service | 8008 | Attendance tracking |
| Timetable Service | 8009 | Schedule management |
| Exam Service | 8010 | Exam management |
| Library Service | 8011 | Library management |
| Homework Service | 8012 | Homework tracking |
| Fee Service | 8013 | Fee management |
| Transport Service | 8014 | Transport tracking |
| Config Service | 8015 | Configuration management |
| Super Admin Service | 8016 | Super admin functionality |

## 🔍 Health Checks

All services include health checks that:
- **Monitor service availability** every 30 seconds
- **Check HTTP endpoints** for service health
- **Retry failed checks** up to 3 times
- **Start monitoring** after 5 seconds of startup
- **Timeout** after 3 seconds per check

### **Health Check Endpoints**
- Frontend: `http://localhost:3000/api/health`
- API Gateway: `http://localhost:8000/health`
- All Services: `http://localhost:{PORT}/health`

## 🛠️ Development vs Production

### **Development Environment**
- **Hot reloading** enabled
- **Volume mounting** for live code changes
- **Development dependencies** included
- **Debugging** capabilities
- **Fast iteration** cycles

### **Production Environment**
- **Optimized builds** with multi-stage Dockerfiles
- **Minimal image sizes** for faster deployment
- **Security hardening** with non-root users
- **Resource limits** and monitoring
- **Health checks** and auto-restart

## 🔧 Troubleshooting

### **Common Issues**

#### **1. npm Install Hangs in Development**
```bash
# Clear npm cache in container
docker-compose -f docker-compose.development.yml exec frontend npm cache clean --force

# Rebuild frontend container
docker-compose -f docker-compose.development.yml build --no-cache frontend
```

#### **2. Services Not Starting**
```bash
# Check service logs
python docker-manager.py logs --environment development

# Check service health
python docker-manager.py health --environment development

# Restart specific service
docker-compose -f docker-compose.development.yml restart auth-service
```

#### **3. Port Conflicts**
```bash
# Check what's using the ports
netstat -tulpn | grep :3000
netstat -tulpn | grep :8000

# Stop conflicting services
sudo systemctl stop nginx  # if using port 80/443
```

#### **4. Docker Resource Issues**
```bash
# Check Docker resources
docker system df

# Clean up unused resources
docker system prune -a

# Increase Docker resources in Docker Desktop
# Settings > Resources > Memory: 4GB, CPUs: 2
```

### **Debugging Commands**

#### **Access Container Shell**
```bash
# Frontend container
docker-compose -f docker-compose.development.yml exec frontend sh

# Backend service container
docker-compose -f docker-compose.development.yml exec auth-service bash
```

#### **View Real-time Logs**
```bash
# All services
python docker-manager.py logs --environment development --follow

# Specific service
docker-compose -f docker-compose.development.yml logs -f auth-service
```

#### **Check Service Status**
```bash
# Docker services
python docker-manager.py status --environment development

# Container health
docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"
```

## 📊 Monitoring and Logs

### **Service Monitoring**
```bash
# Check all services
python docker-manager.py status --environment development

# Health check
python docker-manager.py health --environment development

# Resource usage
docker stats
```

### **Log Management**
```bash
# View all logs
python docker-manager.py logs --environment development

# Follow logs in real-time
python docker-manager.py logs --environment development --follow

# View specific service logs
docker-compose -f docker-compose.development.yml logs auth-service
```

## 🚀 Production Deployment

### **1. Build Production Images**
```bash
python docker-manager.py build --environment production
```

### **2. Start Production Stack**
```bash
python docker-manager.py start --environment production
```

### **3. Verify Deployment**
```bash
# Check service health
python docker-manager.py health --environment production

# Monitor logs
python docker-manager.py logs --environment production --follow
```

### **4. Access Application**
- **Frontend**: http://localhost:3000
- **API Gateway**: http://localhost:8000
- **Service Health**: http://localhost:8000/health

## 🔒 Security Considerations

### **Container Security**
- **Non-root users** in all containers
- **Minimal base images** (Alpine Linux)
- **No sensitive data** in images
- **Regular security updates**

### **Network Security**
- **Isolated networks** for services
- **Port exposure** only where needed
- **Internal communication** via service names
- **Health check endpoints** for monitoring

### **Production Hardening**
- **Resource limits** on containers
- **Read-only filesystems** where possible
- **Security scanning** of images
- **Regular vulnerability updates**

## 📈 Performance Optimization

### **Image Optimization**
- **Multi-stage builds** for smaller images
- **Layer caching** for faster builds
- **Alpine Linux** base images
- **Minimal dependencies** in production

### **Resource Management**
- **Memory limits** per container
- **CPU limits** for fair sharing
- **Network bandwidth** controls
- **Storage optimization**

## 🆘 Getting Help

### **Useful Commands**
```bash
# Check Docker version
docker --version
docker-compose --version

# Check system resources
docker system df
docker stats

# Clean up resources
docker system prune -a
```

### **Log Locations**
- **Application logs**: Container stdout/stderr
- **Docker logs**: `/var/log/docker/`
- **System logs**: `/var/log/syslog`

### **Support**
- Check the troubleshooting section above
- Review service-specific logs
- Verify Docker and Docker Compose versions
- Ensure sufficient system resources

## 🎉 Success Criteria

The Docker solution is working correctly when:
- ✅ All containers start without errors
- ✅ Health checks pass for all services
- ✅ Frontend is accessible at http://localhost:3000
- ✅ API Gateway responds at http://localhost:8000
- ✅ No npm install issues occur
- ✅ Hot reloading works in development
- ✅ Production builds are optimized
- ✅ Resource usage is reasonable 