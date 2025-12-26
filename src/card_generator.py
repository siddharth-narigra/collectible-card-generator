"""
Card Generator Module

This module provides functionality to generate trading card games using AI.
It creates card data (names, descriptions, stats) using text generation APIs
and card artwork using image generation APIs.
"""

import json
import os
import zipfile
from dataclasses import dataclass, field, asdict
from typing import Any, Callable, Optional

import requests

from html_card_generator import create_html_card, get_available_templates


# =============================================================================
# Constants
# =============================================================================

TEXT_API_URL = "https://text.pollinations.ai/openai"
IMAGE_API_URL = "https://image.pollinations.ai/prompt"
IMAGE_WIDTH = 512
IMAGE_HEIGHT = 512
IMAGE_MODEL = "flux"

# Card type mappings based on theme
THEME_CARD_TYPES: dict[str, list[str]] = {
    "fantasy": ["creature", "spell", "artifact", "enchantment", "hero"],
    "medieval": ["creature", "spell", "artifact", "enchantment", "hero"],
    "magic": ["creature", "spell", "artifact", "enchantment", "hero"],
    "sci-fi": ["robot", "tech", "weapon", "vehicle", "alien"],
    "science fiction": ["robot", "tech", "weapon", "vehicle", "alien"],
    "futuristic": ["robot", "tech", "weapon", "vehicle", "alien"],
    "space": ["robot", "tech", "weapon", "vehicle", "alien"],
}
DEFAULT_CARD_TYPES = ["character", "action", "item", "location", "event"]


# =============================================================================
# Data Classes
# =============================================================================

@dataclass
class Card:
    """Represents a trading card with all its attributes."""
    
    name: str
    description: str
    image_prompt: str
    stats: dict[str, int]
    card_type: str
    
    def to_dict(self) -> dict[str, Any]:
        """Convert the card to a dictionary format."""
        return asdict(self)


# =============================================================================
# Card Generation Functions
# =============================================================================

def generate_card_data(theme: str, card_type: str) -> Optional[Card]:
    """
    Generate card data using the Pollinations.ai text generation API.
    
    Args:
        theme: The theme for the card (e.g., "Fantasy", "Sci-Fi")
        card_type: The type of card (e.g., "creature", "spell")
    
    Returns:
        A Card object with generated data, or None if generation fails.
    """
    json_schema = {
        "name": "string",
        "description": "string",
        "image_prompt": "string",
        "stats": {"stat_name": "integer"},
        "card_type": "string"
    }
    
    llm_prompt = (
        f"You are a creative assistant for a trading card game designer. "
        f"Your task is to generate a unique card concept based on the theme: '{theme}' "
        f"and card type: '{card_type}'. For the card, you must provide a name, "
        f"a short description (max 100 characters), an image prompt for AI image generation, "
        f"and relevant stats. The stats should be balanced for a trading card game. "
        f"Also include the card_type. IMPORTANT: Your entire response MUST be a single, "
        f"valid JSON object. Do not include any text, explanation, or markdown formatting "
        f"before or after the JSON object. The JSON schema for the card object must be "
        f"as follows: {json.dumps(json_schema)}."
    )
    
    payload = {
        "model": "openai",
        "messages": [{"role": "user", "content": llm_prompt}]
    }
    
    try:
        response = requests.post(
            url=TEXT_API_URL,
            headers={"Content-Type": "application/json"},
            json=payload,
            timeout=60
        )
        response.raise_for_status()
        
        response_json = response.json()
        card_data = json.loads(response_json["choices"][0]["message"]["content"])
        
        return Card(
            name=card_data["name"],
            description=card_data["description"],
            image_prompt=card_data["image_prompt"],
            stats=card_data["stats"],
            card_type=card_data["card_type"]
        )
        
    except requests.exceptions.RequestException as e:
        print(f"Error making API call to Pollinations.ai: {e}")
        return None
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON from API response: {e}")
        return None
    except KeyError as e:
        print(f"Missing key in API response: {e}")
        return None


def generate_card_image(image_prompt: str, output_path: str) -> bool:
    """
    Generate a card image using the Pollinations.ai image generation API.
    
    Args:
        image_prompt: The prompt describing the image to generate
        output_path: The file path where the image should be saved
    
    Returns:
        True if the image was generated successfully, False otherwise.
    """
    try:
        encoded_prompt = requests.utils.quote(image_prompt)
        image_url = (
            f"{IMAGE_API_URL}/{encoded_prompt}"
            f"?width={IMAGE_WIDTH}&height={IMAGE_HEIGHT}&model={IMAGE_MODEL}"
        )
        
        response = requests.get(image_url, timeout=120)
        response.raise_for_status()
        
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, 'wb') as f:
            f.write(response.content)
        
        return True
        
    except requests.exceptions.RequestException as e:
        print(f"Error generating image: {e}")
        return False
    except OSError as e:
        print(f"Error saving image: {e}")
        return False


def _get_card_types_for_theme(theme: str) -> list[str]:
    """Get the appropriate card types for a given theme."""
    theme_lower = theme.lower()
    return THEME_CARD_TYPES.get(theme_lower, DEFAULT_CARD_TYPES)


def _create_fallback_card(theme: str, card_type: str, index: int) -> Card:
    """Create a fallback card when API generation fails."""
    return Card(
        name=f"Generic {card_type.title()} {index + 1}",
        description=f"A {card_type} card for the {theme} theme. (API Error Fallback)",
        image_prompt=f"A {theme} {card_type} card artwork, digital art, detailed",
        stats={"Power": index + 1, "Cost": (index + 1) // 2 + 1, "Health": index + 2},
        card_type=card_type
    )


def _get_fallback_image_path() -> str:
    """Get the path to the fallback placeholder image."""
    return os.path.join(os.path.dirname(__file__), "..", "assets", "card_template.jpg")


def _generate_game_rules(
    theme: str,
    template_name: str,
    generated_cards: list[Card]
) -> str:
    """Generate the game rules text file content."""
    card_types = set(card.card_type for card in generated_cards)
    
    rules = f"""Card Game: {theme.title()}
{'=' * 50}

Template Style: {template_name}

BASIC RULES:
- Each player starts with a deck of cards
- Draw cards from your deck each turn
- Play cards to attack opponents or defend yourself
- Use card stats (power, cost, etc.) to determine outcomes
- First player to reduce opponent's health to 0 wins!

CARD TYPES:
"""
    for card_type in card_types:
        rules += f"- {card_type.title()}: Special abilities and effects\n"
    
    rules += f"\nGenerated {len(generated_cards)} unique cards for your {theme} themed game!\n"
    return rules


def _generate_readme(
    theme: str,
    template_name: str,
    generated_cards: list[Card]
) -> str:
    """Generate the README content for the card game."""
    content = f"""# {theme.title()} Card Game

This card game was generated using the Card Game Generator.

**Template Style:** {template_name}

## Contents
- `cards/`: Contains all card data (JSON) and images (PNG)
- `game_info/`: Contains game rules and documentation

## Cards Generated
"""
    for i, card in enumerate(generated_cards):
        content += f"{i + 1}. **{card.name}** ({card.card_type}): {card.description}\n"
    
    return content


# =============================================================================
# Main Generation Function
# =============================================================================

ProgressCallback = Callable[[str, int, int], None]


def create_card_game_zip(
    theme: str,
    output_dir: str,
    num_cards: int = 5,
    template_style: str = "bright_swiss",
    progress_callback: Optional[ProgressCallback] = None
) -> str:
    """
    Create a complete card game as a zip file.
    
    Args:
        theme: The theme for the card game (e.g., "Fantasy", "Cyberpunk")
        output_dir: Directory where the zip file should be created
        num_cards: Number of cards to generate (1-20)
        template_style: The card template style to use
        progress_callback: Optional callback for progress updates
    
    Returns:
        The path to the created zip file.
    
    Raises:
        ValueError: If template_style is not recognized
    """
    # Set up directories
    safe_theme = theme.replace(' ', '_').lower()
    project_dir = os.path.join(output_dir, f"{safe_theme}_card_game")
    cards_dir = os.path.join(project_dir, "cards")
    game_info_dir = os.path.join(project_dir, "game_info")
    
    # Validate and get template
    templates = get_available_templates()
    if template_style not in templates:
        available = list(templates.keys())
        print(f"Template '{template_style}' not found. Available: {available}")
        template_style = available[0] if available else "bright_swiss"
    
    template_path = templates[template_style]["path"]
    template_name = templates[template_style]["name"]
    
    # Create directories
    os.makedirs(cards_dir, exist_ok=True)
    os.makedirs(game_info_dir, exist_ok=True)
    
    # Get card types for theme
    card_types = _get_card_types_for_theme(theme)
    
    # Progress tracking
    total_steps = num_cards * 3  # data + image + card creation per card
    current_step = 0
    generated_cards: list[Card] = []
    
    # Generate each card
    for i in range(num_cards):
        card_type = card_types[i % len(card_types)]
        
        # Step 1: Generate card data
        if progress_callback:
            progress_callback(f"Generating card data {i + 1}/{num_cards}: {card_type}", current_step, total_steps)
        
        card = generate_card_data(theme, card_type)
        if card is None:
            print(f"Falling back to generic card data for {card_type}")
            card = _create_fallback_card(theme, card_type, i)
        
        generated_cards.append(card)
        current_step += 1
        
        # Save card data as JSON
        card_filename_base = f"{card.name.replace(' ', '_').lower()}_{i}"
        json_path = os.path.join(cards_dir, f"{card_filename_base}.json")
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(card.to_dict(), f, indent=4)
        
        # Step 2: Generate card artwork
        if progress_callback:
            progress_callback(f"Generating artwork for {card.name}", current_step, total_steps)
        
        raw_image_path = os.path.join(cards_dir, f"raw_{card_filename_base}.png")
        if not generate_card_image(card.image_prompt, raw_image_path):
            print(f"Using placeholder image for {card.name}")
            raw_image_path = _get_fallback_image_path()
        
        current_step += 1
        
        # Step 3: Create playable card image
        if progress_callback:
            progress_callback(f"Creating playable card for {card.name}", current_step, total_steps)
        
        playable_card_path = os.path.join(cards_dir, f"{card_filename_base}.png")
        create_html_card(card, raw_image_path, template_path, playable_card_path, i + 1)
        current_step += 1
    
    # Create game rules
    rules_path = os.path.join(game_info_dir, "game_rules.txt")
    with open(rules_path, 'w', encoding='utf-8') as f:
        f.write(_generate_game_rules(theme, template_name, generated_cards))
    
    # Create README
    readme_path = os.path.join(project_dir, "README.md")
    with open(readme_path, 'w', encoding='utf-8') as f:
        f.write(_generate_readme(theme, template_name, generated_cards))
    
    # Create zip file
    zip_path = f"{project_dir}.zip"
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, _, files in os.walk(project_dir):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, project_dir)
                zipf.write(file_path, arcname)
    
    if progress_callback:
        progress_callback("Card game generated successfully!", total_steps, total_steps)
    
    return zip_path


# =============================================================================
# CLI Entry Point
# =============================================================================

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        theme_arg = sys.argv[1]
        num_cards_arg = int(sys.argv[2]) if len(sys.argv) > 2 else 5
        template_arg = sys.argv[3] if len(sys.argv) > 3 else "bright_swiss"
        
        print(f"Generating {num_cards_arg} cards for theme: {theme_arg}")
        print(f"Using template: {template_arg}")
        
        output = "./output"
        result = create_card_game_zip(theme_arg, output, num_cards_arg, template_arg)
        print(f"Successfully created: {result}")
    else:
        print("Usage: python card_generator.py <theme> [num_cards] [template_style]")
        print(f"Available templates: {list(get_available_templates().keys())}")
