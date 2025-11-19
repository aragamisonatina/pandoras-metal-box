#!/usr/bin/env python3
"""
Auto-installer script for Pandora's Metal Box
Checks for required dependencies and installs them if missing
"""
import subprocess
import sys
import importlib.util
import os

def install_package(package):
    """Install a package using pip"""
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

def check_and_install_requirements():
    """Check if required packages are installed, install if missing"""
    requirements_file = os.path.join(os.path.dirname(__file__), "requirements.txt")
    
    if not os.path.exists(requirements_file):
        print("Warning: requirements.txt not found")
        return
    
    with open(requirements_file, 'r') as f:
        requirements = f.read().strip().split('\n')
    
    for requirement in requirements:
        if not requirement.strip() or requirement.startswith('#'):
            continue
            
        # Extract package name (handle version specs like numpy>=1.24.0)
        package_name = requirement.split('>=')[0].split('==')[0].split('<=')[0].strip()
        
        try:
            # Try to import the package
            importlib.import_module(package_name)
            print(f"✓ {package_name} is already installed")
        except ImportError:
            print(f"✗ {package_name} not found. Installing...")
            try:
                install_package(requirement)
                print(f"✓ Successfully installed {package_name}")
            except subprocess.CalledProcessError as e:
                print(f"✗ Failed to install {package_name}: {e}")
                sys.exit(1)

if __name__ == "__main__":
    print("Checking dependencies for Pandora's Metal Box...")
    check_and_install_requirements()
    print("All dependencies satisfied!")
    
    # Import and run main
    try:
        import main
        main.main()
    except Exception as e:
        print(f"Error running main: {e}")
        sys.exit(1)