# AI SchoolOS EC2 + Nginx Deployment Guide

## 🚀 Quick Fix for Network Error

If you're getting `net::ERR_CONNECTION_REFUSED` when trying to add students, this guide will help you fix it.

### The Problem
Your frontend is trying to connect to `localhost:8000` but your backend services are running on EC2 with Nginx routing.

### The Solution

#### Step 1: Set Up EC2 + Nginx Configuration

**For Windows:**
```bash
setup-ec2-nginx-config.bat
```

**For Linux/macOS:**
```bash
chmod +x setup-ec2-nginx-config.sh
./setup-ec2-nginx-config.sh
```

This will create a `frontend/.env.production` file with your EC2 + Nginx configuration.

#### Step 2: Update Configuration
Edit the generated `frontend/.env.production` file and replace `YOUR_EC2_PUBLIC_IP` with your actual EC2 public IP address.

Example:
```bash
# API Gateway - EC2 + Nginx Configuration
NEXT_PUBLIC_API_URL=http://18.123.45.67:80

# Service URLs - All routed through Nginx
NEXT_PUBLIC_AUTH_SERVICE_URL=http://18.123.45.67:80
NEXT_PUBLIC_STUDENT_SERVICE_URL=http://18.123.45.67:80
# ... etc (all services use the same Nginx endpoint)
```

#### Step 3: Commit and Deploy
```bash
# Commit the configuration
git add frontend/.env.production
git commit -m "Add EC2 + Nginx production configuration"
git push origin main

# On your EC2 instance
git pull origin main
```

#### Step 4: Rebuild and Deploy
```bash
# On your EC2 instance
cd frontend
npm run build
# Deploy the updated build
```

## 🔧 Manual Configuration

If you prefer to configure manually:

### 1. Create Environment File
Create `frontend/.env.production`:
```bash
# API Gateway - EC2 + Nginx Configuration
NEXT_PUBLIC_API_URL=http://YOUR_EC2_PUBLIC_IP:80

# Service URLs - All routed through Nginx
NEXT_PUBLIC_AUTH_SERVICE_URL=http://YOUR_EC2_PUBLIC_IP:80
NEXT_PUBLIC_STUDENT_SERVICE_URL=http://YOUR_EC2_PUBLIC_IP:80
NEXT_PUBLIC_STAFF_SERVICE_URL=http://YOUR_EC2_PUBLIC_IP:80
NEXT_PUBLIC_FEE_SERVICE_URL=http://YOUR_EC2_PUBLIC_IP:80
NEXT_PUBLIC_HOMEWORK_SERVICE_URL=http://YOUR_EC2_PUBLIC_IP:80
NEXT_PUBLIC_LIBRARY_SERVICE_URL=http://YOUR_EC2_PUBLIC_IP:80
NEXT_PUBLIC_EXAM_SERVICE_URL=http://YOUR_EC2_PUBLIC_IP:80
NEXT_PUBLIC_TIMETABLE_SERVICE_URL=http://YOUR_EC2_PUBLIC_IP:80
NEXT_PUBLIC_ATTENDANCE_SERVICE_URL=http://YOUR_EC2_PUBLIC_IP:80
NEXT_PUBLIC_TRANSPORT_SERVICE_URL=http://YOUR_EC2_PUBLIC_IP:80
NEXT_PUBLIC_COMMUNICATION_SERVICE_URL=http://YOUR_EC2_PUBLIC_IP:80
NEXT_PUBLIC_ANALYTICS_SERVICE_URL=http://YOUR_EC2_PUBLIC_IP:80
NEXT_PUBLIC_NOTIFICATION_SERVICE_URL=http://YOUR_EC2_PUBLIC_IP:80
NEXT_PUBLIC_CONFIG_SERVICE_URL=http://YOUR_EC2_PUBLIC_IP:80
NEXT_PUBLIC_SUPER_ADMIN_SERVICE_URL=http://YOUR_EC2_PUBLIC_IP:80
NEXT_PUBLIC_AI_SERVICE_URL=http://YOUR_EC2_PUBLIC_IP:80
NEXT_PUBLIC_AI_ANALYTICS_SERVICE_URL=http://YOUR_EC2_PUBLIC_IP:80

# Production settings
NODE_ENV=production
```

### 2. Update Docker Configuration
Use the production Docker Compose file with Nginx:
```bash
docker-compose -f docker-compose.production.yml up -d
```

## 🔒 Security Configuration

### EC2 Security Groups
With Nginx, you only need **ONE port** open:

| Port | Service | Description |
|------|---------|-------------|
| 80 | Nginx | HTTP traffic (or 443 for HTTPS) |

**Remove these ports** (no longer needed):
- ❌ Port 3000 (Frontend)
- ❌ Port 8000 (API Gateway)
- ❌ Port 8001-8017 (All services)

### Security Group Rules
```bash
# Allow HTTP traffic only
Type: HTTP
Protocol: TCP
Port Range: 80
Source: 0.0.0.0/0

# Optional: Allow HTTPS traffic
Type: HTTPS
Protocol: TCP
Port Range: 443
Source: 0.0.0.0/0
```

## 🌐 Nginx Routing

Your Nginx configuration routes traffic as follows:

| URL Path | Service | Description |
|----------|---------|-------------|
| `/` | Frontend | Main application |
| `/api/` | API Gateway | All API calls |
| `/auth/` | Auth Service | Authentication |
| `/students/` | Student Service | Student management |
| `/staff/` | Staff Service | Staff management |
| `/fees/` | Fee Service | Fee management |
| `/homework/` | Homework Service | Homework management |
| `/library/` | Library Service | Library management |
| `/exams/` | Exam Service | Exam management |
| `/timetable/` | Timetable Service | Timetable management |
| `/attendance/` | Attendance Service | Attendance tracking |
| `/transport/` | Transport Service | Transport management |
| `/communication/` | Communication Service | Communication |
| `/analytics/` | Analytics Service | Analytics |
| `/notifications/` | Notification Service | Notifications |
| `/config/` | Config Service | Configuration |
| `/super-admin/` | Super Admin Service | Super admin |
| `/ai/` | AI Service | AI features |
| `/ai-analytics/` | AI Analytics Service | AI analytics |
| `/health` | API Gateway | Health check |
| `/services/health` | API Gateway | Services health check |

## 🧪 Testing

### Test Nginx Routing
```bash
# Test frontend
curl http://YOUR_EC2_PUBLIC_IP/

# Test API Gateway
curl http://YOUR_EC2_PUBLIC_IP/api/health

# Test student service
curl http://YOUR_EC2_PUBLIC_IP/api/v1/students

# Test health check
curl http://YOUR_EC2_PUBLIC_IP/health
```

### Test Frontend Connection
Open your browser and navigate to your frontend URL. Try adding a student - the network error should be resolved.

## 🚨 Troubleshooting

### Common Issues

1. **Connection Refused**
   - Check if Nginx is running: `docker ps | grep nginx`
   - Verify security group allows port 80
   - Check Nginx logs: `docker logs ai-schoolos-nginx`

2. **CORS Errors**
   - Nginx handles CORS automatically
   - Check if frontend domain is allowed

3. **Environment Variables Not Loading**
   - Rebuild frontend after updating `.env.production`
   - Clear browser cache
   - Check if environment file is being read

### Debug Commands
```bash
# Check if services are running
docker ps

# Check Nginx logs
docker logs ai-schoolos-nginx

# Check API Gateway logs
docker logs ai-schoolos-api-gateway

# Test Nginx routing
curl -v http://YOUR_EC2_PUBLIC_IP/health
```

## 📝 Next Steps

After fixing the network error:

1. **Test all features** - Add students, staff, etc.
2. **Monitor performance** - Check response times
3. **Set up monitoring** - Use AWS CloudWatch
4. **Configure SSL** - Set up HTTPS with Let's Encrypt
5. **Set up backups** - Configure database backups

## 🔄 Update Process

When you need to update the configuration:

1. Update `frontend/.env.production` with new IP
2. Commit and push to GitHub
3. Pull on EC2 instance
4. Rebuild and redeploy frontend

```bash
# Update configuration
git add frontend/.env.production
git commit -m "Update EC2 + Nginx configuration"
git push origin main

# On EC2
git pull origin main
cd frontend && npm run build
```

## 🎯 Benefits of Nginx Setup

- ✅ **Single entry point** - Only port 80 exposed
- ✅ **Better security** - Internal services not exposed
- ✅ **Load balancing** - Can add multiple service instances
- ✅ **SSL termination** - Easy HTTPS setup
- ✅ **Caching** - Static content caching
- ✅ **Rate limiting** - Protect against abuse

This should resolve your network error and allow you to add students successfully! 