#!/bin/bash
# Setup script for ABAP SQL Syntax Checker

echo "=================================="
echo "ABAP SQL Syntax Checker - Setup"
echo "=================================="
echo ""

# Check Python version
echo "Checking Python version..."
python_version=$(python --version 2>&1)
echo "Found: $python_version"

if ! command -v python &> /dev/null; then
    echo "❌ Error: Python is not installed"
    exit 1
fi

# Create virtual environment (optional but recommended)
read -p "Create a virtual environment? (recommended) [y/N]: " create_venv
if [[ $create_venv =~ ^[Yy]$ ]]; then
    echo ""
    echo "Creating virtual environment..."
    python -m venv venv
    
    echo "Activating virtual environment..."
    if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
        source venv/Scripts/activate
    else
        source venv/bin/activate
    fi
    echo "✓ Virtual environment activated"
fi

# Install dependencies
echo ""
echo "Installing dependencies..."
pip install -q -r requirements.txt

if [ $? -eq 0 ]; then
    echo "✓ Dependencies installed successfully"
else
    echo "❌ Error installing dependencies"
    exit 1
fi

# Run tests
echo ""
echo "Running tests..."
python test_checker.py

if [ $? -eq 0 ]; then
    echo ""
    echo "✓ All tests passed!"
else
    echo ""
    echo "❌ Some tests failed"
    exit 1
fi

# Run demo
echo ""
read -p "Run demo? [Y/n]: " run_demo
if [[ ! $run_demo =~ ^[Nn]$ ]]; then
    echo ""
    echo "Running demo..."
    python abap_sql_checker.py
fi

echo ""
echo "=================================="
echo "✨ Setup complete!"
echo "=================================="
echo ""
echo "Quick commands:"
echo "  - Run demo:        python abap_sql_checker.py"
echo "  - Interactive:     python interactive_checker.py"
echo "  - Run tests:       python test_checker.py"
echo "  - Batch validate:  python batch_validator.py <file/dir>"
echo ""
echo "See QUICKSTART.md for more examples"
echo ""

