# HTML/CSS Card Generation

This document explains the new HTML/CSS-based card generation system introduced in version 2.0 of the Card Game Generator.

## Overview

The HTML/CSS card generation system replaces the previous image manipulation approach with a more flexible and professional template-based system. This allows for:

- Better typography and text rendering
- More complex layouts and styling
- Easier customization and theming
- Professional-quality card designs
- Consistent visual appearance

## How It Works

### 1. HTML Template

The card design is defined in `assets/card_template.html`, which contains:

- **HTML Structure**: Defines the layout and content areas
- **CSS Styling**: Provides all visual styling, colors, fonts, and effects
- **Placeholder Variables**: Marked with `{{VARIABLE_NAME}}` for dynamic content

### 2. Content Injection

The `html_card_generator.py` module:

1. Reads the HTML template
2. Converts the AI-generated card image to base64 for embedding
3. Generates HTML for card stats
4. Replaces all placeholder variables with actual card data
5. Saves a temporary HTML file

### 3. Image Conversion

Using `wkhtmltoimage` (part of wkhtmltopdf):

1. Renders the HTML file as a high-quality image
2. Crops to exact card dimensions (350x490 pixels)
3. Saves as PNG format
4. Cleans up temporary files

## Template Variables

The HTML template uses the following placeholder variables:

| Variable | Description | Example |
|----------|-------------|---------|
| `{{CARD_NAME}}` | The card's name | "Fire Dragon" |
| `{{CARD_TYPE}}` | The card's type | "Creature" |
| `{{CARD_IMAGE_URL}}` | Base64-encoded image data | "data:image/png;base64,..." |
| `{{CARD_DESCRIPTION}}` | Card description text | "A mighty dragon..." |
| `{{CARD_STATS}}` | HTML for stat display | `<div class="stat-item">...</div>` |
| `{{CARD_RARITY}}` | Calculated rarity | "Epic" |
| `{{CARD_NUMBER}}` | Card number | "001" |

## Customizing the Template

### Changing Colors

Modify the CSS color values in the template:

```css
.card {
    background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
    border: 3px solid #ffd700; /* Golden border */
}

.card-name {
    color: #ffd700; /* Golden text */
}
```

### Adjusting Layout

Modify the HTML structure and CSS grid/flexbox properties:

```css
.card-stats {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(60px, 1fr));
    gap: 8px;
}
```

### Adding New Elements

Add new HTML elements and corresponding CSS:

```html
<div class="card-ability">
    <div class="ability-name">{{ABILITY_NAME}}</div>
    <div class="ability-description">{{ABILITY_DESCRIPTION}}</div>
</div>
```

### Changing Fonts

Update the Google Fonts import and font-family declarations:

```css
@import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@400;600;700&display=swap');

.card-name {
    font-family: 'Cinzel', serif;
}
```

## Rarity System

Cards are automatically assigned rarity based on their total stats:

- **Common**: Total stats ≤ 10
- **Rare**: Total stats 11-15
- **Epic**: Total stats 16-20
- **Legendary**: Total stats > 20

This can be customized in the `create_html_card` function:

```python
total_stats = sum(card.stats.values()) if card.stats else 0
if total_stats > 25:
    rarity = "Mythic"
elif total_stats > 20:
    rarity = "Legendary"
# ... etc
```

## Technical Requirements

### wkhtmltopdf Installation

The system requires `wkhtmltopdf` to be installed:

**Ubuntu/Debian:**
```bash
sudo apt-get install wkhtmltopdf
```

**macOS:**
```bash
brew install wkhtmltopdf
```

**Windows:**
Download from https://wkhtmltopdf.org/downloads.html

### Image Conversion Parameters

The conversion uses these parameters for optimal quality:

```python
cmd = [
    'wkhtmltoimage',
    '--width', '350',        # Card width
    '--height', '490',       # Card height
    '--quality', '100',      # Maximum quality
    '--format', 'png',       # PNG format
    '--disable-smart-width', # Exact dimensions
    '--crop-h', '490',       # Crop height
    '--crop-w', '350',       # Crop width
    '--crop-x', '0',         # Crop X offset
    '--crop-y', '0',         # Crop Y offset
    temp_html_path,
    output_path
]
```

## Troubleshooting

### Common Issues

1. **wkhtmltoimage not found**:
   - Ensure wkhtmltopdf is installed and in PATH
   - Try running `wkhtmltoimage --version` to test

2. **Font rendering issues**:
   - Check internet connection for Google Fonts
   - Consider using local fonts for offline use

3. **Image quality problems**:
   - Adjust the `--quality` parameter
   - Check source image resolution

4. **Layout problems**:
   - Validate HTML syntax
   - Check CSS for conflicting styles
   - Test template in a web browser first

### Debugging

To debug template issues:

1. Save the temporary HTML file (comment out the cleanup code)
2. Open the HTML file in a web browser
3. Use browser developer tools to inspect and modify CSS
4. Copy working changes back to the template

## Performance Considerations

- HTML rendering is generally faster than complex image manipulation
- Base64 encoding increases file size but ensures portability
- Template caching could be added for better performance
- Batch processing multiple cards could be optimized

## Future Enhancements

Potential improvements to the system:

- Multiple template themes
- Dynamic template selection based on card type
- Advanced layout algorithms for different content lengths
- SVG-based templates for vector graphics
- Print-ready templates with bleed areas
- Interactive card previews in the GUI

