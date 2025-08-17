# User Guide - Card Game Generator

Welcome to the Card Game Generator! This guide will help you create amazing custom card games using AI technology.

## Getting Started

### Launching the Application

1. Open your terminal/command prompt
2. Navigate to the card_game_generator folder
3. Run: `python main.py`
4. The GUI window will open

### First Time Setup

When you first run the application:
- The output directory will be set to `output/` in the project folder
- You can change this to any folder you prefer
- Make sure you have an internet connection

## Using the Interface

### Main Window Overview

The application window contains several sections:

1. **Title**: "Card Game Generator" at the top
2. **Theme Input**: Where you enter your desired theme
3. **Number of Cards**: Choose how many cards to generate (1-20)
4. **Output Directory**: Where your card game will be saved
5. **Generate Button**: Starts the card generation process
6. **Progress Bar**: Shows generation progress
7. **Status Display**: Current operation status
8. **Generation Log**: Detailed log of the process
9. **Example Themes**: Quick buttons for popular themes

### Step-by-Step Usage

#### Step 1: Choose a Theme

In the "Theme" field, enter any theme you want for your card game:

**Popular Themes:**
- Fantasy (dragons, wizards, magic)
- Sci-Fi (robots, spaceships, aliens)
- Horror (monsters, ghosts, supernatural)
- Cyberpunk (hackers, AI, neon cities)
- Steampunk (Victorian steam technology)
- Pirates (ships, treasure, adventures)
- Medieval (knights, castles, warfare)
- Space (planets, astronauts, cosmos)

**Creative Themes:**
- Underwater Adventure
- Time Travel
- Dinosaur World
- Superhero Academy
- Zombie Apocalypse
- Fairy Tale Kingdom
- Wild West
- Ancient Egypt

**Tips for Good Themes:**
- Be specific: "Medieval Knights" vs just "Medieval"
- Use descriptive words: "Dark Fantasy" vs "Fantasy"
- Combine concepts: "Space Pirates" or "Cyberpunk Wizards"

#### Step 2: Set Number of Cards

Use the spinner to choose how many cards to generate:
- **1-3 cards**: Quick test or small game
- **5 cards**: Standard small deck
- **10 cards**: Medium-sized game
- **15-20 cards**: Large, complete game

**Recommendations:**
- First time users: Start with 3-5 cards
- Testing themes: Use 1-2 cards
- Complete games: 10+ cards

#### Step 3: Choose Output Location

Click "Browse" to select where to save your card game:
- Default: `output/` folder in the project directory
- Recommended: Create a "My Card Games" folder
- Make sure you have write permissions to the folder

#### Step 4: Generate Your Game

Click "Generate Card Game" and watch the magic happen:

1. **Card Generation Phase**: AI creates card data
   - Names, descriptions, and stats for each card
   - Progress shown as "Generating card X/Y"

2. **Image Generation Phase**: AI creates artwork
   - Custom artwork for each card
   - Progress shown as "Generating image for [Card Name]"

3. **Packaging Phase**: Creates final zip file
   - Combines all cards and documentation
   - Shows "Card game generated successfully!"

#### Step 5: Find Your Game

After generation completes:
- A success message shows the file location
- Find the zip file in your chosen output directory
- File name format: `[theme]_card_game.zip`

## Understanding the Output

### Zip File Contents

Your generated card game contains:

```
theme_card_game/
├── cards/                  # All your cards
│   ├── card_name_0.json   # Card data
│   ├── card_name_0.png    # Card artwork
│   ├── card_name_1.json
│   ├── card_name_1.png
│   └── ...
├── game_info/             # Game documentation
│   └── game_rules.txt     # How to play
└── README.md              # Game overview
```

### Card Data Explained

Each `.json` file contains:

```json
{
    "name": "Shadow Assassin",
    "description": "A stealthy warrior who strikes from the darkness",
    "image_prompt": "A hooded assassin in dark clothing with glowing eyes",
    "stats": {
        "power": 7,
        "cost": 4,
        "stealth": 9
    },
    "card_type": "creature"
}
```

**Fields Explained:**
- **name**: The card's unique name
- **description**: What the card does or represents
- **image_prompt**: Description used to generate the artwork
- **stats**: Game statistics (power, cost, health, etc.)
- **card_type**: Category of card (creature, spell, item, etc.)

### Game Rules File

The `game_rules.txt` file contains:
- Basic gameplay instructions
- Explanation of card types
- List of all generated cards
- Suggestions for house rules

## Advanced Features

### Monitoring Generation

The **Generation Log** shows detailed progress:
- Each step of the process
- Any errors or warnings
- Final success confirmation

**Understanding Log Messages:**
- `[1/10] Generating card 1/5: creature` - Creating card data
- `[6/10] Generating image for Dragon Warrior` - Creating artwork
- `SUCCESS! Card game generated: /path/to/file.zip` - Complete!

### Customizing Output

#### Changing Themes Mid-Generation
- You cannot change themes during generation
- Wait for completion or restart the application

#### Adjusting Card Count
- More cards = longer generation time
- Each card takes 30-60 seconds to generate
- Images take longer than text

#### Output Directory Tips
- Use descriptive folder names
- Keep games organized by theme
- Backup your favorite generations

## Tips for Best Results

### Theme Selection

**Good Themes:**
- "Epic Fantasy Adventure"
- "Cyberpunk Hackers"
- "Pirate Treasure Hunt"
- "Space Marine Combat"

**Avoid:**
- Very generic terms ("Game", "Cards")
- Copyrighted names ("Pokemon", "Magic")
- Overly complex descriptions

### Optimal Settings

**For Quick Testing:**
- Theme: Simple, clear concept
- Cards: 1-3
- Watch the log for any issues

**For Complete Games:**
- Theme: Rich, detailed concept
- Cards: 10-15
- Allow 10-20 minutes for generation

**For Experimentation:**
- Try unusual theme combinations
- Generate small batches first
- Save successful themes for larger generations

## Troubleshooting

### Common Issues

#### Generation Fails
**Symptoms**: Error messages in log, no zip file created
**Solutions:**
1. Check internet connection
2. Try a simpler theme
3. Reduce number of cards
4. Restart the application

#### Slow Generation
**Symptoms**: Progress bar moves very slowly
**Solutions:**
1. Be patient - AI generation takes time
2. Check internet speed
3. Try generating fewer cards
4. Close other internet-heavy applications

#### Empty or Generic Cards
**Symptoms**: Cards have generic names or descriptions
**Solutions:**
1. Use more specific themes
2. Try different theme wording
3. Generate again - AI results vary

#### Images Don't Match Theme
**Symptoms**: Card artwork doesn't fit the theme
**Solutions:**
1. Use more descriptive themes
2. Try generating again
3. Check if theme is too abstract

### Error Messages

**"Please enter a theme!"**
- Solution: Type something in the theme field

**"Number of cards must be between 1 and 20!"**
- Solution: Use the spinner or type a valid number

**"Could not create output directory"**
- Solution: Choose a different output folder or check permissions

**"Error generating cards: [details]"**
- Solution: Check internet connection and try again

## Best Practices

### Planning Your Game

1. **Start Small**: Generate 3-5 cards first
2. **Test Themes**: Try different variations
3. **Build Collections**: Create multiple small games
4. **Document Ideas**: Keep notes on successful themes

### Organizing Your Games

1. **Use Folders**: Organize by theme or date
2. **Name Clearly**: Use descriptive folder names
3. **Backup Favorites**: Save your best generations
4. **Share Games**: Zip files are easy to share

### Creative Tips

1. **Mix Themes**: "Steampunk Pirates" or "Space Wizards"
2. **Use Adjectives**: "Dark Fantasy" vs "Fantasy"
3. **Think Visually**: Themes that create good imagery work best
4. **Experiment**: Try unusual combinations

## Playing Your Generated Games

### Basic Gameplay

1. **Print Cards**: Print the images and data
2. **Cut Out**: Create physical cards
3. **Learn Rules**: Read the game_rules.txt file
4. **Play**: Use the stats for gameplay

### Digital Play

1. **Screen Sharing**: Share cards during video calls
2. **Digital Tabletops**: Import into online gaming platforms
3. **Mobile**: View cards on phones/tablets

### House Rules

Create your own rules using the card stats:
- Use "power" for attack strength
- Use "cost" for playing requirements
- Use "health" for durability
- Create special abilities based on descriptions

## Getting Help

### If You Need Assistance

1. **Check This Guide**: Most questions are answered here
2. **Read Error Messages**: They often explain the problem
3. **Try Simple Tests**: Generate 1 card with a simple theme
4. **Check Requirements**: Ensure Python and internet work

### Community and Support

- Share your generated games with friends
- Experiment with different themes
- Create themed collections
- Have fun and be creative!

---

**Enjoy creating amazing card games!** 🎮✨

Remember: The AI generates unique content each time, so even the same theme will produce different results. Don't hesitate to generate multiple versions to find the perfect cards for your game!

