#!/usr/bin/env python3
"""
PDF to Markdown Converter Script
Converts PDF files to formatted markdown documents with consistent formatting.
"""

import sys
import os
import re
import subprocess
from pathlib import Path


def extract_pdf_text(pdf_path):
    """Extract text from PDF using pdftotext command."""
    try:
        result = subprocess.run(
            ['pdftotext', pdf_path, '-'],
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"Error extracting text from PDF: {e}")
        return None
    except FileNotFoundError:
        print("Error: pdftotext command not found. Please install poppler-utils.")
        print("On macOS: brew install poppler")
        return None


def clean_text(text):
    """Clean and normalize the extracted text."""
    # Remove page numbers and headers/footers
    text = re.sub(r'^\d+/\d+\s*$', '', text, flags=re.MULTILINE)
    text = re.sub(r'^ORCA Bylaws 9-16-25\.doc\s*$', '', text, flags=re.MULTILINE)
    
    # Clean up excessive whitespace
    text = re.sub(r'\n\s*\n\s*\n+', '\n\n', text)
    text = re.sub(r'[ \t]+', ' ', text)
    
    # Remove trailing whitespace from lines
    text = '\n'.join(line.rstrip() for line in text.split('\n'))
    
    return text.strip()


def format_markdown(text):
    """Convert plain text to formatted markdown."""
    lines = text.split('\n')
    markdown_lines = []
    in_table = False
    
    for i, line in enumerate(lines):
        line = line.strip()
        if not line:
            markdown_lines.append('')
            continue
            
        # Handle main title
        if line.startswith('OCEAN RACING CATAMARAN ASSOCIATION'):
            markdown_lines.append('# ORCA Bylaws')
            markdown_lines.append('')
            markdown_lines.append('**OCEAN RACING CATAMARAN ASSOCIATION (ORCA), INCORPORATED**')
            markdown_lines.append('')
            continue
            
        # Handle approval date
        if 'Approved by the ORCA Board' in line:
            markdown_lines.append(f'*{line}.*')
            markdown_lines.append('')
            markdown_lines.append('---')
            markdown_lines.append('')
            continue
            
        # Handle section headers (1.0, 2.0, etc.)
        if re.match(r'^\d+\.\d+\s+[A-Z]', line):
            section_match = re.match(r'^(\d+\.\d+)\s+(.+)', line)
            if section_match:
                section_num, title = section_match.groups()
                markdown_lines.append(f'## {section_num} {title}')
                markdown_lines.append('')
            continue
            
        # Handle subsection headers (3.1, 3.2, etc.)
        if re.match(r'^\d+\.\d+$', line):
            markdown_lines.append(f'### {line}')
            markdown_lines.append('')
            continue
            
        # Handle sub-subsection headers (5.3.1, 5.3.2, etc.)
        if re.match(r'^\d+\.\d+\.\d+$', line):
            markdown_lines.append(f'#### {line}')
            markdown_lines.append('')
            continue
            
        # Handle sub-sub-subsection headers (6.3.2.1, etc.)
        if re.match(r'^\d+\.\d+\.\d+\.\d+$', line):
            markdown_lines.append(f'##### {line}')
            markdown_lines.append('')
            continue
            
        # Handle table headers and data
        if 'BOAT LWL, FEET' in line or 'MINIMUM QUALIFIED CREW' in line:
            if not in_table:
                markdown_lines.append('| BOAT LWL, FEET | MINIMUM QUALIFIED CREW |')
                markdown_lines.append('|----------------|------------------------|')
                in_table = True
            continue
            
        # Handle table data rows
        if in_table and re.match(r'^\d+\.\d+.*\d+$', line):
            parts = line.split()
            if len(parts) >= 2:
                lwl_range = ' '.join(parts[:-1])
                crew_count = parts[-1]
                markdown_lines.append(f'| {lwl_range} | {crew_count} |')
            continue
            
        # Handle mathematical formulas
        if 'Corrected Time =' in line:
            markdown_lines.append(f'**{line}**')
            markdown_lines.append('')
            continue
            
        # Handle list items that start with dashes
        if line.startswith('- ') and not line.startswith('--'):
            markdown_lines.append(f'- {line[2:]}')
            continue
            
        # Handle special formatting for subsections
        if line.startswith('items align with section'):
            markdown_lines.append(f'*{line}*')
            markdown_lines.append('')
            continue
            
        # Handle unused sections
        if line == '{unused}':
            markdown_lines.append(f'### {line}')
            markdown_lines.append('')
            continue
            
        # Regular paragraph text
        if line:
            # Check if this is a continuation of the previous line
            if markdown_lines and not markdown_lines[-1].startswith('#') and not markdown_lines[-1].startswith('|') and not markdown_lines[-1].startswith('-') and markdown_lines[-1] != '':
                markdown_lines[-1] += ' ' + line
            else:
                markdown_lines.append(line)
    
    return '\n'.join(markdown_lines)


def add_final_formatting(markdown_text):
    """Add final formatting touches to the markdown."""
    # Add proper spacing around headers
    markdown_text = re.sub(r'\n(#{1,6}[^#\n]+)\n([^#\n])', r'\n\1\n\n\2', markdown_text)
    
    # Add spacing around tables
    markdown_text = re.sub(r'\n(\|[^|\n]+\|)\n([^|\n])', r'\n\1\n\n\2', markdown_text)
    
    # Clean up multiple newlines
    markdown_text = re.sub(r'\n{3,}', '\n\n', markdown_text)
    
    return markdown_text


def convert_pdf_to_markdown(pdf_path, output_path=None):
    """Main conversion function."""
    pdf_path = Path(pdf_path)
    
    if not pdf_path.exists():
        print(f"Error: PDF file '{pdf_path}' not found.")
        return False
    
    if output_path is None:
        output_path = pdf_path.with_suffix('.md')
    else:
        output_path = Path(output_path)
    
    print(f"Converting '{pdf_path}' to '{output_path}'...")
    
    # Extract text from PDF
    raw_text = extract_pdf_text(pdf_path)
    if raw_text is None:
        return False
    
    # Clean the text
    cleaned_text = clean_text(raw_text)
    
    # Convert to markdown
    markdown_text = format_markdown(cleaned_text)
    
    # Add final formatting
    final_markdown = add_final_formatting(markdown_text)
    
    # Write to output file
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(final_markdown)
        print(f"Successfully converted to '{output_path}'")
        return True
    except Exception as e:
        print(f"Error writing output file: {e}")
        return False


def main():
    """Main function to handle command line arguments."""
    if len(sys.argv) < 2:
        print("Usage: python pdf_to_markdown.py <pdf_file> [output_file]")
        print("Example: python pdf_to_markdown.py Bylaws.pdf")
        print("Example: python pdf_to_markdown.py Bylaws.pdf output.md")
        sys.exit(1)
    
    pdf_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else None
    
    success = convert_pdf_to_markdown(pdf_file, output_file)
    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
