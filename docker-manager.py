#!/usr/bin/env python3
"""
AI SchoolOS - Docker Manager
Manages Docker containers for development and production environments
"""

import subprocess
import sys
import time
import os
import argparse
from pathlib import Path
from typing import List, Dict, Optional

class DockerManager:
    def __init__(self):
        self.project_root = Path.cwd()
        self.docker_compose_prod = self.project_root / "docker-compose.production.yml"
        self.docker_compose_dev = self.project_root / "docker-compose.development.yml"
        
        self.services = {
            "frontend": {"port": 3000, "description": "Frontend Application"},
            "api-gateway": {"port": 8000, "description": "API Gateway"},
            "auth-service": {"port": 8001, "description": "Authentication Service"},
            "student-service": {"port": 8002, "description": "Student Service"},
            "staff-service": {"port": 8003, "description": "Staff Service"},
            "ai-service": {"port": 8004, "description": "AI Service"},
            "analytics-service": {"port": 8005, "description": "Analytics Service"},
            "notification-service": {"port": 8006, "description": "Notification Service"},
            "communication-service": {"port": 8007, "description": "Communication Service"},
            "attendance-service": {"port": 8008, "description": "Attendance Service"},
            "timetable-service": {"port": 8009, "description": "Timetable Service"},
            "exam-service": {"port": 8010, "description": "Exam Service"},
            "library-service": {"port": 8011, "description": "Library Service"},
            "homework-service": {"port": 8012, "description": "Homework Service"},
            "fee-service": {"port": 8013, "description": "Fee Service"},
            "transport-service": {"port": 8014, "description": "Transport Service"},
            "config-service": {"port": 8015, "description": "Configuration Service"},
            "super-admin-service": {"port": 8016, "description": "Super Admin Service"}
        }

    def check_docker(self) -> bool:
        """Check if Docker is available"""
        try:
            result = subprocess.run(
                ["docker", "--version"],
                capture_output=True,
                text=True,
                check=True
            )
            print(f"✅ Docker: {result.stdout.strip()}")
            
            result = subprocess.run(
                ["docker-compose", "--version"],
                capture_output=True,
                text=True,
                check=True
            )
            print(f"✅ Docker Compose: {result.stdout.strip()}")
            return True
        except (subprocess.CalledProcessError, FileNotFoundError) as e:
            print(f"❌ Docker not available: {e}")
            return False

    def check_requirements(self) -> bool:
        """Check if all required files exist"""
        print("🔍 Checking Docker requirements...")
        
        # Check Docker Compose files
        if not self.docker_compose_prod.exists():
            print(f"❌ {self.docker_compose_prod} not found")
            return False
            
        if not self.docker_compose_dev.exists():
            print(f"❌ {self.docker_compose_dev} not found")
            return False
            
        # Check frontend Dockerfiles
        frontend_prod_dockerfile = self.project_root / "frontend" / "Dockerfile.production"
        frontend_dev_dockerfile = self.project_root / "frontend" / "Dockerfile.development"
        
        if not frontend_prod_dockerfile.exists():
            print(f"❌ {frontend_prod_dockerfile} not found")
            return False
            
        if not frontend_dev_dockerfile.exists():
            print(f"❌ {frontend_dev_dockerfile} not found")
            return False
            
        # Check backend Dockerfiles
        backend_api_dockerfile = self.project_root / "backend" / "Dockerfile.api-gateway"
        backend_service_dockerfile = self.project_root / "backend" / "Dockerfile.service"
        
        if not backend_api_dockerfile.exists():
            print(f"❌ {backend_api_dockerfile} not found")
            return False
            
        if not backend_service_dockerfile.exists():
            print(f"❌ {backend_service_dockerfile} not found")
            return False
            
        print("✅ All Docker requirements met")
        return True

    def build_images(self, environment: str = "development", services: List[str] = None) -> bool:
        """Build Docker images"""
        compose_file = self.docker_compose_dev if environment == "development" else self.docker_compose_prod
        
        print(f"🔨 Building Docker images for {environment} environment...")
        
        try:
            cmd = ["docker-compose", "-f", str(compose_file), "build"]
            if services:
                cmd.extend(services)
                
            result = subprocess.run(cmd, check=True, capture_output=True, text=True)
            print("✅ Docker images built successfully")
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to build Docker images: {e}")
            if e.stdout:
                print(f"STDOUT: {e.stdout}")
            if e.stderr:
                print(f"STDERR: {e.stderr}")
            return False

    def start_services(self, environment: str = "development", services: List[str] = None) -> bool:
        """Start Docker services"""
        compose_file = self.docker_compose_dev if environment == "development" else self.docker_compose_prod
        
        print(f"🚀 Starting Docker services for {environment} environment...")
        
        try:
            cmd = ["docker-compose", "-f", str(compose_file), "up", "-d"]
            if services:
                cmd.extend(services)
                
            result = subprocess.run(cmd, check=True, capture_output=True, text=True)
            print("✅ Docker services started successfully")
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to start Docker services: {e}")
            if e.stdout:
                print(f"STDOUT: {e.stdout}")
            if e.stderr:
                print(f"STDERR: {e.stderr}")
            return False

    def stop_services(self, environment: str = "development") -> bool:
        """Stop Docker services"""
        compose_file = self.docker_compose_dev if environment == "development" else self.docker_compose_prod
        
        print(f"🛑 Stopping Docker services for {environment} environment...")
        
        try:
            result = subprocess.run(
                ["docker-compose", "-f", str(compose_file), "down"],
                check=True,
                capture_output=True,
                text=True
            )
            print("✅ Docker services stopped successfully")
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to stop Docker services: {e}")
            return False

    def restart_services(self, environment: str = "development") -> bool:
        """Restart Docker services"""
        print(f"🔄 Restarting Docker services for {environment} environment...")
        
        if not self.stop_services(environment):
            return False
            
        time.sleep(2)
        
        return self.start_services(environment)

    def show_status(self, environment: str = "development") -> bool:
        """Show status of Docker services"""
        compose_file = self.docker_compose_dev if environment == "development" else self.docker_compose_prod
        
        print(f"📊 Docker services status for {environment} environment:")
        print("=" * 60)
        
        try:
            result = subprocess.run(
                ["docker-compose", "-f", str(compose_file), "ps"],
                check=True,
                capture_output=True,
                text=True
            )
            print(result.stdout)
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to get service status: {e}")
            return False

    def show_logs(self, environment: str = "development", service: str = None, follow: bool = False) -> bool:
        """Show logs of Docker services"""
        compose_file = self.docker_compose_dev if environment == "development" else self.docker_compose_prod
        
        print(f"📋 Showing logs for {environment} environment...")
        
        try:
            cmd = ["docker-compose", "-f", str(compose_file), "logs"]
            if follow:
                cmd.append("-f")
            if service:
                cmd.append(service)
                
            result = subprocess.run(cmd, check=True, capture_output=True, text=True)
            print(result.stdout)
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to get logs: {e}")
            return False

    def clean_up(self, environment: str = "development") -> bool:
        """Clean up Docker resources"""
        compose_file = self.docker_compose_dev if environment == "development" else self.docker_compose_prod
        
        print(f"🧹 Cleaning up Docker resources for {environment} environment...")
        
        try:
            # Stop and remove containers
            subprocess.run(
                ["docker-compose", "-f", str(compose_file), "down", "--volumes", "--remove-orphans"],
                check=True,
                capture_output=True,
                text=True
            )
            
            # Remove images
            subprocess.run(
                ["docker-compose", "-f", str(compose_file), "down", "--rmi", "all"],
                check=True,
                capture_output=True,
                text=True
            )
            
            print("✅ Docker resources cleaned up successfully")
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to clean up Docker resources: {e}")
            return False

    def health_check(self, environment: str = "development") -> bool:
        """Check health of all services"""
        compose_file = self.docker_compose_dev if environment == "development" else self.docker_compose_prod
        
        print(f"🏥 Checking health of services for {environment} environment...")
        
        try:
            result = subprocess.run(
                ["docker-compose", "-f", str(compose_file), "ps"],
                check=True,
                capture_output=True,
                text=True
            )
            
            lines = result.stdout.strip().split('\n')
            healthy_count = 0
            total_count = 0
            
            for line in lines:
                if 'Up' in line and 'healthy' in line:
                    healthy_count += 1
                if 'Up' in line:
                    total_count += 1
                    
            print(f"Health Status: {healthy_count}/{total_count} services healthy")
            
            if healthy_count == total_count:
                print("✅ All services are healthy")
                return True
            else:
                print("⚠️  Some services are not healthy")
                return False
                
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to check health: {e}")
            return False

    def run_full_stack(self, environment: str = "development") -> bool:
        """Run the complete full stack"""
        print(f"🚀 Starting AI SchoolOS Full Stack ({environment})...")
        print("=" * 60)
        
        # Check requirements
        if not self.check_docker():
            return False
            
        if not self.check_requirements():
            return False
            
        # Build images
        if not self.build_images(environment):
            return False
            
        # Start services
        if not self.start_services(environment):
            return False
            
        # Wait for services to be ready
        print("⏳ Waiting for services to be ready...")
        time.sleep(30)
        
        # Check health
        if not self.health_check(environment):
            print("⚠️  Some services may not be ready yet")
            
        # Show status
        self.show_status(environment)
        
        print("\n🎉 Full stack started successfully!")
        print(f"🌐 Frontend: http://localhost:3000")
        print(f"🔗 API Gateway: http://localhost:8000")
        print(f"📊 Service Status: docker-compose -f docker-compose.{environment}.yml ps")
        print(f"📋 Logs: docker-compose -f docker-compose.{environment}.yml logs -f")
        print(f"🛑 Stop: docker-compose -f docker-compose.{environment}.yml down")
        
        return True

def main():
    parser = argparse.ArgumentParser(description="AI SchoolOS Docker Manager")
    parser.add_argument("command", 
                       choices=["build", "start", "stop", "restart", "status", "logs", "clean", "health", "run"],
                       help="Command to execute")
    parser.add_argument("--environment", "-e", default="development",
                       choices=["development", "production"],
                       help="Environment to operate on")
    parser.add_argument("--services", "-s", nargs="*",
                       help="Specific services to operate on")
    parser.add_argument("--follow", "-f", action="store_true",
                       help="Follow logs (for logs command)")
    
    args = parser.parse_args()
    
    manager = DockerManager()
    
    if args.command == "build":
        manager.build_images(args.environment, args.services)
    elif args.command == "start":
        manager.start_services(args.environment, args.services)
    elif args.command == "stop":
        manager.stop_services(args.environment)
    elif args.command == "restart":
        manager.restart_services(args.environment)
    elif args.command == "status":
        manager.show_status(args.environment)
    elif args.command == "logs":
        service = args.services[0] if args.services else None
        manager.show_logs(args.environment, service, args.follow)
    elif args.command == "clean":
        manager.clean_up(args.environment)
    elif args.command == "health":
        manager.health_check(args.environment)
    elif args.command == "run":
        manager.run_full_stack(args.environment)

if __name__ == "__main__":
    main() 