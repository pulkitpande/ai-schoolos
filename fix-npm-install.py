#!/usr/bin/env python3
"""
AI SchoolOS - NPM Install Fixer
Diagnoses and fixes common npm install issues that cause infinite hanging
"""

import subprocess
import sys
import time
import os
import shutil
from pathlib import Path
import json

class NPMFixer:
    def __init__(self):
        self.project_root = Path.cwd()
        self.frontend_dir = self.project_root / "frontend"
        self.node_modules = self.frontend_dir / "node_modules"
        self.package_lock = self.frontend_dir / "package-lock.json"
        self.npm_cache_dir = None
        
    def get_npm_cache_dir(self):
        """Get npm cache directory"""
        try:
            result = subprocess.run(
                ["npm", "config", "get", "cache"],
                capture_output=True,
                text=True,
                check=True
            )
            return Path(result.stdout.strip())
        except:
            return None

    def check_npm_status(self):
        """Check npm and Node.js status"""
        print("🔍 Checking npm and Node.js status...")
        
        # Check Node.js version
        try:
            result = subprocess.run(
                ["node", "--version"],
                capture_output=True,
                text=True,
                check=True
            )
            print(f"✅ Node.js version: {result.stdout.strip()}")
        except Exception as e:
            print(f"❌ Node.js not available: {e}")
            return False
            
        # Check npm version
        try:
            result = subprocess.run(
                ["npm", "--version"],
                capture_output=True,
                text=True,
                check=True
            )
            print(f"✅ npm version: {result.stdout.strip()}")
        except Exception as e:
            # Try alternative method using Node.js
            try:
                result = subprocess.run(
                    ["node", "-e", "console.log(require('child_process').execSync('npm --version').toString())"],
                    capture_output=True,
                    text=True,
                    check=True
                )
                print(f"✅ npm version: {result.stdout.strip()}")
            except Exception as e2:
                print(f"❌ npm not available: {e}")
                return False
            
        # Check npm cache
        cache_dir = self.get_npm_cache_dir()
        if cache_dir:
            print(f"📁 npm cache directory: {cache_dir}")
            if cache_dir.exists():
                cache_size = sum(f.stat().st_size for f in cache_dir.rglob('*') if f.is_file())
                print(f"📊 Cache size: {cache_size / (1024*1024):.1f} MB")
            else:
                print("⚠️  npm cache directory doesn't exist")
        else:
            print("⚠️  Could not determine npm cache directory")
            
        return True

    def clear_npm_cache(self):
        """Clear npm cache"""
        print("🧹 Clearing npm cache...")
        try:
            result = subprocess.run(
                ["npm", "cache", "clean", "--force"],
                capture_output=True,
                text=True,
                check=True
            )
            print("✅ npm cache cleared")
            return True
        except Exception as e:
            print(f"❌ Failed to clear npm cache: {e}")
            return False

    def remove_node_modules(self):
        """Remove node_modules directory"""
        if self.node_modules.exists():
            print("🗑️  Removing node_modules directory...")
            try:
                shutil.rmtree(self.node_modules)
                print("✅ node_modules removed")
                return True
            except Exception as e:
                print(f"❌ Failed to remove node_modules: {e}")
                return False
        else:
            print("ℹ️  node_modules directory doesn't exist")
            return True

    def remove_package_lock(self):
        """Remove package-lock.json"""
        if self.package_lock.exists():
            print("🗑️  Removing package-lock.json...")
            try:
                self.package_lock.unlink()
                print("✅ package-lock.json removed")
                return True
            except Exception as e:
                print(f"❌ Failed to remove package-lock.json: {e}")
                return False
        else:
            print("ℹ️  package-lock.json doesn't exist")
            return True

    def check_network_connectivity(self):
        """Check network connectivity to npm registry"""
        print("🌐 Checking network connectivity...")
        
        # Check if we can reach npm registry
        try:
            result = subprocess.run(
                ["npm", "ping"],
                capture_output=True,
                text=True,
                timeout=30
            )
            if result.returncode == 0:
                print("✅ npm registry is accessible")
                return True
            else:
                print("❌ npm registry is not accessible")
                return False
        except subprocess.TimeoutExpired:
            print("❌ npm registry connection timed out")
            return False
        except Exception as e:
            print(f"❌ Network check failed: {e}")
            return False

    def try_npm_install_with_timeout(self, timeout_minutes=10):
        """Try npm install with timeout"""
        print(f"📦 Attempting npm install (timeout: {timeout_minutes} minutes)...")
        
        try:
            result = subprocess.run(
                ["npm", "install"],
                cwd=self.frontend_dir,
                capture_output=True,
                text=True,
                timeout=timeout_minutes * 60
            )
            
            if result.returncode == 0:
                print("✅ npm install completed successfully")
                return True
            else:
                print(f"❌ npm install failed with exit code {result.returncode}")
                if result.stderr:
                    print(f"Error: {result.stderr}")
                return False
                
        except subprocess.TimeoutExpired:
            print(f"❌ npm install timed out after {timeout_minutes} minutes")
            return False
        except Exception as e:
            print(f"❌ npm install failed: {e}")
            return False

    def try_alternative_install_methods(self):
        """Try alternative installation methods"""
        print("🔄 Trying alternative installation methods...")
        
        # Method 1: npm install --no-optional
        print("📦 Trying npm install --no-optional...")
        try:
            result = subprocess.run(
                ["npm", "install", "--no-optional"],
                cwd=self.frontend_dir,
                capture_output=True,
                text=True,
                timeout=300  # 5 minutes
            )
            if result.returncode == 0:
                print("✅ npm install --no-optional completed successfully")
                return True
        except subprocess.TimeoutExpired:
            print("❌ npm install --no-optional timed out")
        except Exception as e:
            print(f"❌ npm install --no-optional failed: {e}")
            
        # Method 2: npm install --legacy-peer-deps
        print("📦 Trying npm install --legacy-peer-deps...")
        try:
            result = subprocess.run(
                ["npm", "install", "--legacy-peer-deps"],
                cwd=self.frontend_dir,
                capture_output=True,
                text=True,
                timeout=300  # 5 minutes
            )
            if result.returncode == 0:
                print("✅ npm install --legacy-peer-deps completed successfully")
                return True
        except subprocess.TimeoutExpired:
            print("❌ npm install --legacy-peer-deps timed out")
        except Exception as e:
            print(f"❌ npm install --legacy-peer-deps failed: {e}")
            
        # Method 3: npm install --force
        print("📦 Trying npm install --force...")
        try:
            result = subprocess.run(
                ["npm", "install", "--force"],
                cwd=self.frontend_dir,
                capture_output=True,
                text=True,
                timeout=300  # 5 minutes
            )
            if result.returncode == 0:
                print("✅ npm install --force completed successfully")
                return True
        except subprocess.TimeoutExpired:
            print("❌ npm install --force timed out")
        except Exception as e:
            print(f"❌ npm install --force failed: {e}")
            
        return False

    def check_package_json(self):
        """Check and validate package.json"""
        package_json = self.frontend_dir / "package.json"
        
        if not package_json.exists():
            print("❌ package.json not found in frontend directory")
            return False
            
        try:
            with open(package_json, 'r') as f:
                data = json.load(f)
                
            print("✅ package.json is valid JSON")
            print(f"📦 Package name: {data.get('name', 'Unknown')}")
            print(f"📦 Package version: {data.get('version', 'Unknown')}")
            
            dependencies = data.get('dependencies', {})
            dev_dependencies = data.get('devDependencies', {})
            
            print(f"📦 Dependencies: {len(dependencies)}")
            print(f"📦 Dev Dependencies: {len(dev_dependencies)}")
            
            return True
        except json.JSONDecodeError as e:
            print(f"❌ package.json is not valid JSON: {e}")
            return False
        except Exception as e:
            print(f"❌ Error reading package.json: {e}")
            return False

    def fix_npm_issues(self):
        """Main method to fix npm install issues"""
        print("🔧 AI SchoolOS - NPM Install Fixer")
        print("=" * 50)
        
        # Step 1: Check npm status
        if not self.check_npm_status():
            return False
            
        # Step 2: Check network connectivity
        if not self.check_network_connectivity():
            print("⚠️  Network issues detected. Continuing anyway...")
            
        # Step 3: Check package.json
        if not self.check_package_json():
            return False
            
        # Step 4: Clear npm cache
        self.clear_npm_cache()
        
        # Step 5: Remove existing node_modules and package-lock.json
        self.remove_node_modules()
        self.remove_package_lock()
        
        # Step 6: Try standard npm install
        if self.try_npm_install_with_timeout():
            return True
            
        # Step 7: Try alternative methods
        if self.try_alternative_install_methods():
            return True
            
        print("❌ All installation methods failed")
        return False

def main():
    fixer = NPMFixer()
    
    if len(sys.argv) > 1 and sys.argv[1] == "--check":
        # Just check status
        fixer.check_npm_status()
        fixer.check_network_connectivity()
        fixer.check_package_json()
    else:
        # Full fix
        success = fixer.fix_npm_issues()
        if success:
            print("\n🎉 npm install issues fixed!")
            print("You can now try running the frontend again.")
        else:
            print("\n❌ Failed to fix npm install issues.")
            print("Please check your network connection and try again.")

if __name__ == "__main__":
    main() 