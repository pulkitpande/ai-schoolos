 # 🚀 AI SchoolOS - Production Scaling Guide

## 🎯 **Perfect Production Architecture**

### **Why This Setup is Perfect for Scaling:**

1. **Single Entry Point**: Only port 80 exposed externally
2. **Reverse Proxy**: Nginx handles all routing internally
3. **Microservices**: Each service runs independently
4. **Health Checks**: Automatic monitoring and restart
5. **Container Isolation**: Each service in its own container
6. **Easy Scaling**: Add more instances of any service

## 🏗️ **Architecture Overview**

```
Internet → Port 80 → Nginx → Services
                    ↓
            ┌─────────────────┐
            │   Frontend      │ (Port 3000)
            ├─────────────────┤
            │  API Gateway    │ (Port 8000)
            ├─────────────────┤
            │  Auth Service   │ (Port 8001)
            ├─────────────────┤
            │ Student Service │ (Port 8002)
            └─────────────────┘
```

## 🚀 **Deployment Steps**

### **Step 1: Deploy to Production**
```bash
# On your EC2 instance
git clone https://github.com/pulkitpande/ai-schoolos.git
cd ai-schoolos

# Make script executable
chmod +x deploy-production.sh

# Run production deployment
./deploy-production.sh
```

### **Step 2: Configure EC2 Security Group**
Only **ONE** inbound rule needed:

| Type | Protocol | Port Range | Source | Description |
|------|----------|------------|--------|-------------|
| **HTTP** | TCP | 80 | 0.0.0.0/0 | Main Application |

### **Step 3: Test Your Application**
```bash
# Test locally
curl http://localhost/health

# Test externally (replace with your EC2 IP)
curl http://3.110.158.50/health
```

## 🌐 **URL Structure**

| Service | Internal URL | External URL | Description |
|---------|--------------|--------------|-------------|
| **Frontend** | `http://localhost:3000` | `http://your-domain.com/` | Main application |
| **API Gateway** | `http://localhost:8000` | `http://your-domain.com/api/` | API endpoints |
| **Auth Service** | `http://localhost:8001` | `http://your-domain.com/auth/` | Authentication |
| **Student Service** | `http://localhost:8002` | `http://your-domain.com/students/` | Student management |

## 🔧 **Management Commands**

### **View Service Status**
```bash
# Check all services
docker-compose -f docker-compose.production.yml ps

# View logs
docker-compose -f docker-compose.production.yml logs -f

# View specific service logs
docker-compose -f docker-compose.production.yml logs -f nginx
docker-compose -f docker-compose.production.yml logs -f frontend
```

### **Update Services**
```bash
# Pull latest code
git pull origin main

# Rebuild and restart
docker-compose -f docker-compose.production.yml up -d --build

# Restart specific service
docker-compose -f docker-compose.production.yml restart frontend
```

### **Scale Services**
```bash
# Scale frontend to 3 instances
docker-compose -f docker-compose.production.yml up -d --scale frontend=3

# Scale API gateway to 2 instances
docker-compose -f docker-compose.production.yml up -d --scale api-gateway=2
```

## 📈 **Scaling Strategies**

### **1. Horizontal Scaling**
```bash
# Scale any service horizontally
docker-compose -f docker-compose.production.yml up -d --scale auth-service=3
docker-compose -f docker-compose.production.yml up -d --scale student-service=2
```

### **2. Load Balancer Setup**
For production, add a load balancer:
```yaml
# Add to docker-compose.production.yml
load-balancer:
  image: nginx:alpine
  ports:
    - "80:80"
  volumes:
    - ./load-balancer.conf:/etc/nginx/nginx.conf:ro
  depends_on:
    - nginx
```

### **3. Database Scaling**
```bash
# Add PostgreSQL for production
postgres:
  image: postgres:13
  environment:
    POSTGRES_DB: schoolos
    POSTGRES_USER: admin
    POSTGRES_PASSWORD: secure_password
  volumes:
    - postgres_data:/var/lib/postgresql/data
```

## 🔒 **Security Best Practices**

### **1. Environment Variables**
Create `.env.production`:
```bash
# Database
DATABASE_URL=postgresql://admin:secure_password@postgres:5432/schoolos

# JWT Secret
JWT_SECRET=your_super_secure_jwt_secret_here

# API Keys
API_KEY=your_api_key_here
```

### **2. SSL/HTTPS Setup**
```bash
# Install Certbot
sudo apt-get update
sudo apt-get install certbot python3-certbot-nginx

# Get SSL certificate
sudo certbot --nginx -d your-domain.com

# Auto-renewal
sudo crontab -e
# Add: 0 12 * * * /usr/bin/certbot renew --quiet
```

### **3. Firewall Configuration**
```bash
# Allow only necessary ports
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw allow 22/tcp  # SSH
sudo ufw enable
```

## 📊 **Monitoring & Health Checks**

### **Health Check Endpoints**
- **Overall Health**: `http://your-domain.com/health`
- **Frontend Health**: `http://your-domain.com/api/health`
- **Service Health**: `http://your-domain.com/auth/health`

### **Monitoring Commands**
```bash
# Check resource usage
docker stats

# Check service health
curl -f http://localhost/health

# Monitor logs in real-time
docker-compose -f docker-compose.production.yml logs -f --tail=100
```

## 🚨 **Troubleshooting**

### **Common Issues**

#### **1. Port 80 Already in Use**
```bash
# Check what's using port 80
sudo netstat -tlnp | grep :80

# Stop conflicting service
sudo systemctl stop apache2  # or nginx
```

#### **2. Services Not Starting**
```bash
# Check logs
docker-compose -f docker-compose.production.yml logs

# Restart all services
docker-compose -f docker-compose.production.yml down
docker-compose -f docker-compose.production.yml up -d
```

#### **3. External Access Issues**
```bash
# Check EC2 security group
# Ensure port 80 is open

# Test locally
curl http://localhost

# Test from EC2
curl http://$(curl -s http://169.254.169.254/latest/meta-data/public-ipv4)
```

## 🎯 **Perfect Scaling Checklist**

- [ ] ✅ Single port (80) exposed externally
- [ ] ✅ Nginx reverse proxy configured
- [ ] ✅ All services running in containers
- [ ] ✅ Health checks implemented
- [ ] ✅ Environment variables secured
- [ ] ✅ SSL certificate installed
- [ ] ✅ Firewall configured
- [ ] ✅ Monitoring set up
- [ ] ✅ Backup strategy in place
- [ ] ✅ Auto-scaling configured

## 🚀 **Next Steps for Enterprise Scaling**

1. **Add Load Balancer** (AWS ALB/ELB)
2. **Implement Auto Scaling Groups**
3. **Set up RDS for database**
4. **Add Redis for caching**
5. **Implement CDN for static assets**
6. **Set up CI/CD pipeline**
7. **Add monitoring (CloudWatch, Prometheus)**
8. **Implement logging aggregation**

---

**🎉 Congratulations!** Your AI SchoolOS is now perfectly set up for production scaling!