#!/usr/bin/env python3
"""
HTML to PDF Converter
A simple and reusable tool to convert HTML files to PDF format.
"""

import argparse
import sys
import os
from pathlib import Path
from weasyprint import HTML, CSS


def convert_html_to_pdf(input_path, output_path=None, base_url=None, css_files=None):
    """
    Convert an HTML file to PDF format.
    
    Args:
        input_path (str): Path to the input HTML file
        output_path (str, optional): Path to the output PDF file. 
                                     If not provided, will use input filename with .pdf extension
        base_url (str, optional): Base URL for resolving relative paths in HTML
        css_files (list, optional): List of additional CSS files to apply
    
    Returns:
        str: Path to the generated PDF file
    """
    # Validate input file
    input_file = Path(input_path)
    if not input_file.exists():
        raise FileNotFoundError(f"Input file not found: {input_path}")
    
    if not input_file.is_file():
        raise ValueError(f"Input path is not a file: {input_path}")
    
    # Determine output path
    if output_path is None:
        output_path = input_file.with_suffix('.pdf')
    else:
        output_path = Path(output_path)
    
    # Create output directory if it doesn't exist
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Set base URL if not provided (use input file's directory)
    if base_url is None:
        base_url = input_file.parent.resolve().as_uri()
    
    # Load HTML
    html = HTML(filename=str(input_file), base_url=base_url)
    
    # Load additional CSS files if provided
    stylesheets = []
    if css_files:
        for css_file in css_files:
            css_path = Path(css_file)
            if css_path.exists():
                stylesheets.append(CSS(filename=str(css_path)))
            else:
                print(f"Warning: CSS file not found: {css_file}", file=sys.stderr)
    
    # Convert to PDF
    if stylesheets:
        html.write_pdf(str(output_path), stylesheets=stylesheets)
    else:
        html.write_pdf(str(output_path))
    
    return str(output_path)


def main():
    """Main entry point for the command-line interface."""
    parser = argparse.ArgumentParser(
        description='Convert HTML files to PDF format',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s input.html
  %(prog)s input.html -o output.pdf
  %(prog)s input.html -o output.pdf -b http://example.com
  %(prog)s input.html -c style1.css -c style2.css
        """
    )
    
    parser.add_argument(
        'input',
        help='Path to the input HTML file'
    )
    
    parser.add_argument(
        '-o', '--output',
        help='Path to the output PDF file (default: same as input with .pdf extension)',
        default=None
    )
    
    parser.add_argument(
        '-b', '--base-url',
        help='Base URL for resolving relative paths in HTML',
        default=None
    )
    
    parser.add_argument(
        '-c', '--css',
        action='append',
        dest='css_files',
        help='Additional CSS file to apply (can be used multiple times)',
        default=None
    )
    
    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Enable verbose output'
    )
    
    args = parser.parse_args()
    
    try:
        if args.verbose:
            print(f"Converting {args.input} to PDF...")
            if args.base_url:
                print(f"Using base URL: {args.base_url}")
            if args.css_files:
                print(f"Additional CSS files: {', '.join(args.css_files)}")
        
        output_file = convert_html_to_pdf(
            args.input,
            args.output,
            args.base_url,
            args.css_files
        )
        
        print(f"✓ Successfully converted to: {output_file}")
        return 0
        
    except Exception as e:
        print(f"✗ Error: {e}", file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.exit(main())
