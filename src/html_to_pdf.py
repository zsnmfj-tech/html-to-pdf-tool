#!/usr/bin/env python3
"""
HTML to PDF Converter (Pro)
A robust tool to convert HTML files to PDF format using Playwright/Chromium 
to ensure perfect layout and image preservation.
"""

import argparse
import sys
import os
import asyncio
from pathlib import Path
from bs4 import BeautifulSoup
from playwright.async_api import async_playwright


def preprocess_html(input_path):
    """
    Preprocess HTML to fix lazy loading images and relative paths.
    """
    input_file = Path(input_path).resolve()
    with open(input_file, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f, 'html.parser')

    # 1. Fix lazy loading images (common in WeChat articles)
    for img in soup.find_all('img'):
        # If data-src exists but src is missing or placeholder, swap them
        data_src = img.get('data-src')
        if data_src:
            img['src'] = data_src
            
    # 2. Convert relative paths to absolute file paths for local resources
    base_dir = input_file.parent
    for tag in soup.find_all(['img', 'link', 'script']):
        attr = 'src' if tag.name in ['img', 'script'] else 'href'
        val = tag.get(attr)
        if val and not val.startswith(('http://', 'https://', 'data:', 'file://')):
            # It's a relative path
            abs_path = (base_dir / val).resolve()
            if abs_path.exists():
                tag[attr] = abs_path.as_uri()

    # Save to a temporary file
    temp_file = input_file.parent / f"temp_{input_file.name}"
    with open(temp_file, 'w', encoding='utf-8') as f:
        f.write(str(soup))
    
    return temp_file


async def convert_html_to_pdf_playwright(input_path, output_path=None, wait_until='networkidle'):
    """
    Convert HTML to PDF using Playwright for maximum fidelity.
    """
    input_file = Path(input_path).resolve()
    
    # Preprocess to fix images
    temp_html = preprocess_html(input_file)
    
    if output_path is None:
        output_path = input_file.with_suffix('.pdf')
    else:
        output_path = Path(output_path).resolve()
    
    output_path.parent.mkdir(parents=True, exist_ok=True)

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(viewport={'width': 1280, 'height': 800})
        page = await context.new_page()
        
        # Navigate to the temporary file
        await page.goto(temp_html.as_uri(), wait_until=wait_until)
        
        # Give a little extra time for any remaining lazy loads or animations
        await asyncio.sleep(2)
        
        # Generate PDF
        await page.pdf(
            path=str(output_path),
            format='A4',
            print_background=True,
            margin={'top': '1cm', 'bottom': '1cm', 'left': '1cm', 'right': '1cm'}
        )
        
        await browser.close()
    
    # Clean up temp file
    if temp_html.exists():
        temp_html.unlink()
        
    return str(output_path)


def main():
    parser = argparse.ArgumentParser(description='Convert HTML to PDF with high fidelity using Chromium')
    parser.add_argument('input', help='Path to the input HTML file')
    parser.add_argument('-o', '--output', help='Path to the output PDF file')
    parser.add_argument('-w', '--wait', default='networkidle', help='Wait condition (load, domcontentloaded, networkidle)')
    
    args = parser.parse_args()
    
    try:
        print(f"Converting {args.input} to PDF using Chromium...")
        output_file = asyncio.run(convert_html_to_pdf_playwright(args.input, args.output, args.wait))
        print(f"✓ Successfully converted to: {output_file}")
        return 0
    except Exception as e:
        print(f"✗ Error: {e}", file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.exit(main())
