#!/usr/bin/env python3
"""
Enhanced AI SchoolOS Backend Starter
This script starts the essential backend services without Docker
"""

import subprocess
import sys
import time
import os
import argparse
import threading
from pathlib import Path
from typing import List, Dict, Optional

class BackendStarter:
    def __init__(self):
        self.project_root = Path.cwd()
        self.backend_dir = self.project_root / "backend"
        self.services = {
            "api-gateway": "API Gateway",
            "auth-service": "Authentication Service", 
            "student-service": "Student Service",
            "staff-service": "Staff Service",
            "ai-service": "AI Service",
            "analytics-service": "Analytics Service",
            "notification-service": "Notification Service",
            "communication-service": "Communication Service",
            "attendance-service": "Attendance Service",
            "timetable-service": "Timetable Service",
            "exam-service": "Exam Service",
            "library-service": "Library Service",
            "homework-service": "Homework Service",
            "fee-service": "Fee Service",
            "transport-service": "Transport Service",
            "config-service": "Configuration Service",
            "super-admin-service": "Super Admin Service"
        }
        
    def run_command(self, cmd: str, description: str, cwd: Optional[Path] = None) -> bool:
        """Run a command with better error handling"""
        print(f"🔄 {description}...")
        try:
            result = subprocess.run(
                cmd, 
                shell=True, 
                check=True, 
                capture_output=True, 
                text=True,
                cwd=cwd
            )
            print(f"✅ {description} completed")
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ {description} failed: {e}")
            if e.stdout:
                print(f"STDOUT: {e.stdout}")
            if e.stderr:
                print(f"STDERR: {e.stderr}")
            return False
        except Exception as e:
            print(f"❌ {description} failed with unexpected error: {e}")
            return False

    def check_requirements(self) -> bool:
        """Check if all required files exist"""
        print("🔍 Checking requirements...")
        
        if not self.backend_dir.exists():
            print("❌ Error: backend directory not found!")
            print("Please run this script from the project root directory")
            return False
            
        # Check for shared requirements
        shared_req = self.backend_dir / "shared" / "requirements.txt"
        if not shared_req.exists():
            print(f"❌ Warning: {shared_req} not found")
            
        # Check for service requirements
        missing_services = []
        for service in self.services.keys():
            service_req = self.backend_dir / "services" / service / "requirements.txt"
            if not service_req.exists():
                missing_services.append(service)
                
        if missing_services:
            print(f"⚠️  Warning: Missing requirements.txt for services: {', '.join(missing_services)}")
            
        print("✅ Requirements check completed")
        return True

    def setup_virtual_environment(self) -> bool:
        """Set up virtual environment if not exists"""
        venv_path = self.project_root / ".venv"
        
        if venv_path.exists():
            print("✅ Virtual environment already exists")
            return True
            
        print("📦 Creating virtual environment...")
        if not self.run_command("python -m venv .venv", "Creating virtual environment"):
            return False
            
        # Activate virtual environment
        if os.name == 'nt':  # Windows
            activate_script = venv_path / "Scripts" / "activate.bat"
        else:  # Unix/Linux/Mac
            activate_script = venv_path / "bin" / "activate"
            
        if not activate_script.exists():
            print("❌ Virtual environment activation script not found")
            return False
            
        return True

    def install_dependencies(self, services_to_install: List[str] = None) -> bool:
        """Install dependencies for specified services"""
        if services_to_install is None:
            services_to_install = list(self.services.keys())
            
        print("📦 Installing Python dependencies...")
        
        # Install shared dependencies first
        shared_req = self.backend_dir / "shared" / "requirements.txt"
        if shared_req.exists():
            if not self.run_command(
                "pip install -r shared/requirements.txt", 
                "Installing shared dependencies",
                cwd=self.backend_dir
            ):
                return False
        
        # Install API Gateway dependencies
        api_gateway_req = self.backend_dir / "api-gateway" / "requirements.txt"
        if api_gateway_req.exists():
            if not self.run_command(
                "pip install -r api-gateway/requirements.txt",
                "Installing API Gateway dependencies",
                cwd=self.backend_dir
            ):
                return False
        
        # Install service dependencies
        for service in services_to_install:
            if service in self.services:
                service_req = self.backend_dir / "services" / service / "requirements.txt"
                if service_req.exists():
                    if not self.run_command(
                        f"pip install -r services/{service}/requirements.txt",
                        f"Installing {self.services[service]} dependencies",
                        cwd=self.backend_dir
                    ):
                        return False
                else:
                    print(f"⚠️  Skipping {service}: requirements.txt not found")
        
        return True

    def start_service(self, service_name: str) -> bool:
        """Start a specific service"""
        service_dir = self.backend_dir / "services" / service_name
        main_file = service_dir / "main.py"
        
        if not main_file.exists():
            print(f"❌ {service_name}: main.py not found")
            return False
            
        print(f"🚀 Starting {self.services.get(service_name, service_name)}...")
        
        try:
            # Start service in background
            process = subprocess.Popen(
                [sys.executable, "main.py"],
                cwd=service_dir,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            print(f"✅ {service_name} started (PID: {process.pid})")
            return True
        except Exception as e:
            print(f"❌ Failed to start {service_name}: {e}")
            return False

    def start_api_gateway(self) -> bool:
        """Start the API Gateway"""
        gateway_dir = self.backend_dir / "api-gateway"
        main_file = gateway_dir / "main.py"
        
        if not main_file.exists():
            print("❌ API Gateway: main.py not found")
            return False
            
        print("🚀 Starting API Gateway...")
        
        try:
            process = subprocess.Popen(
                [sys.executable, "main.py"],
                cwd=gateway_dir,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            print(f"✅ API Gateway started (PID: {process.pid})")
            return True
        except Exception as e:
            print(f"❌ Failed to start API Gateway: {e}")
            return False

    def start_services(self, services_to_start: List[str] = None) -> bool:
        """Start multiple services"""
        if services_to_start is None:
            services_to_start = ["auth-service", "student-service"]
            
        print("🚀 Starting services...")
        
        # Start API Gateway first
        if not self.start_api_gateway():
            return False
            
        # Start other services
        for service in services_to_start:
            if service in self.services:
                if not self.start_service(service):
                    print(f"⚠️  Failed to start {service}, continuing...")
            else:
                print(f"⚠️  Unknown service: {service}")
                
        return True

    def show_help(self):
        """Show help information"""
        print("=" * 60)
        print("AI SchoolOS - Enhanced Backend Starter")
        print("=" * 60)
        print()
        print("Available commands:")
        print("  install [services]  - Install dependencies for specified services")
        print("  start [services]    - Start specified services")
        print("  check               - Check requirements and dependencies")
        print("  setup               - Set up virtual environment")
        print("  help                - Show this help message")
        print()
        print("Available services:")
        for service, description in self.services.items():
            print(f"  {service:<20} - {description}")
        print()
        print("Examples:")
        print("  python start-backend-simple.py install")
        print("  python start-backend-simple.py install auth-service student-service")
        print("  python start-backend-simple.py start auth-service student-service")
        print("  python start-backend-simple.py check")

def main():
    parser = argparse.ArgumentParser(description="AI SchoolOS Backend Starter")
    parser.add_argument("command", nargs="?", default="help", 
                       choices=["install", "start", "check", "setup", "help"],
                       help="Command to execute")
    parser.add_argument("services", nargs="*", help="Services to operate on")
    
    args = parser.parse_args()
    
    starter = BackendStarter()
    
    if args.command == "help":
        starter.show_help()
        return
        
    if args.command == "check":
        starter.check_requirements()
        return
        
    if args.command == "setup":
        starter.setup_virtual_environment()
        return
        
    if args.command == "install":
        if not starter.check_requirements():
            return
        starter.install_dependencies(args.services)
        return
        
    if args.command == "start":
        if not starter.check_requirements():
            return
        starter.start_services(args.services)
        return

if __name__ == "__main__":
    main() 