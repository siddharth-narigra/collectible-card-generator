#!/usr/bin/env python3
"""
Installation Verification Script for Card Game Generator
========================================================

This script verifies that the Card Game Generator is properly installed
and all dependencies are available.

Usage:
    python verify_installation.py

The script will check:
- Python version compatibility
- Required packages installation
- Internet connectivity
- File permissions
- Basic functionality

Author: Card Game Generator Team
Version: 1.0.0
"""

import sys
import os
import importlib
import subprocess
import json
from pathlib import Path

def print_header(title):
    """Print a formatted header"""
    print("\n" + "=" * 60)
    print(f" {title}")
    print("=" * 60)

def print_check(description, status, details=""):
    """Print a check result"""
    status_symbol = "✓" if status else "✗"
    status_text = "PASS" if status else "FAIL"
    print(f"{status_symbol} {description}: {status_text}")
    if details:
        print(f"  {details}")

def check_python_version():
    """Check if Python version is compatible"""
    print_header("Python Version Check")
    
    version = sys.version_info
    required_major, required_minor = 3, 7
    
    compatible = version.major >= required_major and version.minor >= required_minor
    
    print_check(
        f"Python {required_major}.{required_minor}+ required",
        compatible,
        f"Found Python {version.major}.{version.minor}.{version.micro}"
    )
    
    return compatible

def check_required_packages():
    """Check if required packages are installed"""
    print_header("Package Dependencies Check")
    
    required_packages = {
        'requests': '2.25.0',
        'PIL': '8.0.0'  # Pillow imports as PIL
    }
    
    all_packages_ok = True
    
    for package, min_version in required_packages.items():
        try:
            if package == 'PIL':
                import PIL
                module = PIL
                package_name = 'Pillow'
            else:
                module = importlib.import_module(package)
                package_name = package
            
            # Try to get version
            version = getattr(module, '__version__', 'Unknown')
            
            print_check(
                f"{package_name} package",
                True,
                f"Version {version} found"
            )
            
        except ImportError:
            print_check(
                f"{package_name} package",
                False,
                f"Not installed. Run: pip install {package_name}"
            )
            all_packages_ok = False
    
    return all_packages_ok

def check_tkinter():
    """Check if tkinter is available"""
    print_header("GUI Framework Check")
    
    try:
        import tkinter
        print_check(
            "tkinter (GUI framework)",
            True,
            "Available for GUI interface"
        )
        return True
    except ImportError:
        print_check(
            "tkinter (GUI framework)",
            False,
            "Not available. Install python3-tk package"
        )
        return False

def check_internet_connectivity():
    """Check internet connectivity to required APIs"""
    print_header("Internet Connectivity Check")
    
    try:
        import requests
        
        # Test Pollinations.ai text API
        try:
            response = requests.get("https://text.pollinations.ai/models", timeout=10)
            text_api_ok = response.status_code == 200
        except:
            text_api_ok = False
        
        print_check(
            "Pollinations.ai text API",
            text_api_ok,
            "Required for card text generation"
        )
        
        # Test Pollinations.ai image API
        try:
            response = requests.get("https://image.pollinations.ai/prompt/test?width=64&height=64", timeout=10)
            image_api_ok = response.status_code == 200
        except:
            image_api_ok = False
        
        print_check(
            "Pollinations.ai image API",
            image_api_ok,
            "Required for card image generation"
        )
        
        return text_api_ok and image_api_ok
        
    except ImportError:
        print_check(
            "Internet connectivity test",
            False,
            "requests package not available"
        )
        return False

def check_file_permissions():
    """Check file system permissions"""
    print_header("File System Permissions Check")
    
    # Check if we can create directories
    test_dir = Path("test_permissions")
    try:
        test_dir.mkdir(exist_ok=True)
        dir_ok = True
        test_dir.rmdir()
    except:
        dir_ok = False
    
    print_check(
        "Directory creation",
        dir_ok,
        "Required for output folders"
    )
    
    # Check if we can create files
    test_file = Path("test_file.txt")
    try:
        test_file.write_text("test")
        file_ok = True
        test_file.unlink()
    except:
        file_ok = False
    
    print_check(
        "File creation",
        file_ok,
        "Required for card generation"
    )
    
    return dir_ok and file_ok

def check_project_structure():
    """Check if project files are in place"""
    print_header("Project Structure Check")
    
    required_files = [
        "main.py",
        "requirements.txt",
        "README.md",
        "src/card_generator.py",
        "src/gui.py"
    ]
    
    all_files_ok = True
    
    for file_path in required_files:
        exists = Path(file_path).exists()
        print_check(
            f"File: {file_path}",
            exists,
            "Required project file"
        )
        if not exists:
            all_files_ok = False
    
    return all_files_ok

def test_basic_functionality():
    """Test basic card generation functionality"""
    print_header("Basic Functionality Test")
    
    try:
        # Add src to path
        sys.path.insert(0, 'src')
        
        from card_generator import Card, generate_card_data
        
        # Test Card class
        test_card = Card(
            name="Test Card",
            description="A test card",
            image_prompt="test image",
            stats={"power": 1},
            card_type="test"
        )
        
        card_dict = test_card.to_dict()
        card_ok = isinstance(card_dict, dict) and "name" in card_dict
        
        print_check(
            "Card class functionality",
            card_ok,
            "Basic card creation works"
        )
        
        return card_ok
        
    except Exception as e:
        print_check(
            "Basic functionality test",
            False,
            f"Error: {str(e)}"
        )
        return False

def run_verification():
    """Run all verification checks"""
    print("Card Game Generator - Installation Verification")
    print("This script will verify that everything is properly installed.")
    
    checks = [
        ("Python Version", check_python_version),
        ("Required Packages", check_required_packages),
        ("GUI Framework", check_tkinter),
        ("Internet Connectivity", check_internet_connectivity),
        ("File Permissions", check_file_permissions),
        ("Project Structure", check_project_structure),
        ("Basic Functionality", test_basic_functionality)
    ]
    
    results = {}
    
    for check_name, check_function in checks:
        try:
            results[check_name] = check_function()
        except Exception as e:
            print_check(check_name, False, f"Error during check: {str(e)}")
            results[check_name] = False
    
    # Summary
    print_header("Verification Summary")
    
    passed = sum(results.values())
    total = len(results)
    
    print(f"Checks passed: {passed}/{total}")
    
    if passed == total:
        print("\n🎉 All checks passed! The Card Game Generator is ready to use.")
        print("\nTo start the application, run:")
        print("    python main.py")
    else:
        print("\n⚠️  Some checks failed. Please address the issues above.")
        print("\nCommon solutions:")
        print("- Install missing packages: pip install -r requirements.txt")
        print("- Check internet connection")
        print("- Ensure you're in the correct directory")
        print("- Check file permissions")
    
    print("\nFor detailed setup instructions, see:")
    print("- docs/SETUP_GUIDE.md")
    print("- README.md")
    
    return passed == total

if __name__ == "__main__":
    success = run_verification()
    sys.exit(0 if success else 1)

