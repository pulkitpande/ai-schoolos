#!/usr/bin/env python3
"""
AI SchoolOS Service Monitor
Monitors the status of running backend services
"""

import psutil
import time
import argparse
from pathlib import Path
from typing import Dict, List, Optional
import subprocess
import json

class ServiceMonitor:
    def __init__(self):
        self.project_root = Path.cwd()
        self.backend_dir = self.project_root / "backend"
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

    def find_python_processes(self) -> List[Dict]:
        """Find all Python processes that might be our services"""
        python_processes = []
        
        for proc in psutil.process_iter(['pid', 'name', 'cmdline', 'cwd']):
            try:
                if proc.info['name'] and 'python' in proc.info['name'].lower():
                    cmdline = proc.info['cmdline']
                    cwd = proc.info['cwd']
                    
                    if cmdline and cwd:
                        # Check if it's running from our backend directory
                        if str(self.backend_dir) in str(cwd):
                            python_processes.append({
                                'pid': proc.info['pid'],
                                'name': proc.info['name'],
                                'cmdline': cmdline,
                                'cwd': cwd,
                                'status': proc.status()
                            })
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
                
        return python_processes

    def check_port_status(self, port: int) -> bool:
        """Check if a port is in use"""
        try:
            import socket
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            result = sock.connect_ex(('localhost', port))
            sock.close()
            return result == 0
        except:
            return False

    def get_service_status(self, service_name: str) -> Dict:
        """Get detailed status of a specific service"""
        service_info = self.services.get(service_name, {})
        port = service_info.get('port', 0)
        
        # Check if port is in use
        port_status = self.check_port_status(port)
        
        # Find Python processes for this service
        processes = []
        for proc in self.find_python_processes():
            cmdline = ' '.join(proc['cmdline'])
            if service_name in cmdline or f"services/{service_name}" in str(proc['cwd']):
                processes.append(proc)
        
        return {
            'service': service_name,
            'description': service_info.get('description', 'Unknown Service'),
            'port': port,
            'port_status': 'Running' if port_status else 'Not Running',
            'processes': processes,
            'status': 'Running' if processes or port_status else 'Not Running'
        }

    def get_all_services_status(self) -> Dict:
        """Get status of all services"""
        status = {}
        for service_name in self.services.keys():
            status[service_name] = self.get_service_status(service_name)
        return status

    def print_status_table(self, services_status: Dict):
        """Print a formatted status table"""
        print("=" * 80)
        print("AI SchoolOS - Service Status Monitor")
        print("=" * 80)
        print()
        
        print(f"{'Service':<20} {'Port':<8} {'Status':<12} {'Processes':<10}")
        print("-" * 80)
        
        running_count = 0
        total_count = len(services_status)
        
        for service_name, status in services_status.items():
            service_status = status['status']
            port_status = status['port_status']
            process_count = len(status['processes'])
            
            if service_status == 'Running':
                running_count += 1
                status_icon = "🟢"
            else:
                status_icon = "🔴"
            
            print(f"{service_name:<20} {status['port']:<8} {status_icon} {service_status:<12} {process_count:<10}")
        
        print("-" * 80)
        print(f"Summary: {running_count}/{total_count} services running")
        print()

    def print_detailed_status(self, service_name: str):
        """Print detailed status for a specific service"""
        status = self.get_service_status(service_name)
        
        print(f"Detailed Status for {service_name}")
        print("=" * 50)
        print(f"Service: {status['service']}")
        print(f"Description: {status['description']}")
        print(f"Port: {status['port']}")
        print(f"Port Status: {status['port_status']}")
        print(f"Overall Status: {status['status']}")
        print()
        
        if status['processes']:
            print("Running Processes:")
            for proc in status['processes']:
                print(f"  PID: {proc['pid']}")
                print(f"  Status: {proc['status']}")
                print(f"  Working Directory: {proc['cwd']}")
                print(f"  Command: {' '.join(proc['cmdline'])}")
                print()
        else:
            print("No running processes found for this service.")

    def start_service(self, service_name: str) -> bool:
        """Start a specific service"""
        if service_name not in self.services:
            print(f"❌ Unknown service: {service_name}")
            return False
            
        service_dir = self.backend_dir / "services" / service_name
        main_file = service_dir / "main.py"
        
        if not main_file.exists():
            print(f"❌ {service_name}: main.py not found")
            return False
            
        print(f"🚀 Starting {service_name}...")
        
        try:
            process = subprocess.Popen(
                ['python', 'main.py'],
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

    def stop_service(self, service_name: str) -> bool:
        """Stop a specific service"""
        status = self.get_service_status(service_name)
        
        if not status['processes']:
            print(f"⚠️  {service_name} is not running")
            return True
            
        print(f"🛑 Stopping {service_name}...")
        
        for proc in status['processes']:
            try:
                process = psutil.Process(proc['pid'])
                process.terminate()
                print(f"✅ Terminated process {proc['pid']}")
            except Exception as e:
                print(f"❌ Failed to terminate process {proc['pid']}: {e}")
                
        return True

    def restart_service(self, service_name: str) -> bool:
        """Restart a specific service"""
        print(f"🔄 Restarting {service_name}...")
        
        if not self.stop_service(service_name):
            return False
            
        time.sleep(2)  # Wait for processes to terminate
        
        return self.start_service(service_name)

def main():
    parser = argparse.ArgumentParser(description="AI SchoolOS Service Monitor")
    parser.add_argument("command", nargs="?", default="status",
                       choices=["status", "start", "stop", "restart", "detailed"],
                       help="Command to execute")
    parser.add_argument("service", nargs="?", help="Service name for detailed operations")
    
    args = parser.parse_args()
    
    monitor = ServiceMonitor()
    
    if args.command == "status":
        status = monitor.get_all_services_status()
        monitor.print_status_table(status)
        
    elif args.command == "detailed":
        if not args.service:
            print("❌ Please specify a service name for detailed status")
            print("Example: python monitor-services.py detailed auth-service")
            return
            
        monitor.print_detailed_status(args.service)
        
    elif args.command == "start":
        if not args.service:
            print("❌ Please specify a service name to start")
            print("Example: python monitor-services.py start auth-service")
            return
            
        monitor.start_service(args.service)
        
    elif args.command == "stop":
        if not args.service:
            print("❌ Please specify a service name to stop")
            print("Example: python monitor-services.py stop auth-service")
            return
            
        monitor.stop_service(args.service)
        
    elif args.command == "restart":
        if not args.service:
            print("❌ Please specify a service name to restart")
            print("Example: python monitor-services.py restart auth-service")
            return
            
        monitor.restart_service(args.service)

if __name__ == "__main__":
    main() 