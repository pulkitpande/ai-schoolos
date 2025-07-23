# AI SchoolOS - Complete School Management System

A comprehensive school management system built with Next.js frontend and Python microservices backend, designed for modern educational institutions.

## 🚀 Features

### Frontend (Next.js)
- Modern React-based UI with TypeScript
- Responsive design with Tailwind CSS
- Real-time updates and notifications
- Role-based access control
- Interactive dashboards

### Backend (Python Microservices)
- **API Gateway**: Central routing and authentication
- **Auth Service**: User authentication and authorization
- **Student Service**: Student management and records
- **Staff Service**: Staff and teacher management
- **Attendance Service**: Attendance tracking
- **Exam Service**: Exam and assessment management
- **Fee Service**: Fee collection and management
- **Library Service**: Library book management
- **Transport Service**: Transportation tracking
- **Communication Service**: Messaging and notifications
- **Analytics Service**: Data analytics and reporting
- **AI Service**: AI-powered insights and recommendations

## 🛠️ Technology Stack

### Frontend
- **Next.js 14** - React framework
- **TypeScript** - Type safety
- **Tailwind CSS** - Styling
- **Axios** - HTTP client

### Backend
- **Python 3.11** - Core language
- **FastAPI** - Web framework
- **SQLAlchemy** - ORM
- **PostgreSQL** - Database
- **Redis** - Caching
- **Docker** - Containerization

### Infrastructure
- **Docker Compose** - Multi-container orchestration
- **Nginx** - Reverse proxy
- **PostgreSQL** - Primary database
- **Redis** - Session storage

## 📁 Project Structure

```
ai-schoolos/
├── frontend/                 # Next.js frontend application
│   ├── src/
│   ├── public/
│   ├── package.json
│   └── Dockerfile.development
├── backend/                  # Python microservices
│   ├── api-gateway/         # API Gateway service
│   ├── services/            # Individual microservices
│   │   ├── auth-service/
│   │   ├── student-service/
│   │   ├── staff-service/
│   │   ├── attendance-service/
│   │   ├── exam-service/
│   │   ├── fee-service/
│   │   ├── library-service/
│   │   ├── transport-service/
│   │   ├── communication-service/
│   │   ├── analytics-service/
│   │   └── ai-service/
│   ├── shared/              # Shared utilities and models
│   └── Dockerfile.*         # Docker configurations
├── docker-compose.yml       # Full stack orchestration
├── docker-compose.simple.yml # Minimal setup
├── scripts/                 # Utility scripts
└── docs/                   # Documentation
```

## 🚀 Quick Start

### Prerequisites
- Docker and Docker Compose
- Git
- Node.js 18+ (for local development)
- Python 3.11+ (for local development)

### Option 1: Docker (Recommended)

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-username/ai-schoolos.git
   cd ai-schoolos
   ```

2. **Start all services**
   ```bash
   docker-compose -f docker-compose.simple.yml up -d --build
   ```

3. **Access the application**
   - Frontend: http://localhost:3000
   - API Gateway: http://localhost:8000
   - Auth Service: http://localhost:8001
   - Student Service: http://localhost:8002

### Option 2: Local Development

1. **Start backend services**
   ```bash
   python start-backend-simple.py
   ```

2. **Start frontend**
   ```bash
   cd frontend
   npm install
   npm run dev
   ```

## 🐳 Docker Deployment

### Development Environment
```bash
docker-compose -f docker-compose.development.yml up -d
```

### Production Environment
```bash
docker-compose -f docker-compose.production.yml up -d
```

### Minimal Setup (Recommended for testing)
```bash
docker-compose -f docker-compose.simple.yml up -d
```

## 📊 Monitoring

### Check Service Status
```bash
docker-compose -f docker-compose.simple.yml ps
```

### View Logs
```bash
# All services
docker-compose -f docker-compose.simple.yml logs

# Specific service
docker-compose -f docker-compose.simple.yml logs frontend
```

### Health Checks
- Frontend: http://localhost:3000
- API Gateway: http://localhost:8000/health
- Auth Service: http://localhost:8001/health
- Student Service: http://localhost:8002/health

## 🔧 Configuration

### Environment Variables
Create `.env` files in respective directories:

**Frontend (.env.local)**
```
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_APP_NAME=AI SchoolOS
```

**Backend (.env)**
```
DATABASE_URL=postgresql://user:password@localhost:5432/schoolos
REDIS_URL=redis://localhost:6379
JWT_SECRET=your-secret-key
```

## 🛠️ Development

### Adding New Services
1. Create service directory in `backend/services/`
2. Add Dockerfile configuration
3. Update docker-compose files
4. Add health check endpoints

### Frontend Development
```bash
cd frontend
npm install
npm run dev
```

### Backend Development
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## 📚 Documentation

- [Docker Deployment Guide](DOCKER_DEPLOYMENT_GUIDE.md)
- [NPM Issues Solution](NPM_ISSUES_SOLUTION.md)
- [Backend Starter Guide](BACKEND_STARTER_README.md)
- [Testing Guide](TESTING_GUIDE.md)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License.

## 🆘 Troubleshooting

### Common Issues

1. **Docker build fails**
   - Clear Docker cache: `docker system prune -a`
   - Check available disk space
   - Use simplified compose file

2. **Services not starting**
   - Check logs: `docker-compose logs`
   - Verify ports are available
   - Check environment variables

3. **Frontend not loading**
   - Verify API URL configuration
   - Check network connectivity
   - Clear browser cache

### Support
- Check [Troubleshooting Guide](TROUBLESHOOTING.md)
- Review [Working Solution](WORKING_SOLUTION.md)
- Open an issue on GitHub

## 🎯 Roadmap

- [ ] Mobile application
- [ ] Advanced analytics dashboard
- [ ] AI-powered insights
- [ ] Multi-language support
- [ ] Advanced reporting
- [ ] Integration with external systems

---

**Built with ❤️ for modern education** 