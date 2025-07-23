#!/usr/bin/env python3
"""
Script to fix all service Dockerfiles with correct paths for build context.
"""

import os
from pathlib import Path

# Service configurations
SERVICES = [
    "student-service", "staff-service", "fee-service", "exam-service",
    "attendance-service", "homework-service", "timetable-service", "library-service",
    "transport-service", "communication-service", "analytics-service",
    "notification-service", "config-service", "super-admin-service"
]

def fix_dockerfile(service_name: str):
    """Fix the Dockerfile for a specific service."""
    dockerfile_path = Path(f"backend/services/{service_name}/Dockerfile")
    
    if not dockerfile_path.exists():
        print(f"Dockerfile not found for {service_name}")
        return
    
    # Read current content
    with open(dockerfile_path, 'r') as f:
        content = f.read()
    
    # Fix the paths
    content = content.replace(
        "COPY requirements.txt .",
        f"COPY services/{service_name}/requirements.txt ."
    )
    content = content.replace(
        "COPY ../../shared ./shared",
        "COPY shared ./shared"
    )
    content = content.replace(
        "COPY . .",
        f"COPY services/{service_name}/ ."
    )
    
    # Write back
    with open(dockerfile_path, 'w') as f:
        f.write(content)
    
    print(f"Fixed Dockerfile for {service_name}")

def main():
    """Fix all service Dockerfiles."""
    print("Fixing Dockerfiles for all services...")
    
    for service in SERVICES:
        fix_dockerfile(service)
    
    print("All Dockerfiles fixed!")

if __name__ == "__main__":
    main() 