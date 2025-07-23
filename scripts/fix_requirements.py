#!/usr/bin/env python3
"""
Script to fix requirements.txt files by replacing shared requirements with direct dependencies
"""

import os
import glob

# Direct dependencies for all services
DIRECT_DEPS = """# Core dependencies
fastapi>=0.104.0
uvicorn[standard]>=0.24.0
pydantic>=2.5.0
python-multipart>=0.0.6
python-jose[cryptography]>=3.3.0
passlib[bcrypt]>=1.7.4
python-dotenv>=1.0.0
sqlalchemy>=2.0.0
psycopg2-binary>=2.9.0
redis>=5.0.0
pymongo>=4.6.0
minio>=7.2.0
alembic>=1.13.0
"""

def fix_requirements_file(file_path):
    """Fix a requirements.txt file by replacing shared requirements with direct deps"""
    try:
        with open(file_path, 'w') as f:
            f.write(DIRECT_DEPS)
        print(f"Fixed: {file_path}")
    except Exception as e:
        print(f"Error fixing {file_path}: {e}")

def main():
    """Main function to fix all requirements.txt files"""
    # Find all requirements.txt files in services
    service_patterns = [
        "backend/services/*/requirements.txt",
        "backend/api-gateway/requirements.txt"
    ]
    
    for pattern in service_patterns:
        for file_path in glob.glob(pattern):
            fix_requirements_file(file_path)

if __name__ == "__main__":
    main() 