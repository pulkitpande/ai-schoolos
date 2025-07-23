# AI SchoolOS - NPM Install Issues & Solutions

## 🚨 Problem: npm install runs infinitely and never completes

This is a common issue that affects many Node.js projects, especially on Windows systems. The `npm install` command hangs indefinitely, preventing the frontend from starting.

### Common Causes:
- **Network connectivity issues** to npm registry
- **Corrupted npm cache**
- **Conflicting package-lock.json**
- **Large node_modules directory**
- **Antivirus software interference**
- **Proxy/firewall blocking npm**
- **Insufficient disk space**
- **Node.js/npm version conflicts**

## 🔧 Complete Solution

### 1. NPM Install Fixer (`fix-npm-install.py`)

**Purpose**: Diagnoses and fixes npm install issues automatically.

**Features**:
- ✅ Clears npm cache automatically
- ✅ Removes problematic `node_modules` and `package-lock.json`
- ✅ Tries multiple installation methods with timeouts
- ✅ Handles network connectivity issues
- ✅ Provides detailed error reporting

**Usage**:
```bash
# Check npm status
python fix-npm-install.py --check

# Fix npm install issues
python fix-npm-install.py

# Windows batch file
fix-npm-install.bat
```

**What it does**:
1. Checks Node.js and npm availability
2. Validates network connectivity to npm registry
3. Clears npm cache with `npm cache clean --force`
4. Removes existing `node_modules` and `package-lock.json`
5. Tries standard `npm install` with 10-minute timeout
6. Falls back to alternative methods:
   - `npm install --no-optional`
   - `npm install --legacy-peer-deps`
   - `npm install --force`
   - `npm install --no-audit --no-fund`

### 2. Simplified Full Stack Starter (`start-without-npm.py`)

**Purpose**: Starts backend and frontend without npm install issues.

**Features**:
- ✅ Skips npm install if dependencies are already present
- ✅ Starts backend services with proper error handling
- ✅ Starts frontend development server
- ✅ Graceful shutdown with Ctrl+C
- ✅ Process monitoring and recovery

**Usage**:
```bash
# Start with default services (auth-service, student-service)
python start-without-npm.py

# Start with specific services
python start-without-npm.py --services auth-service student-service ai-service

# Skip frontend dependency check
python start-without-npm.py --skip-frontend-check

# Windows batch file
start-simple.bat auth-service student-service
```

### 3. Service Monitor (`monitor-services.py`)

**Purpose**: Real-time monitoring of all services.

**Features**:
- ✅ Shows which services are running
- ✅ Port checking for service health
- ✅ Can start/stop/restart individual services
- ✅ Process ID tracking
- ✅ Visual status indicators (🟢/🔴)

**Usage**:
```bash
# Check all services status
python monitor-services.py status

# Get detailed info about a service
python monitor-services.py detailed auth-service

# Start a specific service
python monitor-services.py start auth-service

# Stop a specific service
python monitor-services.py stop auth-service

# Restart a specific service
python monitor-services.py restart auth-service
```

## 🛠️ Manual Troubleshooting Steps

### If npm install still hangs:

1. **Clear everything manually**:
   ```bash
   cd frontend
   rmdir /s node_modules
   del package-lock.json
   npm cache clean --force
   ```

2. **Try alternative installation methods**:
   ```bash
   npm install --no-optional
   npm install --legacy-peer-deps
   npm install --force
   npm install --no-audit --no-fund
   ```

3. **Check network connectivity**:
   ```bash
   npm ping
   npm config get registry
   ```

4. **Update npm and Node.js**:
   ```bash
   npm install -g npm@latest
   ```

5. **Use yarn instead of npm**:
   ```bash
   npm install -g yarn
   yarn install
   ```

## 📊 Service Status Monitoring

### Current Issue Analysis:
From the output shown, we can see:
- ✅ Backend services start successfully
- ❌ Services stop unexpectedly after startup
- ❌ Frontend fails to start due to npm not found in PATH
- ⚠️ API Gateway timeout (services not responding on port 8000)

### Recommended Actions:

1. **Fix npm PATH issue**:
   ```bash
   # Add npm to PATH or use full path
   C:\Program Files\nodejs\npm.cmd run dev
   ```

2. **Check backend service logs**:
   ```bash
   # Check if services have proper main.py files
   dir backend\api-gateway\main.py
   dir backend\services\auth-service\main.py
   dir backend\services\student-service\main.py
   ```

3. **Verify service requirements**:
   ```bash
   # Check if requirements.txt files exist
   dir backend\api-gateway\requirements.txt
   dir backend\services\auth-service\requirements.txt
   ```

## 🚀 Quick Start Guide

### Step 1: Fix npm issues (if needed)
```bash
python fix-npm-install.py
```

### Step 2: Start the full stack
```bash
# Simple approach (recommended)
python start-without-npm.py

# Or with specific services
python start-without-npm.py --services auth-service student-service ai-service
```

### Step 3: Monitor services
```bash
python monitor-services.py status
```

### Step 4: Access the application
- **Frontend**: http://localhost:3000
- **API Gateway**: http://localhost:8000
- **Service Monitor**: Run `python monitor-services.py status`

## 🔍 Debugging Commands

### Check npm status:
```bash
python fix-npm-install.py --check
```

### Check service requirements:
```bash
python start-backend-simple.py check
```

### Monitor all services:
```bash
python monitor-services.py status
```

### Get detailed service info:
```bash
python monitor-services.py detailed auth-service
```

## 📋 File Structure

```
ai-schoolos/
├── fix-npm-install.py          # NPM issue fixer
├── fix-npm-install.bat         # Windows batch file
├── start-without-npm.py        # Simplified full stack starter
├── start-simple.bat            # Windows batch file
├── monitor-services.py          # Service monitor
├── start-backend-simple.py     # Enhanced backend starter
├── start-backend-enhanced.bat  # Windows batch file
├── NPM_ISSUES_SOLUTION.md      # This documentation
└── frontend/
    ├── package.json
    ├── node_modules/           # (created after npm install)
    └── .env.local              # (created automatically)
```

## 🎯 Success Criteria

The solution is working correctly when:
- ✅ `npm install` completes within 10 minutes
- ✅ Frontend starts on http://localhost:3000
- ✅ Backend services start without errors
- ✅ API Gateway responds on http://localhost:8000
- ✅ Service monitor shows all services as "Running"

## 🆘 Getting Help

If you're still experiencing issues:

1. **Check the logs**: Look for specific error messages
2. **Verify requirements**: Ensure all dependencies are installed
3. **Try Docker**: Use the Docker solution for consistent environment
4. **Check network**: Ensure no firewall/proxy is blocking npm
5. **Update tools**: Make sure Node.js and npm are up to date

## 📞 Support

For additional help:
- Check the troubleshooting guide in `TROUBLESHOOTING.md`
- Review the development setup in `DEVELOPMENT_SETUP.md`
- Use the Docker solution for production-ready deployment 