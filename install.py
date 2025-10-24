#!/usr/bin/env python3
import subprocess
import sys
import os

def install_requirements():
    """Install required packages"""
    requirements = [
        "click>=8.0.0",
        "colorama>=0.4.4", 
        "python-dateutil>=2.8.2",
        "pyyaml>=5.4.0"
    ]
    
    for package in requirements:
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])
            print(f"✅ Installed {package}")
        except subprocess.CalledProcessError:
            print(f"❌ Failed to install {package}")
            sys.exit(1)

def setup_package():
    """Setup the phishguard package"""
    try:
        subprocess.check_call([sys.executable, "setup.py", "develop"])
        print("✅ PhishGuard Africa installed successfully!")
    except subprocess.CalledProcessError:
        print("❌ Failed to setup package")
        sys.exit(1)

if __name__ == "__main__":
    print("🚀 Installing PhishGuard Africa...")
    install_requirements()
    setup_package()
    print("\n🎉 Installation complete!")
    print("💡 Usage examples:")
    print("   phishguard check \"Your message here\"")
    print("   phishguard stats")
    print("   phishguard demo")