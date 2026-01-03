#!/bin/bash

set -e  # stop on error

REPO_DIR="$HOME/livredor"
PYTHON_SCRIPT="main.py"

cd "$REPO_DIR"

echo "🔄 Pulling latest changes..."
git pull

echo "▶️ Running Python script..."
python3 "$PYTHON_SCRIPT"