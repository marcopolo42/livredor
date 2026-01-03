#!/bin/bash

set -e

while true; do
    git pull
    source venv/bin/activate
    pip install -r requirements.txt
    python main.py
    echo "❌ Script stopped — restarting in 2s..."
    sleep 2
done