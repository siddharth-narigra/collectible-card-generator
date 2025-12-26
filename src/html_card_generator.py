"""
HTML Card Generator Module

This module handles the conversion of card data into visual card images
using HTML/CSS templates and the wkhtmltoimage utility.
"""

import base64
import os
import subprocess
from pathlib import Path
from typing import Any, Protocol


# =============================================================================
# Type Definitions
# =============================================================================

class CardProtocol(Protocol):
    """Protocol defining the expected interface for a Card object."""
    name: str
    description: str
    stats: dict[str, int]
    card_type: str


# =============================================================================
# Constants
# =============================================================================

CARD_WIDTH = 428
CARD_HEIGHT = 571
ASSETS_DIR = Path(__file__).parent.parent / "assets"

# Template definitions
TEMPLATES = {
    "bright_swiss": {
        "filename": "bright_swiss_template.html",
        "name": "Bright Swiss Design",
        "description": "A modern Swiss-inspired design with bright yellow and blue accents.",
    },
    "detailed": {
        "filename": "detailed_representation_template.html",
        "name": "Detailed Representation",
        "description": "A detailed, ornate design with a focus on clear information hierarchy.",
    },
}


# =============================================================================
# Helper Functions
# =============================================================================

def _encode_image_to_base64(image_path: str) -> str:
    """
    Encode an image file to a base64 data URL.
    
    Args:
        image_path: Path to the image file
    
    Returns:
        A base64 data URL string, or a placeholder URL if the file doesn't exist.
    """
    if os.path.exists(image_path):
        with open(image_path, 'rb') as img_file:
            img_data = base64.b64encode(img_file.read()).decode('utf-8')
            return f"data:image/png;base64,{img_data}"
    
    print(f"Warning: Card image not found at {image_path}. Using placeholder.")
    return "https://placehold.co/428x350/000/FFF?text=Image+Not+Found"


def _generate_stats_html(stats: dict[str, int]) -> str:
    """
    Generate HTML markup for card statistics.
    
    Args:
        stats: Dictionary of stat names to values
    
    Returns:
        HTML string representing the stats.
    """
    if not stats:
        return "No Stats Available"
    
    html_parts = []
    for stat_name, stat_value in stats.items():
        html_parts.append(f'''
            <div class="stat-item">
                <div class="stat-label">{stat_name.upper()}</div>
                <div class="stat-value">{stat_value}</div>
            </div>
        ''')
    
    return ''.join(html_parts)


def _determine_rarity(stats: dict[str, int]) -> str:
    """
    Determine card rarity based on total stat values.
    
    Args:
        stats: Dictionary of stat names to values
    
    Returns:
        Rarity string: "Legendary", "Epic", "Rare", or "Common"
    """
    total = sum(stats.values()) if stats else 0
    
    if total > 20:
        return "Legendary"
    elif total > 15:
        return "Epic"
    elif total > 10:
        return "Rare"
    return "Common"


def _run_wkhtmltoimage(html_path: str, output_path: str) -> bool:
    """
    Convert an HTML file to an image using wkhtmltoimage.
    
    Args:
        html_path: Path to the HTML file to convert
        output_path: Path where the output image should be saved
    
    Returns:
        True if conversion was successful, False otherwise.
    """
    cmd = [
        'wkhtmltoimage',
        '--enable-local-file-access',
        '--width', str(CARD_WIDTH),
        '--height', str(CARD_HEIGHT),
        '--quality', '100',
        '--format', 'png',
        '--disable-smart-width',
        '--crop-h', str(CARD_HEIGHT),
        '--crop-w', str(CARD_WIDTH),
        '--crop-x', '0',
        '--crop-y', '0',
        html_path,
        output_path
    ]
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode != 0:
        print(f"Error converting HTML to image: {result.stderr}")
        return False
    
    return True


# =============================================================================
# Main Functions
# =============================================================================

def get_available_templates() -> dict[str, dict[str, Any]]:
    """
    Get a dictionary of available card templates.
    
    Returns:
        Dictionary mapping template IDs to template info dictionaries.
        Each template info contains: name, description, and path.
    """
    templates = {}
    
    for template_id, info in TEMPLATES.items():
        template_path = ASSETS_DIR / info["filename"]
        
        if template_path.exists():
            templates[template_id] = {
                "name": info["name"],
                "description": info["description"],
                "path": str(template_path),
            }
    
    return templates


def create_html_card(
    card: CardProtocol,
    card_image_path: str,
    template_path: str,
    output_path: str,
    card_number: int = 1
) -> bool:
    """
    Create a playable card image using an HTML/CSS template.
    
    This function reads an HTML template, populates it with card data,
    and converts it to a PNG image using wkhtmltoimage.
    
    Args:
        card: Card object with name, description, stats, and card_type
        card_image_path: Path to the card's artwork image
        template_path: Path to the HTML template file
        output_path: Path where the final card image should be saved
        card_number: Card number for display on the card
    
    Returns:
        True if the card was created successfully, False otherwise.
    """
    try:
        # Read the HTML template
        with open(template_path, 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        # Prepare template data
        img_src = _encode_image_to_base64(card_image_path)
        stats_html = _generate_stats_html(card.stats)
        rarity = _determine_rarity(card.stats)
        description = card.description or ""
        
        # Replace placeholders
        replacements = {
            "{{CARD_NAME}}": card.name,
            "{{CARD_TYPE}}": card.card_type.title(),
            "{{CARD_IMAGE_URL}}": img_src,
            "{{CARD_DESCRIPTION}}": description,
            "{{CARD_STATS}}": stats_html,
            "{{CARD_RARITY}}": rarity,
            "{{CARD_NUMBER}}": f"{card_number:03d}",
        }
        
        for placeholder, value in replacements.items():
            html_content = html_content.replace(placeholder, value)
        
        # Save temporary HTML file
        temp_html_path = output_path.replace('.png', '_temp.html')
        with open(temp_html_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        # Convert to image
        success = _run_wkhtmltoimage(temp_html_path, output_path)
        
        # Clean up temporary file
        if os.path.exists(temp_html_path):
            os.remove(temp_html_path)
        
        return success
        
    except FileNotFoundError as e:
        print(f"Template file not found: {e}")
        return False
    except Exception as e:
        print(f"Error creating HTML card: {e}")
        return False


# =============================================================================
# Test Function
# =============================================================================

def test_html_card_generation() -> None:
    """Test card generation with sample data for all available templates."""
    from dataclasses import dataclass
    
    @dataclass
    class TestCard:
        name: str
        description: str
        stats: dict[str, int]
        card_type: str
    
    test_card = TestCard(
        name="Arcane Sorceress",
        description="A master of elemental magic, she weaves powerful spells.",
        stats={"ATK": 10, "DEF": 4, "SPD": 7, "HP": 6},
        card_type="creature"
    )
    
    templates = get_available_templates()
    test_image = ASSETS_DIR / "card_template.jpg"
    output_dir = Path(__file__).parent.parent / "output"
    output_dir.mkdir(exist_ok=True)
    
    for template_id, template_info in templates.items():
        output_path = output_dir / f"test_card_{template_id}.png"
        
        success = create_html_card(
            test_card,
            str(test_image),
            template_info["path"],
            str(output_path)
        )
        
        if success:
            print(f"✓ Test card created: {template_info['name']} -> {output_path}")
        else:
            print(f"✗ Failed: {template_info['name']}")


if __name__ == "__main__":
    test_html_card_generation()
