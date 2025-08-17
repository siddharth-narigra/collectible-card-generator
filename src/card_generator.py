import requests
import os
import json
import zipfile
from typing import List, Dict, Any
from html_card_generator import create_html_card, get_available_templates

class Card:
    def __init__(self, name: str, description: str, image_prompt: str, stats: dict[str, Any], card_type: str):
        self.name = name
        self.description = description
        self.image_prompt = image_prompt
        self.stats = stats
        self.card_type = card_type

    def to_dict(self):
        return {
            "name": self.name,
            "description": self.description,
            "image_prompt": self.image_prompt,
            "stats": self.stats,
            "card_type": self.card_type
        }

def generate_card_data(theme: str, card_type: str) -> Card:
    headers = {
        "Content-Type": "application/json"
    }
    # The prompt for the LLM, asking for a JSON object
    json_schema = {"name": "string", "description": "string", "image_prompt": "string", "stats": {"stat_name": "integer"}, "card_type": "string"}
    llm_prompt = f"You are a creative assistant for a trading card game designer. Your task is to generate a unique card concept based on the theme: \'{theme}\' and card type: \'{card_type}\'. For the card, you must provide a name, a short description (max 100 characters), an image prompt for AI image generation, and relevant stats. The stats should be balanced for a trading card game. Also include the card_type. IMPORTANT: Your entire response MUST be a single, valid JSON object. Do not include any text, explanation, or markdown formatting before or after the JSON object. The JSON schema for the card object must be as follows: {json.dumps(json_schema)}."

    data = {
        "model": "openai", # Using OpenAI model from Pollinations.ai
        "messages": [
            {"role": "user", "content": llm_prompt}
        ]
    }
    try:
        response = requests.post(
            url="https://text.pollinations.ai/openai",
            headers=headers,
            json=data
        )
        response.raise_for_status()
        response_json = response.json()
        card_data_json = json.loads(response_json["choices"][0]["message"]["content"])
        return Card(
            name=card_data_json["name"],
            description=card_data_json["description"],
            image_prompt=card_data_json["image_prompt"],
            stats=card_data_json["stats"],
            card_type=card_data_json["card_type"]
        )
    except requests.exceptions.RequestException as e:
        print(f"Error making API call to Pollinations.ai: {e}")
        return None
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON from Pollinations.ai API: {e}")
        return None
    except KeyError as e:
        print(f"Missing key in Pollinations.ai API response: {e}")
        return None

def generate_card_image(image_prompt: str, output_path: str) -> bool:
    """Generate card image using Pollinations.ai image API"""
    try:
        # Use Pollinations.ai image generation API
        image_url = f"https://image.pollinations.ai/prompt/{requests.utils.quote(image_prompt)}?width=512&height=512&model=flux"
        
        response = requests.get(image_url)
        response.raise_for_status()
        
        # Save the image
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, 'wb') as f:
            f.write(response.content)
        
        return True
    except Exception as e:
        print(f"Error generating image: {e}")
        return False

def create_card_game_zip(theme: str, output_dir: str, num_cards: int = 5, template_style: str = "classic", progress_callback=None):
    """Create a complete card game zip with specified number of cards and template style"""
    project_dir = os.path.join(output_dir, f"{theme.replace(' ', '_').lower()}_card_game")
    cards_dir = os.path.join(project_dir, "cards")
    game_info_dir = os.path.join(project_dir, "game_info")
    
    # Get available templates
    templates = get_available_templates()
    
    # Validate template selection
    if template_style not in templates:
        print(f"Template '{template_style}' not found. Available templates: {list(templates.keys())}")
        template_style = "classic"  # Fallback to classic
    
    template_path = templates[template_style]["path"]
    template_name = templates[template_style]["name"]

    os.makedirs(cards_dir, exist_ok=True)
    os.makedirs(game_info_dir, exist_ok=True)

    # Define card types based on theme
    if theme.lower() in ["fantasy", "medieval", "magic"]:
        card_types = ["creature", "spell", "artifact", "enchantment", "hero"]
    elif theme.lower() in ["sci-fi", "science fiction", "futuristic", "space"]:
        card_types = ["robot", "tech", "weapon", "vehicle", "alien"]
    else:
        card_types = ["character", "action", "item", "location", "event"]
    
    generated_cards = []
    total_steps = num_cards * 3  # Card data + image generation + playable card creation
    current_step = 0

    for i in range(num_cards):
        card_type = card_types[i % len(card_types)]
        
        if progress_callback:
            progress_callback(f"Generating card data {i+1}/{num_cards}: {card_type}", current_step, total_steps)
        
        # Generate card data
        card = generate_card_data(theme, card_type)
        if card is None:
            # Fallback card if API call fails or returns invalid data
            print(f"Falling back to generic card data for {card_type} due to API error.")
            card = Card(
                name=f"Generic {card_type.title()} {i+1}",
                description=f"A {card_type} card for the {theme} theme. (API Error Fallback)",
                image_prompt=f"A {theme} {card_type} card artwork",
                stats={"Power": i+1, "Cost": (i+1)//2 + 1, "Health": i+2},
                card_type=card_type
            )
        
        generated_cards.append(card)
        current_step += 1

        # Save card data
        card_filename_base = f"{card.name.replace(' ', '_').lower()}_{i}"
        with open(os.path.join(cards_dir, f"{card_filename_base}.json"), 'w') as f:
            json.dump(card.to_dict(), f, indent=4)

        if progress_callback:
            progress_callback(f"Generating artwork for {card.name}", current_step, total_steps)

        # Generate raw card image
        raw_card_image_path = os.path.join(cards_dir, f"raw_{card_filename_base}.png")
        image_generated = generate_card_image(card.image_prompt, raw_card_image_path)
        if not image_generated:
            print(f"Falling back to placeholder image for {card.name} due to image API error.")
            # Use a default placeholder image if image generation fails
            raw_card_image_path = os.path.join(os.path.dirname(__file__), "..", "assets", "card_template.jpg") # Using existing placeholder

        current_step += 1

        if progress_callback:
            progress_callback(f"Creating playable card for {card.name}", current_step, total_steps)

        # Create playable card image using selected HTML template
        playable_card_image_path = os.path.join(cards_dir, f"{card_filename_base}.png")
        create_html_card(card, raw_card_image_path, template_path, playable_card_image_path, i+1)
        current_step += 1

    # Create game rules file
    with open(os.path.join(game_info_dir, "game_rules.txt"), 'w') as f:
        f.write(f"Card Game: {theme.title()}\n")
        f.write("=" * 50 + "\n\n")
        f.write(f"Template Style: {template_name}\n\n")
        f.write("BASIC RULES:\n")
        f.write("- Each player starts with a deck of cards\n")
        f.write("- Draw cards from your deck each turn\n")
        f.write("- Play cards to attack opponents or defend yourself\n")
        f.write("- Use card stats (power, cost, etc.) to determine outcomes\n")
        f.write("- First player to reduce opponent's health to 0 wins!\n\n")
        f.write("CARD TYPES:\n")
        for card_type in set(card.card_type for card in generated_cards):
            f.write(f"- {card_type.title()}: Special abilities and effects\n")
        f.write(f"\nGenerated {len(generated_cards)} unique cards for your {theme} themed game!\n")

    # Create README file
    with open(os.path.join(project_dir, "README.md"), 'w') as f:
        f.write(f"# {theme.title()} Card Game\n\n")
        f.write("This card game was generated using the Card Game Generator.\n\n")
        f.write(f"**Template Style:** {template_name}\n\n")
        f.write("## Contents\n")
        f.write("- `cards/`: Contains all card data (JSON) and images (PNG)\n")
        f.write("- `game_info/`: Contains game rules and documentation\n\n")
        f.write("## Cards Generated\n")
        for i, card in enumerate(generated_cards):
            f.write(f"{i+1}. **{card.name}** ({card.card_type}): {card.description}\n")

    # Create zip file
    zip_filename = f"{project_dir}.zip"
    with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, _, files in os.walk(project_dir):
            for file in files:
                file_path = os.path.join(root, file)
                zipf.write(file_path, os.path.relpath(file_path, project_dir))
    
    if progress_callback:
        progress_callback("Card game generated successfully!", total_steps, total_steps)
    
    return zip_filename

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        theme_input = sys.argv[1]
        num_cards = int(sys.argv[2]) if len(sys.argv) > 2 else 5
        template_style = sys.argv[3] if len(sys.argv) > 3 else "classic"
        
        print(f"Generating {num_cards} cards for theme: {theme_input}")
        print(f"Using template: {template_style}")
        
        zip_file = create_card_game_zip(theme_input, "./output", num_cards, template_style)
        print(f"Successfully created: {zip_file}")
    else:
        print("Usage: python3 card_generator.py <theme> [num_cards] [template_style]")
        print("Available templates:", list(get_available_templates().keys()))


