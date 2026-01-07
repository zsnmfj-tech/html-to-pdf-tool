#!/usr/bin/env python3
"""Basic tests for html_to_pdf module."""

import sys
import os
from pathlib import Path

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from html_to_pdf import convert_html_to_pdf


def test_simple_html():
    """Test converting a simple HTML file."""
    # Create a simple test HTML
    test_dir = Path(__file__).parent
    test_html = test_dir / 'test_simple.html'
    test_pdf = test_dir / 'test_simple.pdf'
    
    # Create test HTML
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <title>Test Page</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; }
            h1 { color: #333; }
            p { line-height: 1.6; }
        </style>
    </head>
    <body>
        <h1>Test HTML to PDF Conversion</h1>
        <p>This is a test paragraph to verify the conversion works correctly.</p>
        <p>支持中文内容测试。</p>
    </body>
    </html>
    """
    
    test_html.write_text(html_content, encoding='utf-8')
    
    try:
        # Convert to PDF
        output = convert_html_to_pdf(str(test_html), str(test_pdf))
        
        # Check if PDF was created
        assert test_pdf.exists(), "PDF file was not created"
        assert test_pdf.stat().st_size > 0, "PDF file is empty"
        
        print(f"✓ Test passed: {output}")
        
        # Cleanup
        test_html.unlink()
        test_pdf.unlink()
        
        return True
        
    except Exception as e:
        print(f"✗ Test failed: {e}")
        # Cleanup on failure
        if test_html.exists():
            test_html.unlink()
        if test_pdf.exists():
            test_pdf.unlink()
        return False


if __name__ == '__main__':
    success = test_simple_html()
    sys.exit(0 if success else 1)
