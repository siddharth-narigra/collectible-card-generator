# Troubleshooting Guide

This guide helps resolve common issues with the Card Game Generator.

## API Errors

### 502 Server Error: Bad Gateway

**Error Message:**
```
Error making API call to Pollinations.ai: 502 Server Error: Bad Gateway for url: https://text.pollinations.ai/openai
```

**Cause:**
This error occurs when the Pollinations.ai API service is temporarily unavailable or experiencing high traffic. This is an external service issue and not a problem with the card generator itself.

**Solutions:**

1. **Wait and Retry**: The most common solution is to wait a few minutes and try again. API services often experience temporary outages.

2. **Check Internet Connection**: Ensure you have a stable internet connection.

3. **Use Fallback Mode**: The card generator automatically falls back to generic card data when the API fails. While the cards won't be as creative, they will still be functional and properly formatted.

4. **Check API Status**: You can check if Pollinations.ai is experiencing issues by visiting their website or checking their status page.

### Image Generation Errors

**Error Message:**
```
Error generating image: [Various error messages]
```

**Cause:**
Image generation can fail due to API limits, network issues, or service unavailability.

**Solutions:**

1. **Fallback Images**: The generator uses placeholder images when image generation fails.

2. **Retry Later**: Image generation APIs often have rate limits or temporary outages.

3. **Check Image Prompts**: Ensure your theme doesn't contain inappropriate content that might be blocked by the AI service.

## Card Rendering Issues

### Cards Appear Blank or Missing Elements

**Symptoms:**
- Cards show no name, description, or stats
- Cards appear as blank templates
- Layout elements are missing

**Causes and Solutions:**

1. **wkhtmltopdf Not Installed**
   ```bash
   # Ubuntu/Debian:
   sudo apt-get install wkhtmltopdf
   
   # macOS:
   brew install wkhtmltopdf
   
   # Windows: Download from https://wkhtmltopdf.org/downloads.html
   ```

2. **Template File Missing**
   - Check that template files exist in the `assets/` directory
   - Verify `card_template.html` and `swiss_template.html` are present

3. **Font Loading Issues**
   - The templates use Google Fonts which require internet access
   - If offline, fonts will fall back to system defaults

4. **Data Population Issues**
   - Check that card data is being generated correctly
   - Verify the Card class has all required attributes

### Layout Problems

**Symptoms:**
- Text overlapping
- Images not displaying correctly
- Stats not aligned properly

**Solutions:**

1. **Template Validation**
   - Test templates individually using `python3 src/html_card_generator.py`
   - Check browser console for CSS errors

2. **Image Size Issues**
   - Ensure generated images are valid PNG files
   - Check image file sizes (very large files may cause issues)

3. **Text Length**
   - Very long card names or descriptions may cause layout issues
   - The templates are designed for typical card game text lengths

## Installation Issues

### Module Not Found Errors

**Error Message:**
```
ModuleNotFoundError: No module named 'requests'
```

**Solution:**
```bash
pip install -r requirements.txt
```

### Permission Errors

**Error Message:**
```
PermissionError: [Errno 13] Permission denied
```

**Solutions:**

1. **Run with appropriate permissions**
   ```bash
   # On Unix systems, you may need:
   sudo python3 main.py
   ```

2. **Check file permissions**
   ```bash
   chmod +x main.py
   ```

3. **Use virtual environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

## Performance Issues

### Slow Card Generation

**Causes:**
- AI API response times
- Image generation processing
- Network latency

**Solutions:**

1. **Reduce Number of Cards**: Start with fewer cards to test
2. **Check Network Speed**: Ensure stable, fast internet connection
3. **Be Patient**: AI generation can take 30-60 seconds per card

### Memory Issues

**Symptoms:**
- Application crashes during generation
- System becomes unresponsive

**Solutions:**

1. **Close Other Applications**: Free up system memory
2. **Generate Fewer Cards**: Reduce batch size
3. **Check Available Disk Space**: Ensure sufficient space for output files

## Quality Issues

### Poor Card Quality

**Symptoms:**
- Blurry or pixelated cards
- Poor image quality
- Text rendering issues

**Solutions:**

1. **Check wkhtmltopdf Version**
   ```bash
   wkhtmltoimage --version
   ```
   Ensure you have version 0.12.6 or later

2. **Adjust Quality Settings**: The generator uses high-quality settings by default

3. **Template Modifications**: You can edit the HTML/CSS templates for custom styling

### Inconsistent Results

**Symptoms:**
- Cards vary significantly in quality
- Some cards missing elements while others are fine

**Causes:**
- API rate limiting
- Network instability
- Temporary service issues

**Solutions:**

1. **Regenerate Problem Cards**: Delete and regenerate specific cards
2. **Check Logs**: Look for specific error messages
3. **Test with Smaller Batches**: Generate cards one at a time to isolate issues

## Getting Help

If you continue to experience issues:

1. **Check the Console Output**: Look for specific error messages
2. **Test Individual Components**: Run `html_card_generator.py` to test templates
3. **Verify Installation**: Ensure all dependencies are properly installed
4. **Check System Requirements**: Ensure your system meets minimum requirements

## System Requirements

- **Python**: 3.7 or higher
- **Internet Connection**: Required for AI APIs and Google Fonts
- **Disk Space**: At least 100MB free space for card generation
- **Memory**: Minimum 2GB RAM recommended
- **Operating System**: Windows 10+, macOS 10.14+, or Linux

## Common Error Codes

| Error Code | Description | Solution |
|------------|-------------|----------|
| 502 | Bad Gateway (API) | Wait and retry |
| 404 | Template not found | Check file paths |
| 403 | Permission denied | Check file permissions |
| ConnectionError | Network issue | Check internet connection |
| TimeoutError | Request timeout | Retry with stable connection |

Remember: The card generator includes robust fallback mechanisms, so even when APIs fail, you should still get functional cards with generic data and placeholder images.

