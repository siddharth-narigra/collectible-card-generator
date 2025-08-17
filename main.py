#!/usr/bin/env python3
"""
Card Game Generator - Main Launcher
===================================

This is the main entry point for the Card Game Generator application.
Run this script to start the GUI application.

Usage:
    python main.py

Requirements:
    - Python 3.7+
    - tkinter (usually included with Python)
    - requests
    - Pillow (optional, for image processing)

Author: Card Game Generator Team
Version: 1.0.0
"""

import sys
import os

# Add src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

try:
    from src.gui import main
    
    if __name__ == "__main__":
        print("Starting Card Game Generator...")
        print("=" * 50)
        print("Welcome to the Card Game Generator!")
        print("This application will help you create custom card games")
        print("based on any theme you choose.")
        print("=" * 50)
        main()
        
except ImportError as e:
    print(f"Error importing required modules: {e}")
    print("Please make sure all dependencies are installed.")
    print("Run: pip install -r requirements.txt")
    sys.exit(1)
except Exception as e:
    print(f"Error starting application: {e}")
    sys.exit(1)

