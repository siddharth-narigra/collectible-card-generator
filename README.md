# Card Game Generator

A Python application that generates custom trading card games based on any theme you provide. The application uses AI to create unique cards with artwork, stats, and descriptions, then creates professional-looking playable card images using HTML/CSS templates inspired by classic trading card designs.

## Features

- 🎨 **AI-Generated Cards**: Creates unique cards with names, descriptions, and artwork
- 🖼️ **Custom Artwork**: Generates themed images for each card using AI
- 📊 **Balanced Stats**: Automatically generates balanced game statistics
- 🎯 **Theme-Based**: Supports any theme (Fantasy, Sci-Fi, Horror, etc.)
- 🃏 **Multiple Card Templates**: Choose from different design styles
- 📦 **Complete Package**: Outputs a zip file with all cards and game rules
- 🖥️ **User-Friendly GUI**: Easy-to-use graphical interface with template selection
- 🆓 **Free APIs**: Uses free AI services (no API keys required)

## Card Templates

The application now supports multiple card design templates:

### 1. Classic Template
- **Style**: Traditional trading card design
- **Color Scheme**: Beige/brown gradient backgrounds
- **Features**: Elegant borders, circular stat displays, premium feel
- **Best For**: Traditional card games, fantasy themes

### 2. Swiss Design Template
- **Style**: Minimalistic, clean design inspired by Swiss design principles
- **Color Scheme**: Light gray backgrounds with red accents
- **Features**: Grid-based layout, modern typography, clean lines
- **Best For**: Modern themes, sci-fi, minimalist aesthetics

## Screenshots

### Classic Template Cards
The classic template features:
- Beige/brown gradient backgrounds
- Prominent name bars with elegant typography
- Large artwork areas with inset borders
- Descriptive text sections
- Circular stat displays (ATK, DEF, SPD, HP)
- Footer information showing card type, rarity, and number

### Swiss Design Template Cards
The Swiss design template features:
- Clean, minimalistic layout with grid structure
- Modern typography using Inter font
- Left-side image placement with right-side information
- Horizontal stat bar at bottom
- Red accent color for stats and highlights
- Professional, contemporary appearance

## Installation

### Prerequisites

- Python 3.7 or higher
- Internet connection (for AI API calls)
- wkhtmltopdf (for HTML to image conversion)

### Quick Setup

1. **Download the project**:
   ```bash
   # If you have git:
   git clone <repository-url>
   cd card_game_generator
   
   # Or download and extract the zip file
   ```

2. **Install system dependencies**:
   ```bash
   # Ubuntu/Debian:
   sudo apt-get update
   sudo apt-get install -y wkhtmltopdf python3-tk
   
   # macOS (with Homebrew):
   brew install wkhtmltopdf
   
   # Windows: Download wkhtmltopdf from https://wkhtmltopdf.org/downloads.html
   ```

3. **Install Python dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**:
   ```bash
   python main.py
   ```

## Usage

### Using the GUI

1. **Launch the application**:
   ```bash
   python main.py
   ```

2. **Enter a theme**: Type any theme you want (e.g., "Fantasy", "Cyberpunk", "Pirates")

3. **Set number of cards**: Choose how many cards to generate (1-20)

4. **Select card template**: Choose between "Classic" or "Swiss Design" templates

5. **Choose output directory**: Select where to save the generated card game

6. **Click "Generate Card Game"**: Watch the progress as your cards are created

7. **Find your game**: The application will create a zip file containing all your cards

### Using the Command Line

You can also use the card generator directly from the command line:

```bash
cd src
python card_generator.py "Fantasy" 5 "classic"
python card_generator.py "Cyberpunk" 3 "swiss"
```

Arguments:
- `theme`: The theme for your card game
- `num_cards`: Number of cards to generate (1-20)
- `template`: Template style ("classic" or "swiss")

## Template Selection

### In the GUI
- Use the "Card Template" dropdown to select your preferred design
- Click the "Info" button to see details about each template
- The selected template will be used for all cards in the generated game

### Command Line
- Add the template name as the third argument
- Available templates: `classic`, `swiss`
- If no template is specified, defaults to `classic`

## Output Structure

The generated zip file contains:

```
theme_card_game/
├── cards/
│   ├── card_name_0.json         # Card data (name, description, stats)
│   ├── card_name_0.png          # Professional playable card image
│   ├── raw_card_name_0.png      # Original AI-generated artwork
│   ├── card_name_1.json
│   ├── card_name_1.png
│   ├── raw_card_name_1.png
│   └── ...
├── game_info/
│   └── game_rules.txt           # Basic game rules and instructions
└── README.md                    # Information about the generated game
```

### Card Data Format

Each card JSON file contains:

```json
{
    "name": "Dragon Warrior",
    "description": "A mighty warrior who rides dragons into battle",
    "image_prompt": "A fantasy warrior riding a dragon, epic battle scene",
    "stats": {
        "attack": 8,
        "defense": 6,
        "health": 10,
        "mana": 5
    },
    "card_type": "creature"
}
```

### Card Image Features

The generated playable card images include:

- **Template-Based Design**: Choose from multiple professional templates
- **Professional Quality**: 428x571 pixel resolution suitable for printing
- **Structured Layout**: Clear sections for all card information
- **Embedded Artwork**: AI-generated images seamlessly integrated
- **Stat Displays**: Template-appropriate stat visualization
- **Card Information**: Type, rarity, and numbering system
- **Premium Feel**: Professional borders and typography

## Supported Themes

The application works with any theme you can imagine:

- **Fantasy**: Dragons, wizards, magic spells
- **Sci-Fi**: Robots, spaceships, alien technology
- **Horror**: Monsters, ghosts, supernatural creatures
- **Cyberpunk**: Hackers, AI, futuristic technology
- **Steampunk**: Victorian-era steam technology
- **Pirates**: Ships, treasure, sea adventures
- **Medieval**: Knights, castles, medieval warfare
- **Space**: Planets, astronauts, cosmic phenomena
- **And many more!**

## Technical Details

### APIs Used

- **Text Generation**: Pollinations.ai (free, no API key required)
- **Image Generation**: Pollinations.ai (free, no API key required)

### Dependencies

- `requests`: For API calls
- `tkinter`: For GUI (included with Python)
- `wkhtmltopdf`: For HTML to image conversion

### Project Structure

```
card_game_generator/
├── src/
│   ├── card_generator.py       # Core card generation logic
│   ├── html_card_generator.py  # HTML/CSS card template rendering
│   └── gui.py                  # GUI application with template selection
├── assets/
│   ├── card_template.html      # Classic HTML/CSS card template
│   ├── swiss_template.html     # Swiss Design HTML/CSS card template
│   └── card_template.jpg       # Fallback template image
├── docs/                       # Additional documentation
├── output/                     # Default output directory
├── main.py                     # Main launcher script
├── requirements.txt            # Python dependencies
└── README.md                   # This file
```

## Template Design Details

### Classic Template
- **Color Scheme**: Beige to brown gradient (#bfb8a8 to #a59d8e)
- **Borders**: Dark brown (#2b2a28) with inset shadows
- **Typography**: Cinzel serif for names, Roboto for descriptions
- **Layout**: Vertical card with circular stat displays
- **Style**: Traditional, elegant, premium feel

### Swiss Design Template
- **Color Scheme**: Light gray (#f0f0f0) with red accents (#e63946)
- **Borders**: Clean lines with minimal shadows
- **Typography**: Inter sans-serif throughout
- **Layout**: Grid-based with left image, right info
- **Style**: Modern, minimalistic, clean

## Troubleshooting

### Common Issues

1. **"Module not found" error**:
   ```bash
   pip install -r requirements.txt
   ```

2. **"wkhtmltoimage not found" error**:
   ```bash
   # Ubuntu/Debian:
   sudo apt-get install wkhtmltopdf
   
   # macOS:
   brew install wkhtmltopdf
   ```

3. **Template not found**:
   - Check that template files exist in the `assets/` directory
   - Verify template names in the dropdown match available templates

4. **Internet connection required**:
   - The application needs internet access to generate cards and images
   - Check your internet connection

5. **Slow generation**:
   - AI generation can take time, especially for images
   - Be patient and watch the progress bar

6. **Empty or failed cards**:
   - Sometimes AI APIs may be temporarily unavailable
   - Try again or reduce the number of cards

## Customization

### Adding New Templates

1. **Create HTML template**: Add a new `.html` file in the `assets/` directory
2. **Use placeholders**: Include `{{CARD_NAME}}`, `{{CARD_IMAGE_URL}}`, etc.
3. **Update template registry**: Modify `get_available_templates()` in `html_card_generator.py`
4. **Test the template**: Run the test function to verify it works

### Modifying Existing Templates

Edit the HTML/CSS files in the `assets/` directory:

- `card_template.html`: Classic template
- `swiss_template.html`: Swiss design template

### Changing Card Types

Edit `card_generator.py` to customize card types for different themes:

```python
# In the create_card_game_zip function
if theme.lower() in ["fantasy", "medieval", "magic"]:
    card_types = ["creature", "spell", "artifact", "enchantment", "hero"]
elif theme.lower() in ["sci-fi", "science fiction", "futuristic", "space"]:
    card_types = ["robot", "tech", "weapon", "vehicle", "alien"]
```
