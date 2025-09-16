# PDF to Markdown Conversion Tools

This directory contains automated tools to convert the ORCA Bylaws PDF into a formatted markdown document.

## Files

- `pdf_to_markdown.py` - Main Python script for PDF to markdown conversion
- `convert_bylaws.sh` - Simple shell script wrapper for easy conversion
- `requirements.txt` - System requirements documentation
- `.github/workflows/` - GitHub Actions workflows for automatic conversion
- `Bylaws.pdf` - Original PDF document
- `Bylaws.md` - Manually formatted markdown version
- `Bylaws_auto.md` - Automatically generated markdown version

## Quick Start

### Option 1: Using the shell script (easiest)
```bash
./convert_bylaws.sh
```
This will create `Bylaws.md` with the converted content.

### Option 2: Using the Python script directly
```bash
python3 pdf_to_markdown.py Bylaws.pdf
```
This will create `Bylaws.md` with the converted content.

### Option 3: Specify custom output file
```bash
python3 pdf_to_markdown.py Bylaws.pdf MyBylaws.md
```

### Option 4: Automatic conversion with GitHub Actions
The repository includes GitHub Actions workflows that automatically convert the PDF to markdown whenever `Bylaws.pdf` is updated:

- **Simple workflow** (`.github/workflows/convert-bylaws-simple.yml`) - Basic automatic conversion
- **Advanced workflow** (`.github/workflows/convert-bylaws-advanced.yml`) - Full-featured with PR comments and detailed reporting
- **Standard workflow** (`.github/workflows/convert-bylaws.yml`) - Balanced approach with good error handling

The workflows will:
1. Trigger automatically when `Bylaws.pdf` is pushed to the repository
2. Install required dependencies (poppler-utils)
3. Run the conversion script
4. Commit the updated `Bylaws.md` file
5. Provide detailed status reports

## System Requirements

### Required Software
- **Python 3.6+** - For running the conversion script
- **poppler-utils** - For PDF text extraction (provides `pdftotext` command)

### Installation

#### macOS
```bash
brew install poppler
```

#### Ubuntu/Debian
```bash
sudo apt-get install poppler-utils
```

#### CentOS/RHEL
```bash
sudo yum install poppler-utils
```

## How It Works

1. **Text Extraction**: Uses `pdftotext` command to extract raw text from the PDF
2. **Text Cleaning**: Removes page numbers, headers, and normalizes whitespace
3. **Markdown Formatting**: Applies consistent formatting rules:
   - Converts section numbers to markdown headers
   - Formats tables properly
   - Handles mathematical formulas
   - Preserves document structure
4. **Output**: Writes formatted markdown to specified file

## Formatting Rules

The script applies the following formatting rules:

- `1.0 SECTION TITLE` → `## 1.0 SECTION TITLE`
- `3.1` → `### 3.1`
- `5.3.1` → `#### 5.3.1`
- `6.3.2.1` → `##### 6.3.2.1`
- Table data is converted to markdown tables
- Mathematical formulas are bolded
- Lists are properly formatted
- Special sections like `{unused}` are preserved

## GitHub Actions Setup

### Workflow Options

Choose the workflow that best fits your needs:

1. **Simple Workflow** (`convert-bylaws-simple.yml`)
   - Basic automatic conversion
   - Minimal configuration
   - Good for simple use cases

2. **Standard Workflow** (`convert-bylaws.yml`)
   - Balanced features
   - Good error handling
   - Detailed status reporting

3. **Advanced Workflow** (`convert-bylaws-advanced.yml`)
   - Full-featured with PR comments
   - Comprehensive validation
   - Manual trigger support
   - Detailed change tracking

### Setup Instructions

1. **Enable the workflow**: The workflows are already configured in `.github/workflows/`
2. **Push to repository**: Simply push changes to `Bylaws.pdf` to trigger conversion
3. **Manual trigger**: Use the "Actions" tab in GitHub to manually run the workflow
4. **Monitor results**: Check the Actions tab for conversion status and logs

### Workflow Features

- **Automatic triggering** on PDF changes
- **Dependency installation** (poppler-utils)
- **Error handling** and validation
- **Automatic commits** of generated markdown
- **Status reporting** with file statistics
- **Pull request integration** (advanced workflow)

## Customization

To modify the formatting rules, edit the `format_markdown()` function in `pdf_to_markdown.py`. The function contains regex patterns and formatting logic that can be adjusted for different document structures.

### Workflow Customization

You can customize the GitHub Actions workflows by:
- Modifying trigger conditions in the `on:` section
- Adding additional validation steps
- Customizing commit messages
- Adding notifications or integrations

## Troubleshooting

### Error: "pdftotext command not found"
Install poppler-utils using the installation commands above.

### Error: "PDF file not found"
Ensure the PDF file exists in the current directory or provide the full path.

### Poor formatting results
The script is optimized for the ORCA Bylaws structure. For other PDFs, you may need to modify the formatting rules in the `format_markdown()` function.

## Version History

- **v1.0** - Initial version with basic PDF to markdown conversion
- Supports ORCA Bylaws document structure
- Handles tables, headers, and mathematical formulas
- Includes shell script wrapper for easy usage
