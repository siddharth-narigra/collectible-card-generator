#!/usr/bin/env python3
"""
Card Game Generator - Application Entry Point

A Python application that generates custom trading card games using AI.
Launch this script to start the graphical user interface.

Usage:
    python main.py

Requirements:
    - Python 3.10+
    - tkinter (usually included with Python)
    - requests
    - wkhtmltopdf (system dependency)
"""

import sys
from pathlib import Path

# Add src directory to Python path for imports
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))


def main() -> None:
    """Application entry point."""
    try:
        from gui import main as gui_main
        
        print("=" * 50)
        print("  Card Game Generator")
        print("=" * 50)
        print("Starting application...")
        print()
        
        gui_main()
        
    except ImportError as e:
        print(f"Error: Missing required module - {e}")
        print()
        print("Please install dependencies:")
        print("  pip install -r requirements.txt")
        sys.exit(1)
        
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
