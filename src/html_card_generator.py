import os
import subprocess
import base64
from typing import Dict, Any

def create_html_card(card, card_image_path: str, template_path: str, output_path: str, card_number: int = 1) -> bool:
    """Create a playable card image using HTML/CSS template and wkhtmltopdf."""
    try:
        # Read the HTML template
        with open(template_path, 'r', encoding='utf-8') as f:
            html_template = f.read()
        
        # Convert image to base64 for embedding
        img_src = ""
        if os.path.exists(card_image_path):
            with open(card_image_path, 'rb') as img_file:
                img_data = base64.b64encode(img_file.read()).decode('utf-8')
                img_src = f"data:image/png;base64,{img_data}"
        else:
            print(f"Warning: Card image not found at {card_image_path}. Using placeholder.")
            img_src = "https://placehold.co/428x350/000/FFF?text=Image+Not+Found"

        # Generate stats HTML
        stats_html = ""
        if card.stats:
            for stat_name, stat_value in card.stats.items():
                stats_html += f'''
                    <div class="stat-item">
                        <div class="stat-label">{stat_name.upper()}</div>
                        <div class="stat-value">{stat_value}</div>
                    </div>
                '''
        else:
            stats_html = "No Stats Available"

        # Determine rarity based on stats (simple logic)
        total_stats = sum(card.stats.values()) if card.stats else 0
        if total_stats > 20:
            rarity = "Legendary"
        elif total_stats > 15:
            rarity = "Epic"
        elif total_stats > 10:
            rarity = "Rare"
        else:
            rarity = "Common"
        
        # Ensure description is not None or empty
        card_description = card.description if card.description else ""

        # Replace placeholders in template
        html_content = html_template.replace("{{CARD_NAME}}", card.name)
        html_content = html_content.replace("{{CARD_TYPE}}", card.card_type.title())
        html_content = html_content.replace("{{CARD_IMAGE_URL}}", img_src)
        html_content = html_content.replace("{{CARD_DESCRIPTION}}", card_description)
        html_content = html_content.replace("{{CARD_STATS}}", stats_html)
        html_content = html_content.replace("{{CARD_RARITY}}", rarity)
        html_content = html_content.replace("{{CARD_NUMBER}}", f"{card_number:03d}")
        
        # Save temporary HTML file
        temp_html_path = output_path.replace('.png', '_temp.html')
        with open(temp_html_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        # Convert HTML to image using wkhtmltopdf
        cmd = [
            'wkhtmltoimage',
            '--enable-local-file-access',
            '--width', '428',
            '--height', '571',
            '--quality', '100',
            '--format', 'png',
            '--disable-smart-width',
            '--crop-h', '571',
            '--crop-w', '428',
            '--crop-x', '0',
            '--crop-y', '0',
            temp_html_path,
            output_path
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        # Clean up temporary HTML file
        if os.path.exists(temp_html_path):
            os.remove(temp_html_path)
        
        if result.returncode == 0:
            return True
        else:
            print(f"Error converting HTML to image: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"Error creating HTML card: {e}")
        return False

def get_available_templates():
    """Get list of available card templates."""
    assets_dir = os.path.join(os.path.dirname(__file__), "..", "assets")
    templates = {}
    
    # Bright Swiss Design template
    bright_swiss_path = os.path.join(assets_dir, "bright_swiss_template.html")
    if os.path.exists(bright_swiss_path):
        templates["bright_swiss"] = {
            "name": "Bright Swiss Design",
            "description": "A modern Swiss-inspired design with bright yellow and blue accents.",
            "path": bright_swiss_path
        }

    # Detailed Representation template
    detailed_path = os.path.join(assets_dir, "detailed_representation_template.html")
    if os.path.exists(detailed_path):
        templates["detailed"] = {
            "name": "Detailed Representation",
            "description": "A detailed, ornate design with a focus on clear information hierarchy.",
            "path": detailed_path
        }
    
    return templates

def test_html_card_generation():
    """Test function to create sample cards with different templates."""
    # Create a simple card class for testing
    class TestCard:
        def __init__(self, name, description, stats, card_type):
            self.name = name
            self.description = description
            self.stats = stats
            self.card_type = card_type
    
    # Create a test card
    test_card = TestCard(
        name="Arcane Sorceress",
        description="A master of elemental magic, she weaves powerful spells that can turn the tide of battle in an instant.",
        stats={"ATK": 10, "DEF": 4, "SPD": 7, "HP": 6},
        card_type="creature"
    )
    
    # Get available templates
    templates = get_available_templates()
    
    # Test image path
    test_image_path = os.path.join(os.path.dirname(__file__), "..", "assets", "card_template.jpg")
    
    # Test each template
    for template_id, template_info in templates.items():
        output_path = os.path.join(os.path.dirname(__file__), "..", "output", f"test_card_{template_id}.png")
        
        # Ensure output directory exists
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        # Create the card
        success = create_html_card(test_card, test_image_path, template_info["path"], output_path)
        
        if success:
            print(f"Test card created successfully with {template_info['name']} template: {output_path}")
        else:
            print(f"Failed to create test card with {template_info['name']} template")

if __name__ == "__main__":
    test_html_card_generation()

