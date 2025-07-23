#!/usr/bin/env python3
"""
Generate optimized Dockerfiles for all backend services
"""

import os
import glob

# Template for optimized service Dockerfile
DOCKERFILE_TEMPLATE = '''# Multi-stage build for optimized {service_name}
FROM python:3.11-slim AS builder

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \\
    gcc \\
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY {service_path}/requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir --user -r requirements.txt

# Production stage
FROM python:3.11-slim AS runner

WORKDIR /app

# Copy Python packages from builder
COPY --from=builder /root/.local /root/.local

# Copy application code
COPY {service_path}/ .

# Make sure scripts in .local are usable
ENV PATH=/root/.local/bin:$PATH

# Create non-root user
RUN useradd --create-home --shell /bin/bash app
RUN chown -R app:app /app
USER app

# Expose port
EXPOSE {port}

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \\
    CMD curl -f http://localhost:{port}/health || exit 1

# Start the application
CMD ["python", "main.py"]
'''

# Service configurations
SERVICES = [
    {"name": "auth-service", "path": "services/auth-service", "port": 8001},
    {"name": "student-service", "path": "services/student-service", "port": 8002},
    {"name": "staff-service", "path": "services/staff-service", "port": 8003},
    {"name": "fee-service", "path": "services/fee-service", "port": 8004},
    {"name": "homework-service", "path": "services/homework-service", "port": 8005},
    {"name": "library-service", "path": "services/library-service", "port": 8006},
    {"name": "exam-service", "path": "services/exam-service", "port": 8007},
    {"name": "timetable-service", "path": "services/timetable-service", "port": 8008},
    {"name": "attendance-service", "path": "services/attendance-service", "port": 8009},
    {"name": "transport-service", "path": "services/transport-service", "port": 8010},
    {"name": "communication-service", "path": "services/communication-service", "port": 8011},
    {"name": "analytics-service", "path": "services/analytics-service", "port": 8012},
    {"name": "notification-service", "path": "services/notification-service", "port": 8013},
    {"name": "config-service", "path": "services/config-service", "port": 8014},
    {"name": "super-admin-service", "path": "services/super-admin-service", "port": 8015},
    {"name": "ai-service", "path": "services/ai-service", "port": 8016},
    {"name": "ai-analytics-service", "path": "services/ai-analytics-service", "port": 8017},
]

def generate_dockerfiles():
    """Generate optimized Dockerfiles for all services"""
    backend_dir = "backend"
    
    for service in SERVICES:
        service_path = os.path.join(backend_dir, service["path"])
        dockerfile_path = os.path.join(service_path, "Dockerfile.optimized")
        
        # Check if service directory exists
        if not os.path.exists(service_path):
            print(f"⚠️  Service directory not found: {service_path}")
            continue
        
        # Generate Dockerfile content
        content = DOCKERFILE_TEMPLATE.format(
            service_name=service["name"].replace("-", " ").title(),
            service_path=service["path"],
            port=service["port"]
        )
        
        # Write Dockerfile
        with open(dockerfile_path, 'w') as f:
            f.write(content)
        
        print(f"✅ Generated: {dockerfile_path}")

def main():
    """Main function"""
    print("🚀 Generating optimized Dockerfiles for all services...")
    generate_dockerfiles()
    print("✅ All optimized Dockerfiles generated!")

if __name__ == "__main__":
    main() 