# GitHub Actions Setup Guide

This guide explains how to set up automatic PDF to markdown conversion using GitHub Actions.

## 🚀 Quick Setup

The workflows are already configured in this repository. Simply push your changes to `Bylaws.pdf` and the conversion will happen automatically!

## 📋 Available Workflows

### 1. Simple Workflow (`convert-bylaws-simple.yml`)
**Best for**: Basic automatic conversion with minimal complexity

```yaml
# Triggers on PDF changes
on:
  push:
    paths: ['Bylaws.pdf']
  workflow_dispatch:  # Manual trigger
```

**Features**:
- ✅ Automatic conversion on PDF changes
- ✅ Simple error handling
- ✅ Automatic commit of results
- ✅ Manual trigger support

### 2. Standard Workflow (`convert-bylaws.yml`)
**Best for**: Balanced approach with good error handling

**Features**:
- ✅ All simple workflow features
- ✅ Detailed validation
- ✅ File size reporting
- ✅ Change detection
- ✅ Comprehensive status reporting

### 3. Advanced Workflow (`convert-bylaws-advanced.yml`)
**Best for**: Full-featured setup with PR integration

**Features**:
- ✅ All standard workflow features
- ✅ Pull request comments with previews
- ✅ Comprehensive validation
- ✅ Detailed change tracking
- ✅ Enhanced error handling
- ✅ Workflow summaries

## 🛠️ Setup Instructions

### Step 1: Choose Your Workflow

1. **For simple use**: Keep `convert-bylaws-simple.yml` enabled
2. **For balanced features**: Use `convert-bylaws.yml`
3. **For full features**: Use `convert-bylaws-advanced.yml`

### Step 2: Enable the Workflow

The workflows are already in `.github/workflows/`. They will automatically activate when you push to GitHub.

### Step 3: Test the Workflow

1. Make a small change to `Bylaws.pdf`
2. Commit and push the change
3. Go to the "Actions" tab in your GitHub repository
4. Watch the workflow run automatically

## 🔧 Configuration Options

### Trigger Conditions

Modify the `on:` section in any workflow to change when it runs:

```yaml
on:
  push:
    branches: [ main, master ]  # Specific branches
    paths: [ 'Bylaws.pdf' ]     # Only on PDF changes
  pull_request:
    paths: [ 'Bylaws.pdf' ]     # Also on PRs
  workflow_dispatch:            # Manual trigger
  schedule:
    - cron: '0 0 * * 1'         # Weekly on Mondays
```

### Custom Commit Messages

Modify the commit message in the workflow:

```yaml
- name: Commit changes
  run: |
    git commit -m "Your custom commit message here"
```

### Add Notifications

Add notification steps to any workflow:

```yaml
- name: Notify on success
  if: success()
  run: |
    echo "✅ Conversion completed successfully!"
    # Add your notification logic here
```

## 📊 Monitoring and Debugging

### View Workflow Runs

1. Go to your repository on GitHub
2. Click the "Actions" tab
3. Select the workflow from the left sidebar
4. Click on any run to see detailed logs

### Common Issues

#### Workflow Not Triggering
- Check that `Bylaws.pdf` is in the root directory
- Verify the workflow file is in `.github/workflows/`
- Ensure the file has a `.yml` extension

#### Conversion Fails
- Check the workflow logs for error messages
- Verify `pdf_to_markdown.py` exists and is executable
- Ensure the PDF file is valid and readable

#### No Changes Committed
- The workflow only commits if there are actual changes
- Check if the markdown output is identical to the existing file
- Verify git permissions for the workflow

### Debug Mode

Add debug output to any workflow:

```yaml
- name: Debug information
  run: |
    echo "Current directory: $(pwd)"
    echo "Files present: $(ls -la)"
    echo "PDF info: $(file Bylaws.pdf)"
    echo "Script info: $(file pdf_to_markdown.py)"
```

## 🔄 Workflow Lifecycle

1. **Trigger**: Workflow starts when `Bylaws.pdf` changes
2. **Setup**: Installs Python and poppler-utils
3. **Validation**: Checks files exist and are valid
4. **Conversion**: Runs the PDF to markdown script
5. **Validation**: Verifies the output markdown
6. **Commit**: Commits changes if any were made
7. **Report**: Provides status summary

## 🎯 Best Practices

### Security
- Use `GITHUB_TOKEN` for repository access
- Don't hardcode sensitive information
- Use environment variables for configuration

### Performance
- Use `fetch-depth: 0` only when needed
- Cache dependencies when possible
- Use specific Python versions

### Reliability
- Add proper error handling
- Validate inputs and outputs
- Use meaningful commit messages
- Provide clear status reporting

## 📝 Customization Examples

### Add File Size Limits

```yaml
- name: Check PDF size
  run: |
    size=$(stat -c%s Bylaws.pdf)
    if [ $size -gt 10485760 ]; then  # 10MB limit
      echo "❌ PDF too large: $size bytes"
      exit 1
    fi
    echo "✅ PDF size OK: $size bytes"
```

### Add Conversion Timeout

```yaml
- name: Convert with timeout
  run: |
    timeout 300 python3 pdf_to_markdown.py Bylaws.pdf Bylaws.md
```

### Add Multiple Output Formats

```yaml
- name: Convert to multiple formats
  run: |
    python3 pdf_to_markdown.py Bylaws.pdf Bylaws.md
    python3 pdf_to_markdown.py Bylaws.pdf Bylaws_simple.md --simple
```

## 🆘 Getting Help

If you encounter issues:

1. Check the workflow logs in the Actions tab
2. Verify all files are present and correct
3. Test the conversion script locally first
4. Check the GitHub Actions documentation
5. Review the workflow syntax with a YAML validator

## 📚 Additional Resources

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Workflow Syntax Reference](https://docs.github.com/en/actions/reference/workflow-syntax-for-github-actions)
- [Actions Marketplace](https://github.com/marketplace?type=actions)
