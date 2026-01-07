#!/usr/bin/env python3
"""Setup script for html-to-pdf-tool."""

from setuptools import setup, find_packages
from pathlib import Path

# Read the contents of README file
this_directory = Path(__file__).parent
long_description = ""
readme_file = this_directory / "README.md"
if readme_file.exists():
    long_description = readme_file.read_text(encoding='utf-8')

setup(
    name='html-to-pdf-tool',
    version='1.0.0',
    description='A simple and reusable tool to convert HTML files to PDF format',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Your Name',
    author_email='your.email@example.com',
    url='https://github.com/zsnmfj-tech/html-to-pdf-tool',
    packages=find_packages(),
    package_dir={'': 'src'},
    py_modules=['html_to_pdf'],
    install_requires=[
        'weasyprint>=60.0',
    ],
    entry_points={
        'console_scripts': [
            'html2pdf=html_to_pdf:main',
        ],
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Text Processing :: Markup :: HTML',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
    ],
    python_requires='>=3.7',
    keywords='html pdf converter weasyprint',
)
