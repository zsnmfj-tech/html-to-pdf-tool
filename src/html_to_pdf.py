#!/usr/bin/env python3
"""
HTML to PDF Converter (Optimized)
A simple and reusable tool to convert HTML files to PDF format while preserving 
layout, fonts, and images.
"""

import argparse
import sys
import os
from pathlib import Path
from weasyprint import HTML, CSS
from weasyprint.text.fonts import FontConfiguration


def convert_html_to_pdf(input_path, output_path=None, base_url=None, css_files=None, media_type='print'):
    """
    Convert an HTML file to PDF format with high fidelity.
    
    Args:
        input_path (str): Path to the input HTML file
        output_path (str, optional): Path to the output PDF file
        base_url (str, optional): Base URL for resolving relative paths
        css_files (list, optional): List of additional CSS files to apply
        media_type (str, optional): Media type for CSS (default: 'print')
    
    Returns:
        str: Path to the generated PDF file
    """
    # Validate input file
    input_file = Path(input_path).resolve()
    if not input_file.exists():
        raise FileNotFoundError(f"Input file not found: {input_path}")
    
    # Determine output path
    if output_path is None:
        output_path = input_file.with_suffix('.pdf')
    else:
        output_path = Path(output_path).resolve()
    
    # Create output directory if it doesn't exist
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Set base URL if not provided (use input file's directory)
    if base_url is None:
        base_url = input_file.parent.as_uri()
    elif not base_url.startswith(('http://', 'https://', 'file://')):
        base_url = Path(base_url).resolve().as_uri()
    
    # Font configuration for better font handling
    font_config = FontConfiguration()
    
    # Load HTML
    html = HTML(filename=str(input_file), base_url=base_url, media_type=media_type)
    
    # Load additional CSS files if provided
    stylesheets = []
    if css_files:
        for css_file in css_files:
            css_path = Path(css_file).resolve()
            if css_path.exists():
                stylesheets.append(CSS(filename=str(css_path), font_config=font_config))
            else:
                print(f"Warning: CSS file not found: {css_file}", file=sys.stderr)
    
    # Convert to PDF with optimized settings
    # We use presentational_hints=True to support some legacy HTML attributes
    html.write_pdf(
        str(output_path), 
        stylesheets=stylesheets, 
        font_config=font_config,
        presentational_hints=True
    )
    
    return str(output_path)


def main():
    """Main entry point for the command-line interface."""
    parser = argparse.ArgumentParser(
        description='Convert HTML files to PDF format with high fidelity',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument('input', help='Path to the input HTML file')
    parser.add_argument('-o', '--output', help='Path to the output PDF file')
    parser.add_argument('-b', '--base-url', help='Base URL for resolving relative paths')
    parser.add_argument('-c', '--css', action='append', dest='css_files', help='Additional CSS file')
    parser.add_argument('-m', '--media-type', default='print', help='Media type (print or screen)')
    parser.add_argument('-v', '--verbose', action='store_true', help='Enable verbose output')
    
    args = parser.parse_args()
    
    try:
        if args.verbose:
            print(f"Converting {args.input} to PDF...")
            print(f"Base URL: {args.base_url or 'Auto-detected'}")
            print(f"Media Type: {args.media_type}")
        
        output_file = convert_html_to_pdf(
            args.input,
            args.output,
            args.base_url,
            args.css_files,
            args.media_type
        )
        
        print(f"✓ Successfully converted to: {output_file}")
        return 0
        
    except Exception as e:
        print(f"✗ Error: {e}", file=sys.stderr)
        import traceback
        if args.verbose:
            traceback.print_exc()
        return 1


if __name__ == '__main__':
    sys.exit(main())
