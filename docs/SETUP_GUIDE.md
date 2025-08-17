# Setup Guide - Card Game Generator

This guide will help you set up and run the Card Game Generator on your system.

## System Requirements

### Minimum Requirements
- **Operating System**: Windows 10, macOS 10.14, or Linux (Ubuntu 18.04+)
- **Python**: Version 3.7 or higher
- **RAM**: 2 GB minimum, 4 GB recommended
- **Storage**: 100 MB for application, additional space for generated games
- **Internet**: Stable connection required for AI API calls

### Recommended Requirements
- **Python**: Version 3.9 or higher
- **RAM**: 8 GB or more
- **Storage**: 1 GB free space
- **Internet**: Broadband connection for faster generation

## Installation Methods

### Method 1: Quick Installation (Recommended)

1. **Download the project files**
   - Download the zip file and extract it to your desired location
   - Or clone the repository if available

2. **Open terminal/command prompt**
   - Windows: Press `Win + R`, type `cmd`, press Enter
   - macOS: Press `Cmd + Space`, type `terminal`, press Enter
   - Linux: Press `Ctrl + Alt + T`

3. **Navigate to the project directory**
   ```bash
   cd path/to/card_game_generator
   ```

4. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

5. **Run the application**
   ```bash
   python main.py
   ```

### Method 2: Manual Installation

If the quick method doesn't work, try installing dependencies manually:

```bash
pip install requests
pip install Pillow
python main.py
```

### Method 3: Virtual Environment (Advanced)

For a clean installation that doesn't affect your system Python:

```bash
# Create virtual environment
python -m venv card_game_env

# Activate virtual environment
# On Windows:
card_game_env\Scripts\activate
# On macOS/Linux:
source card_game_env/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run application
python main.py
```

## Platform-Specific Instructions

### Windows

1. **Install Python**:
   - Download from [python.org](https://python.org)
   - During installation, check "Add Python to PATH"

2. **Open Command Prompt**:
   - Press `Win + R`, type `cmd`, press Enter

3. **Navigate and run**:
   ```cmd
   cd C:\path\to\card_game_generator
   pip install -r requirements.txt
   python main.py
   ```

### macOS

1. **Install Python** (if not already installed):
   ```bash
   # Using Homebrew (recommended)
   brew install python
   
   # Or download from python.org
   ```

2. **Open Terminal**:
   - Press `Cmd + Space`, type "terminal"

3. **Navigate and run**:
   ```bash
   cd /path/to/card_game_generator
   pip3 install -r requirements.txt
   python3 main.py
   ```

### Linux (Ubuntu/Debian)

1. **Install Python and pip**:
   ```bash
   sudo apt update
   sudo apt install python3 python3-pip python3-tk
   ```

2. **Navigate and run**:
   ```bash
   cd /path/to/card_game_generator
   pip3 install -r requirements.txt
   python3 main.py
   ```

### Linux (CentOS/RHEL/Fedora)

1. **Install Python and pip**:
   ```bash
   # CentOS/RHEL
   sudo yum install python3 python3-pip python3-tkinter
   
   # Fedora
   sudo dnf install python3 python3-pip python3-tkinter
   ```

2. **Navigate and run**:
   ```bash
   cd /path/to/card_game_generator
   pip3 install -r requirements.txt
   python3 main.py
   ```

## Troubleshooting Installation

### Common Issues and Solutions

#### 1. "Python is not recognized" (Windows)
**Problem**: Python not in system PATH
**Solution**: 
- Reinstall Python and check "Add Python to PATH"
- Or manually add Python to PATH in system environment variables

#### 2. "pip is not recognized"
**Problem**: pip not installed or not in PATH
**Solution**:
```bash
# Try python -m pip instead
python -m pip install -r requirements.txt

# Or install pip manually
python -m ensurepip --upgrade
```

#### 3. "Permission denied" errors
**Problem**: Insufficient permissions
**Solution**:
```bash
# Use --user flag
pip install --user -r requirements.txt

# Or use sudo on Linux/macOS (not recommended)
sudo pip install -r requirements.txt
```

#### 4. "tkinter not found" (Linux)
**Problem**: tkinter not installed
**Solution**:
```bash
# Ubuntu/Debian
sudo apt install python3-tk

# CentOS/RHEL
sudo yum install python3-tkinter

# Fedora
sudo dnf install python3-tkinter
```

#### 5. SSL Certificate errors
**Problem**: Corporate firewall or outdated certificates
**Solution**:
```bash
# Upgrade certificates
pip install --upgrade certifi

# Or use trusted hosts
pip install --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host files.pythonhosted.org -r requirements.txt
```

#### 6. "Module not found" after installation
**Problem**: Wrong Python version or virtual environment
**Solution**:
- Make sure you're using the same Python version for installation and running
- Check if you're in the correct virtual environment
- Try: `python -m pip list` to see installed packages

## Verifying Installation

After installation, verify everything works:

1. **Check Python version**:
   ```bash
   python --version
   # Should show Python 3.7 or higher
   ```

2. **Check installed packages**:
   ```bash
   pip list
   # Should show 'requests' and 'Pillow'
   ```

3. **Test the application**:
   ```bash
   python main.py
   # Should open the GUI window
   ```

4. **Test card generation**:
   - Enter "test" as theme
   - Set cards to 1
   - Click "Generate Card Game"
   - Should create a zip file

## Performance Optimization

### For Better Performance

1. **Use SSD storage** for faster file operations
2. **Ensure stable internet** for API calls
3. **Close unnecessary applications** to free RAM
4. **Use wired internet** instead of WiFi if possible

### For Slower Systems

1. **Generate fewer cards** at once (1-3 instead of 5+)
2. **Use simple themes** (avoid complex descriptions)
3. **Close other applications** while generating
4. **Be patient** - AI generation takes time

## Network Configuration

### Firewall Settings

The application needs internet access for:
- `text.pollinations.ai` (port 443)
- `image.pollinations.ai` (port 443)

Make sure these domains are not blocked by your firewall.

### Proxy Settings

If you're behind a corporate proxy, you may need to configure Python to use it:

```bash
# Set proxy environment variables
export HTTP_PROXY=http://proxy.company.com:8080
export HTTPS_PROXY=http://proxy.company.com:8080

# Or use pip with proxy
pip install --proxy http://proxy.company.com:8080 -r requirements.txt
```

## Getting Help

If you still have issues after following this guide:

1. **Check the error message** carefully
2. **Search online** for the specific error
3. **Try the alternative installation methods**
4. **Check your internet connection**
5. **Verify Python and pip versions**

## Next Steps

Once installation is complete:
- Read the [User Guide](USER_GUIDE.md) to learn how to use the application
- Check the main [README.md](../README.md) for feature overview
- Start generating your first card game!

---

**Happy card generating!** 🎮

