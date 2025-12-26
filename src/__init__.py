"""
Card Game Generator - Source Package

This package contains the core modules for generating custom trading card games.
"""

from .card_generator import Card, generate_card_data, generate_card_image, create_card_game_zip
from .html_card_generator import create_html_card, get_available_templates

__version__ = "1.0.0"
__author__ = "Card Game Generator Team"

__all__ = [
    "Card",
    "generate_card_data",
    "generate_card_image",
    "create_card_game_zip",
    "create_html_card",
    "get_available_templates",
]
