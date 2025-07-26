# AI SchoolOS - Complete Project Documentation

## 📋 Table of Contents

1. [Project Overview](#project-overview)
2. [System Architecture](#system-architecture)
3. [Technology Stack](#technology-stack)
4. [Development Setup](#development-setup)
5. [Production Deployment](#production-deployment)
6. [Network Error Resolution](#network-error-resolution)
7. [Troubleshooting Guide](#troubleshooting-guide)
8. [Debugging Commands](#debugging-commands)
9. [File Structure](#file-structure)
10. [API Documentation](#api-documentation)
11. [Security Considerations](#security-considerations)
12. [Monitoring & Logging](#monitoring--logging)

---

## 🎯 Project Overview

**AI SchoolOS** is a comprehensive school management system built with microservices architecture. It includes student management, staff management, fee management, attendance tracking, and AI-powered analytics.

### Key Features
- ✅ Student & Staff Management
- ✅ Fee Management
- ✅ Attendance Tracking
- ✅ Timetable Management
- ✅ Library Management
- ✅ Exam Management
- ✅ AI Analytics
- ✅ Communication System
- ✅ Transport Management

---

## 🏗️ System Architecture

### High-Level Architecture
```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │   Nginx         │    │   Microservices │
│   (Next.js)     │───▶│   Reverse       │───▶│   (FastAPI)     │
│   Port 3000     │    │   Proxy         │    │   Port 8001-17  │
└─────────────────┘    │   Port 80       │    └─────────────────┘
                       └─────────────────┘
```

### Detailed Architecture
```
┌─────────────────────────────────────────────────────────────────┐
│                        Frontend Layer                          │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐           │
│  │   Admin     │  │   Staff     │  │   Student   │           │
│  │   Portal    │  │   Portal    │  │   Portal    │           │
│  └─────────────┘  └─────────────┘  └─────────────┘           │
└─────────────────────────────────────────────────────────────────┘
                                │
┌─────────────────────────────────────────────────────────────────┐
│                        Nginx Layer                            │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │              Reverse Proxy (Port 80)                  │   │
│  │  • Routes /api/* to API Gateway                      │   │
│  │  • Routes /auth/* to Auth Service                    │   │
│  │  • Routes /students/* to Student Service             │   │
│  │  • Routes /staff/* to Staff Service                  │   │
│  └─────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
                                │
┌─────────────────────────────────────────────────────────────────┐
│                     API Gateway Layer                          │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │              API Gateway (Port 8000)                   │   │
│  │  • Request Routing                                     │   │
│  │  • Authentication                                      │   │
│  │  • Rate Limiting                                       │   │
│  │  • CORS Handling                                       │   │
│  └─────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
                                │
┌─────────────────────────────────────────────────────────────────┐
│                    Microservices Layer                         │
│  ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐ │
│  │  Auth   │ │Student  │ │  Staff  │ │  Fees   │ │Homework │ │
│  │Service  │ │Service  │ │Service  │ │Service  │ │Service  │ │
│  │:8001    │ │:8002    │ │:8003    │ │:8004    │ │:8005    │ │
│  └─────────┘ └─────────┘ └─────────┘ └─────────┘ └─────────┘ │
│  ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐ │
│  │Library  │ │  Exam   │ │Timetable│ │Attendance│ │Transport│ │
│  │Service  │ │Service  │ │Service  │ │Service  │ │Service  │ │
│  │:8006    │ │:8007    │ │:8008    │ │:8009    │ │:8010    │ │
│  └─────────┘ └─────────┘ └─────────┘ └─────────┘ └─────────┘ │
│  ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐ │
│  │Comm.    │ │Analytics│ │Notif.   │ │Config   │ │Super    │ │
│  │Service  │ │Service  │ │Service  │ │Service  │ │Service  │ │
│  │:8011    │ │:8012    │ │:8013    │ │:8014    │ │Service  │ │
│  └─────────┘ └─────────┘ └─────────┘ └─────────┘ │:8015    │ │
│  ┌─────────┐ ┌─────────┐                           └─────────┘ │
│  │  AI     │ │AI       │                                     │
│  │Service  │ │Analytics│                                     │
│  │:8016    │ │Service  │                                     │
│  └─────────┘ │:8017    │                                     │
│               └─────────┘                                     │
└─────────────────────────────────────────────────────────────────┘
                                │
┌─────────────────────────────────────────────────────────────────┐
│                    Data Layer                                  │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐           │
│  │  PostgreSQL │  │    Redis    │  │   MongoDB   │           │
│  │   Database  │  │   Cache     │  │   Analytics │           │
│  │   Port 5432 │  │   Port 6379 │  │   Port 27017│           │
│  └─────────────┘  └─────────────┘  └─────────────┘           │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🛠️ Technology Stack

### Frontend
- **Framework**: Next.js 13+ (React)
- **Language**: TypeScript
- **Styling**: Tailwind CSS
- **State Management**: React Context + Hooks
- **HTTP Client**: Axios
- **Build Tool**: Webpack (Next.js built-in)

### Backend
- **Framework**: FastAPI (Python)
- **Language**: Python 3.9+
- **Database**: PostgreSQL
- **Cache**: Redis
- **Analytics**: MongoDB
- **Authentication**: JWT
- **API Documentation**: Swagger/OpenAPI

### Infrastructure
- **Containerization**: Docker & Docker Compose
- **Reverse Proxy**: Nginx
- **Cloud Platform**: AWS EC2
- **Version Control**: Git
- **CI/CD**: GitHub Actions (recommended)

---

## 🚀 Development Setup

### Prerequisites
```bash
# Required Software
- Docker Desktop
- Node.js 18+
- Python 3.9+
- Git
```

### Local Development
```bash
# 1. Clone Repository
git clone <repository-url>
cd ai-schoolos

# 2. Install Dependencies
npm install
cd frontend && npm install
cd ../backend && pip install -r requirements.txt

# 3. Start Development Environment
docker-compose -f docker-compose.development.yml up -d

# 4. Access Applications
- Frontend: http://localhost:3000
- API Gateway: http://localhost:8000
- API Docs: http://localhost:8000/docs
```

### Environment Configuration
```bash
# Frontend Environment (.env.local)
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_AUTH_SERVICE_URL=http://localhost:8001
NEXT_PUBLIC_STUDENT_SERVICE_URL=http://localhost:8002
# ... (other service URLs)

# Backend Environment
DATABASE_URL=postgresql://user:pass@localhost:5432/schoolos
REDIS_URL=redis://localhost:6379
JWT_SECRET=your-secret-key
```

---

## 🚀 Production Deployment

### EC2 Deployment Process

#### Step 1: Server Setup
```bash
# Connect to EC2
ssh -i your-key.pem ubuntu@your-ec2-ip

# Update System
sudo apt update && sudo apt upgrade -y

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER

# Install Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/download/v2.20.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
```

#### Step 2: Application Deployment
```bash
# Clone Repository
git clone <repository-url>
cd ai-schoolos

# Create Production Environment
./setup-ec2-nginx-config.sh
# Enter your EC2 IP when prompted

# Start Services
docker-compose -f docker-compose.production.yml up -d

# Check Status
docker ps
docker logs ai-schoolos-nginx
```

#### Step 3: Security Configuration
```bash
# EC2 Security Groups
- Port 80 (HTTP): Allow from anywhere
- Port 443 (HTTPS): Allow from anywhere (optional)
- Remove all other ports (3000, 8000-8017)
```

### Nginx Configuration
The Nginx reverse proxy routes traffic as follows:

| URL Path | Service | Internal Port | Description |
|----------|---------|---------------|-------------|
| `/` | Frontend | 3000 | Main application |
| `/api/` | API Gateway | 8000 | All API calls |
| `/auth/` | Auth Service | 8001 | Authentication |
| `/students/` | Student Service | 8002 | Student management |
| `/staff/` | Staff Service | 8003 | Staff management |
| `/fees/` | Fee Service | 8004 | Fee management |
| `/homework/` | Homework Service | 8005 | Homework management |
| `/library/` | Library Service | 8006 | Library management |
| `/exams/` | Exam Service | 8007 | Exam management |
| `/timetable/` | Timetable Service | 8008 | Timetable management |
| `/attendance/` | Attendance Service | 8009 | Attendance tracking |
| `/transport/` | Transport Service | 8010 | Transport management |
| `/communication/` | Communication Service | 8011 | Communication |
| `/analytics/` | Analytics Service | 8012 | Analytics |
| `/notifications/` | Notification Service | 8013 | Notifications |
| `/config/` | Config Service | 8014 | Configuration |
| `/super-admin/` | Super Admin Service | 8015 | Super admin |
| `/ai/` | AI Service | 8016 | AI features |
| `/ai-analytics/` | AI Analytics Service | 8017 | AI analytics |

---

## 🔧 Network Error Resolution

### Problem Description
```
Error: net::ERR_CONNECTION_REFUSED
URL: localhost:8000/api/v1/students
```

### Root Cause
The frontend was trying to connect to `localhost:8000` but the backend services were running on EC2, not locally.

### Solution Implemented

#### 1. Environment Configuration
Created `frontend/.env.production`:
```bash
# All services use the same Nginx endpoint
NEXT_PUBLIC_API_URL=http://YOUR_EC2_IP:80
NEXT_PUBLIC_AUTH_SERVICE_URL=http://YOUR_EC2_IP:80
NEXT_PUBLIC_STUDENT_SERVICE_URL=http://YOUR_EC2_IP:80
# ... (all services use port 80)
```

#### 2. Nginx Reverse Proxy
Updated `nginx.conf` to route all traffic through port 80:
```nginx
# API Gateway routing
location /api/ {
    proxy_pass http://api_gateway/;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;
}

# Service-specific routing
location /students/ {
    proxy_pass http://student_service/;
    # ... (headers)
}
```

#### 3. Security Group Configuration
- **Before**: Ports 3000, 8000-8017 open
- **After**: Only port 80 open

---

## 🚨 Troubleshooting Guide

### Common Issues & Solutions

#### 1. Connection Refused Errors
```bash
# Check if services are running
docker ps

# Check Nginx logs
docker logs ai-schoolos-nginx

# Check API Gateway logs
docker logs ai-schoolos-api-gateway

# Test connectivity
curl -v http://YOUR_EC2_IP/health
```

#### 2. CORS Errors
```bash
# Check Nginx CORS configuration
# Verify frontend domain is allowed
# Check browser console for specific errors
```

#### 3. Environment Variables Not Loading
```bash
# Rebuild frontend after environment changes
cd frontend && npm run build

# Clear browser cache
# Check if .env.production exists
```

#### 4. Database Connection Issues
```bash
# Check database container
docker logs ai-schoolos-postgres

# Verify database URL in environment
# Check if database is initialized
```

#### 5. Service Health Issues
```bash
# Check all service health
curl http://YOUR_EC2_IP/health
curl http://YOUR_EC2_IP/services/health

# Check individual services
docker logs ai-schoolos-auth-service
docker logs ai-schoolos-student-service
```

### Debug Commands

#### Docker Commands
```bash
# List all containers
docker ps -a

# View container logs
docker logs <container-name>

# Execute commands in container
docker exec -it <container-name> /bin/bash

# Check container resources
docker stats
```

#### Network Commands
```bash
# Test port connectivity
telnet YOUR_EC2_IP 80
nc -zv YOUR_EC2_IP 80

# Check DNS resolution
nslookup YOUR_EC2_IP

# Test HTTP connectivity
curl -I http://YOUR_EC2_IP
```

#### System Commands
```bash
# Check disk space
df -h

# Check memory usage
free -h

# Check CPU usage
top

# Check network connections
netstat -tulpn
```

---

## 📁 File Structure

```
ai-schoolos/
├── frontend/                          # Next.js Frontend
│   ├── src/
│   │   ├── app/                      # App Router
│   │   ├── components/               # React Components
│   │   ├── services/                 # API Services
│   │   └── contexts/                 # React Contexts
│   ├── .env.production              # Production Environment
│   └── package.json
├── backend/                          # FastAPI Backend
│   ├── api-gateway/                  # API Gateway Service
│   ├── services/                     # Microservices
│   │   ├── auth-service/
│   │   ├── student-service/
│   │   ├── staff-service/
│   │   └── ... (other services)
│   ├── shared/                       # Shared Utilities
│   └── requirements.txt
├── nginx.conf                        # Nginx Configuration
├── docker-compose.production.yml     # Production Docker Compose
├── setup-ec2-nginx-config.bat       # Windows Setup Script
├── setup-ec2-nginx-config.sh        # Linux Setup Script
├── EC2_DEPLOYMENT_GUIDE.md          # Deployment Guide
└── PROJECT_DOCUMENTATION.md         # This Documentation
```

---

## 🔌 API Documentation

### Authentication Endpoints
```bash
POST /auth/login
POST /auth/register
POST /auth/refresh
GET  /auth/profile
```

### Student Management
```bash
GET    /api/v1/students
POST   /api/v1/students
GET    /api/v1/students/{id}
PUT    /api/v1/students/{id}
DELETE /api/v1/students/{id}
```

### Staff Management
```bash
GET    /api/v1/staff
POST   /api/v1/staff
GET    /api/v1/staff/{id}
PUT    /api/v1/staff/{id}
DELETE /api/v1/staff/{id}
```

### Health Checks
```bash
GET /health                    # API Gateway health
GET /services/health           # All services health
```

### API Response Format
```json
{
  "success": true,
  "data": {
    // Response data
  },
  "message": "Operation successful",
  "error": null
}
```

---

## 🔒 Security Considerations

### Authentication
- JWT tokens for API authentication
- Token refresh mechanism
- Secure password hashing

### Network Security
- Only port 80 exposed externally
- Internal services not accessible from outside
- Nginx handles CORS and security headers

### Data Security
- Database connections encrypted
- Sensitive data encrypted at rest
- Regular security updates

### Environment Variables
- Never commit sensitive data to Git
- Use environment files for configuration
- Rotate secrets regularly

---

## 📊 Monitoring & Logging

### Application Logs
```bash
# View all service logs
docker-compose logs -f

# View specific service logs
docker logs -f ai-schoolos-api-gateway
docker logs -f ai-schoolos-nginx
```

### Health Monitoring
```bash
# Check service health
curl http://YOUR_EC2_IP/health
curl http://YOUR_EC2_IP/services/health

# Monitor resource usage
docker stats
```

### Performance Monitoring
- Response time monitoring
- Error rate tracking
- Resource utilization
- Database performance

### Recommended Monitoring Tools
- AWS CloudWatch
- Prometheus + Grafana
- ELK Stack (Elasticsearch, Logstash, Kibana)

---

## 🔄 Update Process

### Code Updates
```bash
# 1. Update code locally
git add .
git commit -m "Update description"
git push origin main

# 2. Deploy to EC2
ssh -i key.pem ubuntu@YOUR_EC2_IP
cd ai-schoolos
git pull origin main

# 3. Rebuild and restart
docker-compose -f docker-compose.production.yml down
docker-compose -f docker-compose.production.yml up -d --build
```

### Configuration Updates
```bash
# 1. Update environment file
# Edit frontend/.env.production

# 2. Rebuild frontend
cd frontend && npm run build

# 3. Restart services
docker-compose -f docker-compose.production.yml restart frontend
```

### Database Updates
```bash
# Run migrations
docker exec -it ai-schoolos-api-gateway alembic upgrade head

# Backup before updates
docker exec -it ai-schoolos-postgres pg_dump -U postgres schoolos > backup.sql
```

---

## 📞 Support & Maintenance

### Regular Maintenance Tasks
- [ ] Update system packages
- [ ] Update Docker images
- [ ] Rotate security keys
- [ ] Backup databases
- [ ] Monitor disk space
- [ ] Check service health

### Emergency Procedures
1. **Service Down**: Check Docker containers and logs
2. **Database Issues**: Check PostgreSQL logs and connectivity
3. **Network Issues**: Verify security groups and Nginx configuration
4. **Performance Issues**: Monitor resource usage and optimize

### Contact Information
- **Developer**: [Your Contact Info]
- **Documentation**: This file
- **Repository**: [GitHub URL]

---

## 📝 Notes

### Key Learnings
1. **Nginx Reverse Proxy**: Essential for production deployments
2. **Environment Configuration**: Critical for different environments
3. **Security Groups**: Only expose necessary ports
4. **Health Checks**: Important for monitoring service status
5. **Logging**: Essential for debugging and monitoring

### Future Improvements
- [ ] Implement HTTPS with Let's Encrypt
- [ ] Add comprehensive monitoring
- [ ] Implement automated backups
- [ ] Add load balancing
- [ ] Implement CI/CD pipeline
- [ ] Add comprehensive testing

---

*This documentation should be updated as the project evolves.* 