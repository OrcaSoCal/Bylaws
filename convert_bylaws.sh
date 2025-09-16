#!/bin/bash

# Simple wrapper script to convert Bylaws.pdf to markdown
# Usage: ./convert_bylaws.sh [output_filename]

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PDF_FILE="$SCRIPT_DIR/Bylaws.pdf"
OUTPUT_FILE="${1:-$SCRIPT_DIR/Bylaws.md}"

if [ ! -f "$PDF_FILE" ]; then
    echo "Error: Bylaws.pdf not found in $SCRIPT_DIR"
    exit 1
fi

echo "Converting Bylaws.pdf to markdown..."
python3 "$SCRIPT_DIR/pdf_to_markdown.py" "$PDF_FILE" "$OUTPUT_FILE"

if [ $? -eq 0 ]; then
    echo "Conversion completed successfully!"
    echo "Output file: $OUTPUT_FILE"
else
    echo "Conversion failed!"
    exit 1
fi
