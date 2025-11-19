#!/bin/bash
# Setup script for Unix-like systems (Linux/macOS)

echo "Installing dependencies for Pandora's Metal Box..."

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed or not in PATH"
    exit 1
fi

# Install requirements
echo "Installing required packages..."
python3 -m pip install -r requirements.txt

if [ $? -ne 0 ]; then
    echo "Error: Failed to install dependencies"
    exit 1
fi

echo "Dependencies installed successfully!"
echo "Running Pandora's Metal Box..."
python3 main.py