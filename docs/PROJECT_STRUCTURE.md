# Project Structure - Card Game Generator

This document describes the complete structure of the Card Game Generator project.

## Directory Overview

```
card_game_generator/
├── main.py                 # Main application launcher
├── requirements.txt        # Python dependencies
├── README.md              # Main project documentation
├── src/                   # Source code directory
│   ├── card_generator.py  # Core card generation logic
│   ├── gui.py            # GUI application code
│   └── output/           # Default output directory for generated games
├── assets/               # Assets directory (reserved for future use)
├── docs/                 # Documentation directory
│   ├── PROJECT_STRUCTURE.md  # This file
│   ├── SETUP_GUIDE.md        # Installation and setup instructions
│   └── USER_GUIDE.md         # User manual and usage guide
└── output/               # Alternative output directory
```

## File Descriptions

### Root Directory Files

#### `main.py`
- **Purpose**: Main entry point for the application
- **Function**: Launches the GUI application
- **Usage**: `python main.py`
- **Dependencies**: Imports from `src/gui.py`

#### `requirements.txt`
- **Purpose**: Lists Python package dependencies
- **Contents**: 
  - `requests>=2.25.0` (for API calls)
  - `Pillow>=8.0.0` (for image processing)
- **Usage**: `pip install -r requirements.txt`

#### `README.md`
- **Purpose**: Main project documentation
- **Contents**: 
  - Project overview and features
  - Installation instructions
  - Usage examples
  - Troubleshooting guide
  - Technical details

### Source Code Directory (`src/`)

#### `src/card_generator.py`
- **Purpose**: Core card generation functionality
- **Key Classes**:
  - `Card`: Data structure for card information
- **Key Functions**:
  - `generate_card_data()`: Creates card data using AI
  - `generate_card_image()`: Creates card artwork using AI
  - `create_card_game_zip()`: Orchestrates full game generation
- **APIs Used**:
  - Pollinations.ai text generation
  - Pollinations.ai image generation
- **Output**: Zip files containing complete card games

#### `src/gui.py`
- **Purpose**: Graphical user interface
- **Key Classes**:
  - `CardGameGeneratorGUI`: Main GUI application
- **Features**:
  - Theme input field
  - Card count selection
  - Output directory selection
  - Progress tracking
  - Generation logging
  - Example theme buttons
- **Framework**: tkinter (Python standard library)

#### `src/output/`
- **Purpose**: Default output directory for generated card games
- **Contents**: Created automatically when cards are generated
- **Structure**: Contains zip files and extracted game directories

### Documentation Directory (`docs/`)

#### `docs/SETUP_GUIDE.md`
- **Purpose**: Detailed installation and setup instructions
- **Contents**:
  - System requirements
  - Platform-specific installation steps
  - Troubleshooting common installation issues
  - Network configuration
  - Performance optimization tips

#### `docs/USER_GUIDE.md`
- **Purpose**: Comprehensive user manual
- **Contents**:
  - Step-by-step usage instructions
  - Interface explanation
  - Theme suggestions
  - Output format description
  - Best practices
  - Troubleshooting usage issues

#### `docs/PROJECT_STRUCTURE.md`
- **Purpose**: This file - project organization documentation
- **Contents**:
  - Directory structure
  - File descriptions
  - Code organization
  - Data flow explanation

### Assets Directory (`assets/`)
- **Purpose**: Reserved for future assets (icons, images, etc.)
- **Status**: Currently empty, available for future enhancements

### Output Directory (`output/`)
- **Purpose**: Alternative output location
- **Usage**: Can be selected as output directory in GUI
- **Contents**: User-generated card games

## Generated Game Structure

When a card game is generated, it creates the following structure:

```
[theme]_card_game/
├── README.md              # Game-specific documentation
├── cards/                 # All card files
│   ├── [card_name]_0.json # Card data (JSON format)
│   ├── [card_name]_0.png  # Card artwork (PNG image)
│   ├── [card_name]_1.json
│   ├── [card_name]_1.png
│   └── ...                # Additional cards
└── game_info/             # Game documentation
    └── game_rules.txt     # Basic game rules and card list
```

### Generated File Formats

#### Card Data Files (`.json`)
```json
{
    "name": "Card Name",
    "description": "Card description and abilities",
    "image_prompt": "Prompt used for AI image generation",
    "stats": {
        "power": 5,
        "cost": 3,
        "health": 7
    },
    "card_type": "creature"
}
```

#### Card Images (`.png`)
- **Format**: PNG images
- **Size**: 512x512 pixels
- **Content**: AI-generated artwork based on theme and card description
- **Quality**: High-resolution suitable for printing or digital use

## Code Organization

### Data Flow

1. **User Input** → GUI collects theme, card count, output directory
2. **Validation** → GUI validates input parameters
3. **Generation** → GUI calls `create_card_game_zip()` in separate thread
4. **Card Creation** → For each card:
   - `generate_card_data()` creates card information
   - `generate_card_image()` creates card artwork
5. **Packaging** → All files combined into zip archive
6. **Completion** → GUI displays success message and file location

### Error Handling

- **Network Errors**: Graceful handling of API failures
- **File System Errors**: Proper error messages for file operations
- **Input Validation**: User input validation before processing
- **Fallback Content**: Generic cards created if AI generation fails

### Threading

- **Main Thread**: GUI interface and user interaction
- **Worker Thread**: Card generation process (prevents GUI freezing)
- **Progress Updates**: Thread-safe communication for progress reporting

## Dependencies

### Required Python Packages

1. **requests**
   - Purpose: HTTP requests to AI APIs
   - Version: ≥2.25.0
   - Usage: API calls to Pollinations.ai

2. **Pillow**
   - Purpose: Image processing (optional)
   - Version: ≥8.0.0
   - Usage: Future image manipulation features

### Standard Library Modules

- **tkinter**: GUI framework
- **threading**: Background processing
- **json**: Data serialization
- **zipfile**: Archive creation
- **os**: File system operations
- **sys**: System-specific parameters

## Configuration

### Default Settings

- **Default Theme**: None (user must specify)
- **Default Card Count**: 5
- **Default Output**: `src/output/` directory
- **Image Size**: 512x512 pixels
- **API Timeout**: 30 seconds per request

### Customizable Parameters

Users can modify these in the source code:

- **Card Types**: Edit `card_types` lists in `card_generator.py`
- **Image Size**: Modify URL parameters in `generate_card_image()`
- **API Endpoints**: Change URLs in API functions
- **GUI Layout**: Modify widget arrangement in `gui.py`

## Future Enhancements

### Planned Features

- **Custom Card Templates**: User-defined card layouts
- **Multiple AI Providers**: Support for additional AI services
- **Export Formats**: PDF, print-ready formats
- **Game Rule Generator**: AI-generated custom rules
- **Card Editor**: Post-generation editing capabilities

### Extension Points

- **Plugin System**: Modular card type definitions
- **Theme Templates**: Pre-defined theme configurations
- **API Abstraction**: Easy addition of new AI providers
- **Output Formats**: Additional export options

---

This structure provides a solid foundation for the Card Game Generator while remaining extensible for future enhancements.

