#!/bin/bash

set -e  # exit on error

REPO_DIR="/root/livredor"
VENV_DIR="venv"
PYTHON_SCRIPT="main.py"
REQUIREMENTS_FILE="requirements.txt"

cd "$REPO_DIR"

echo "🔄 Pulling latest changes..."
git pull

# Create venv if it doesn't exist
if [ ! -d "$VENV_DIR" ]; then
    echo "🐍 Creating virtual environment..."
    python3 -m venv "$VENV_DIR"
fi

echo "🐍 Activating virtual environment..."
source "$VENV_DIR/bin/activate"

# Upgrade pip (safe & fast)
python -m pip install --upgrade pip

# Install dependencies if requirements.txt exists
if [ -f "$REQUIREMENTS_FILE" ]; then
    echo "📦 Installing dependencies..."
    pip install -r "$REQUIREMENTS_FILE"
else
    echo "⚠️ No requirements.txt found, skipping dependency install"
fi

echo "▶️ Running Python script..."
python "$PYTHON_SCRIPT"