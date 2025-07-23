# AI SchoolOS Troubleshooting Guide

## 🚨 Quick Fix Commands

### 1. Complete Reset and Fix
```bash
# Run the comprehensive fix script
fix-schoolos.bat
```

### 2. Simple Start (Recommended for first-time setup)
```bash
# Run the simplified version
quick-start-simple.bat
```

### 3. Diagnostic Check
```bash
# Check what's wrong
diagnose-schoolos.bat
```

## 🔍 Common Issues and Solutions

### Issue 1: Docker Desktop Not Running
**Symptoms:**
- `error during connect: Get "http://%2F%2F.%2Fpipe%2FdockerDesktopLinuxEngine/v1.48/containers/json?all=1"`
- `The system cannot find the file specified`

**Solution:**
1. Start Docker Desktop
2. Wait for it to fully load (green icon in system tray)
3. Run the diagnostic script: `diagnose-schoolos.bat`

### Issue 2: Port Already in Use
**Symptoms:**
- `Error response from daemon: driver failed programming external connectivity`
- `Bind for 0.0.0.0:3000 failed: port is already allocated`

**Solution:**
```bash
# Check what's using the port
netstat -ano | findstr :3000
netstat -ano | findstr :8000

# Kill the process (replace PID with actual process ID)
taskkill /PID <PID> /F

# Or stop all containers
docker-compose down
```

### Issue 3: Frontend Can't Connect to Backend
**Symptoms:**
- Frontend loads but shows errors
- API calls fail
- Network errors in browser console

**Solution:**
1. Check if environment file exists: `frontend\.env.local`
2. Verify backend services are running: `docker-compose ps`
3. Check service logs: `docker-compose logs api-gateway`

### Issue 4: Docker Build Fails
**Symptoms:**
- Build errors during `docker-compose build`
- Missing dependencies
- Permission errors

**Solution:**
```bash
# Clean everything and rebuild
docker-compose down --volumes --remove-orphans
docker system prune -f
docker-compose build --no-cache
```

### Issue 5: Node Modules Issues
**Symptoms:**
- Frontend build fails
- Missing dependencies
- TypeScript errors

**Solution:**
```bash
# Clean and reinstall
cd frontend
rm -rf node_modules package-lock.json
npm install
cd ..
npm install
```

### Issue 6: Database Connection Issues
**Symptoms:**
- Services fail to start
- Database connection errors
- Migration failures

**Solution:**
```bash
# Reset database
docker-compose down --volumes
docker-compose up -d postgres
# Wait for postgres to be ready, then start other services
docker-compose up -d
```

## 🛠️ Manual Fixes

### Fix Frontend Environment
```bash
# Create frontend environment file
echo NEXT_PUBLIC_API_URL=http://localhost:8000 > frontend\.env.local
echo NEXT_PUBLIC_AUTH_SERVICE_URL=http://localhost:8001 >> frontend\.env.local
echo NEXT_PUBLIC_STUDENT_SERVICE_URL=http://localhost:8002 >> frontend\.env.local
echo NODE_ENV=development >> frontend\.env.local
```

### Fix Docker Permissions (Linux/macOS)
```bash
# Add user to docker group
sudo usermod -aG docker $USER
# Log out and back in, or run:
newgrp docker
```

### Fix Windows Docker Issues
```bash
# Reset Docker Desktop
# 1. Open Docker Desktop
# 2. Go to Settings > Troubleshoot
# 3. Click "Reset to factory defaults"
# 4. Restart Docker Desktop
```

## 📊 Service Health Checks

### Check All Services
```bash
docker-compose ps
```

### Check Specific Service Logs
```bash
# API Gateway
docker-compose logs api-gateway

# Frontend
docker-compose logs frontend

# Database
docker-compose logs postgres
```

### Test Service Endpoints
```bash
# API Gateway
curl http://localhost:8000/health

# Auth Service
curl http://localhost:8001/health

# Frontend
curl http://localhost:3000
```

## 🔧 Advanced Troubleshooting

### Complete System Reset
```bash
# Stop all containers
docker-compose down --volumes --remove-orphans

# Remove all images
docker system prune -a -f

# Clean npm cache
npm cache clean --force

# Remove node_modules
rm -rf frontend/node_modules
rm -rf node_modules

# Reinstall everything
npm install
cd frontend && npm install && cd ..

# Rebuild and start
docker-compose up -d --build
```

### Debug Docker Build
```bash
# Build with verbose output
docker-compose build --no-cache --progress=plain

# Check specific service build
docker-compose build api-gateway --no-cache --progress=plain
```

### Check Resource Usage
```bash
# Check Docker resource usage
docker stats

# Check disk space
docker system df
```

## 📞 Getting Help

If you're still having issues:

1. **Run the diagnostic script:** `diagnose-schoolos.bat`
2. **Check the logs:** `docker-compose logs`
3. **Try the simple version:** `quick-start-simple.bat`
4. **Check this troubleshooting guide**

### Useful Commands for Debugging

```bash
# Check Docker status
docker info

# Check Docker Compose version
docker-compose --version

# Check Node.js version
node --version

# Check npm version
npm --version

# List all containers
docker ps -a

# List all images
docker images

# Check Docker networks
docker network ls
```

## 🎯 Quick Solutions by Issue Type

| Issue | Quick Fix |
|-------|-----------|
| Docker not running | Start Docker Desktop |
| Port conflicts | `docker-compose down` then restart |
| Build failures | `docker-compose build --no-cache` |
| Frontend errors | Check `frontend\.env.local` exists |
| Database issues | `docker-compose down --volumes` |
| Dependencies | `npm install` in frontend and root |
| Everything broken | Run `fix-schoolos.bat` | 