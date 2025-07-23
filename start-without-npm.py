#!/usr/bin/env python3
"""
AI SchoolOS - Simplified Full Stack Starter
Starts backend and frontend without npm install issues
"""

import subprocess
import sys
import time
import os
import signal
from pathlib import Path
from typing import List, Optional
import argparse

class SimpleFullStackStarter:
    def __init__(self):
        self.project_root = Path.cwd()
        self.backend_dir = self.project_root / "backend"
        self.frontend_dir = self.project_root / "frontend"
        self.processes = []
        self.running = True
        
        # Default services to start
        self.default_backend_services = ["auth-service", "student-service"]
        
        # Service configurations
        self.services = {
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

    def setup_signal_handlers(self):
        """Setup signal handlers for graceful shutdown"""
        def signal_handler(signum, frame):
            print("\n🛑 Received shutdown signal. Stopping all services...")
            self.running = False
            self.stop_all_services()
            sys.exit(0)
        
        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)

    def check_requirements(self) -> bool:
        """Check if all required components are available"""
        print("🔍 Checking requirements...")
        
        # Check backend directory
        if not self.backend_dir.exists():
            print("❌ Error: backend directory not found!")
            return False
            
        # Check frontend directory
        if not self.frontend_dir.exists():
            print("❌ Error: frontend directory not found!")
            return False
            
        # Check Python
        try:
            subprocess.run([sys.executable, "--version"], check=True, capture_output=True)
            print("✅ Python is available")
        except (subprocess.CalledProcessError, FileNotFoundError):
            print("❌ Error: Python is not available")
            return False
            
        print("✅ All requirements met")
        return True

    def check_frontend_dependencies(self) -> bool:
        """Check if frontend dependencies are installed"""
        node_modules = self.frontend_dir / "node_modules"
        package_json = self.frontend_dir / "package.json"
        
        if not package_json.exists():
            print("❌ package.json not found in frontend directory")
            return False
            
        if not node_modules.exists():
            print("⚠️  node_modules not found. Frontend dependencies need to be installed.")
            print("💡 Run: cd frontend && npm install")
            print("💡 Or run: python fix-npm-install.py")
            return False
            
        # Check if Next.js is installed
        next_dir = node_modules / "next"
        if not next_dir.exists():
            print("⚠️  Next.js not found in node_modules")
            return False
            
        print("✅ Frontend dependencies are installed")
        return True

    def create_frontend_env(self) -> bool:
        """Create frontend environment file if it doesn't exist"""
        env_file = self.frontend_dir / ".env.local"
        
        if env_file.exists():
            print("✅ Frontend environment file already exists")
            return True
            
        print("🔧 Creating frontend environment file...")
        
        env_content = """# AI SchoolOS Frontend Environment Configuration
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_APP_NAME=AI SchoolOS
NEXT_PUBLIC_APP_VERSION=1.0.0
"""
        
        try:
            with open(env_file, 'w') as f:
                f.write(env_content)
            print("✅ Frontend environment file created")
            return True
        except Exception as e:
            print(f"❌ Failed to create frontend environment file: {e}")
            return False

    def start_backend_service(self, service_name: str) -> Optional[subprocess.Popen]:
        """Start a specific backend service"""
        if service_name == "api-gateway":
            service_dir = self.backend_dir / "api-gateway"
        else:
            service_dir = self.backend_dir / "services" / service_name
            
        main_file = service_dir / "main.py"
        
        if not main_file.exists():
            print(f"⚠️  {service_name}: main.py not found, skipping")
            return None
            
        print(f"🚀 Starting {service_name}...")
        
        try:
            process = subprocess.Popen(
                [sys.executable, "main.py"],
                cwd=service_dir,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            print(f"✅ {service_name} started (PID: {process.pid})")
            return process
        except Exception as e:
            print(f"❌ Failed to start {service_name}: {e}")
            return None

    def start_backend_services(self, services: List[str]) -> bool:
        """Start multiple backend services"""
        print("🚀 Starting backend services...")
        
        # Start API Gateway first
        api_gateway_process = self.start_backend_service("api-gateway")
        if api_gateway_process:
            self.processes.append(("api-gateway", api_gateway_process))
            
        # Wait a bit for API Gateway to start
        time.sleep(2)
        
        # Start other services
        for service in services:
            if service in self.services:
                process = self.start_backend_service(service)
                if process:
                    self.processes.append((service, process))
                time.sleep(1)  # Small delay between services
            else:
                print(f"⚠️  Unknown service: {service}")
                
        return len(self.processes) > 0

    def start_frontend(self) -> Optional[subprocess.Popen]:
        """Start the frontend development server"""
        print("🌐 Starting frontend development server...")
        
        try:
            process = subprocess.Popen(
                ["npm", "run", "dev"],
                cwd=self.frontend_dir,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            print(f"✅ Frontend started (PID: {process.pid})")
            return process
        except Exception as e:
            print(f"❌ Failed to start frontend: {e}")
            return None

    def wait_for_services(self, timeout: int = 30):
        """Wait for services to be ready"""
        print(f"⏳ Waiting for services to be ready (timeout: {timeout}s)...")
        
        start_time = time.time()
        while time.time() - start_time < timeout:
            # Check if API Gateway is responding
            try:
                import socket
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                result = sock.connect_ex(('localhost', 8000))
                sock.close()
                if result == 0:
                    print("✅ API Gateway is ready")
                    break
            except:
                pass
                
            time.sleep(1)
        else:
            print("⚠️  Timeout waiting for services to be ready")

    def print_status(self):
        """Print current status of all services"""
        print("\n" + "=" * 60)
        print("AI SchoolOS - Full Stack Status")
        print("=" * 60)
        
        print(f"Backend Services: {len(self.processes)} running")
        for service_name, process in self.processes:
            status = "Running" if process.poll() is None else "Stopped"
            print(f"  {service_name}: {status} (PID: {process.pid})")
            
        print("\nAccess URLs:")
        print("  🌐 Frontend: http://localhost:3000")
        print("  🔗 API Gateway: http://localhost:8000")
        print("  📊 Service Monitor: python monitor-services.py status")
        print("\nPress Ctrl+C to stop all services")
        print("=" * 60)

    def stop_all_services(self):
        """Stop all running services"""
        print("🛑 Stopping all services...")
        
        for service_name, process in self.processes:
            try:
                print(f"Stopping {service_name} (PID: {process.pid})...")
                process.terminate()
                process.wait(timeout=5)
                print(f"✅ {service_name} stopped")
            except subprocess.TimeoutExpired:
                print(f"⚠️  Force killing {service_name}")
                process.kill()
            except Exception as e:
                print(f"❌ Error stopping {service_name}: {e}")

    def run(self, backend_services: List[str] = None, skip_frontend_check: bool = False):
        """Main run method"""
        if backend_services is None:
            backend_services = self.default_backend_services
            
        print("🚀 Starting AI SchoolOS Full Stack (Simplified)...")
        print("=" * 50)
        
        # Setup signal handlers
        self.setup_signal_handlers()
        
        # Check requirements
        if not self.check_requirements():
            return False
            
        # Check frontend dependencies (unless skipped)
        if not skip_frontend_check:
            if not self.check_frontend_dependencies():
                print("\n💡 To install frontend dependencies:")
                print("   1. Run: python fix-npm-install.py")
                print("   2. Or manually: cd frontend && npm install")
                print("   3. Then run this script again")
                return False
                
        # Create frontend environment
        if not self.create_frontend_env():
            return False
            
        # Start backend services
        if not self.start_backend_services(backend_services):
            print("⚠️  No backend services started")
            
        # Wait for backend services
        self.wait_for_services()
        
        # Start frontend
        frontend_process = self.start_frontend()
        if frontend_process:
            self.processes.append(("frontend", frontend_process))
            
        # Print status
        self.print_status()
        
        # Keep running until interrupted
        try:
            while self.running:
                time.sleep(1)
                # Check if any processes have died
                for service_name, process in self.processes[:]:
                    if process.poll() is not None:
                        print(f"⚠️  {service_name} has stopped unexpectedly")
                        self.processes.remove((service_name, process))
        except KeyboardInterrupt:
            pass
        finally:
            self.stop_all_services()
            print("✅ All services stopped")

def main():
    parser = argparse.ArgumentParser(description="AI SchoolOS Simplified Full Stack Starter")
    parser.add_argument("--services", nargs="*", 
                       help="Backend services to start (default: auth-service student-service)")
    parser.add_argument("--skip-frontend-check", action="store_true",
                       help="Skip checking frontend dependencies")
    
    args = parser.parse_args()
    
    starter = SimpleFullStackStarter()
    starter.run(
        backend_services=args.services,
        skip_frontend_check=args.skip_frontend_check
    )

if __name__ == "__main__":
    main() 