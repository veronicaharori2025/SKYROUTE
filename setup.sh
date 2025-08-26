#!/bin/bash
# SkyRoute Setup Script for MeTTa Hackathon

echo "Setting up SkyRoute project..."
echo "==============================="

# Create virtual environment
echo "1. Creating virtual environment..."
python -m venv venv

# Activate virtual environment
echo "2. Activating virtual environment..."
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate    # Windows

# Install dependencies
echo "3. Installing dependencies..."
pip install -r requirements.txt

# Create additional directories
echo "4. Creating project structure..."
mkdir -p static/css static/images examples

# Generate requirements.txt if not exists
if [ ! -f requirements.txt ]; then
    echo "5. Generating requirements.txt..."
    pip freeze > requirements.txt
fi

echo "Setup complete!"
echo "To run the application: python app.py"
echo "To run tests: python -m pytest test_metta_integration.py -v"