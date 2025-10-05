#!/bin/bash
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
echo "Script is located in: $SCRIPT_DIR"

echo "Activating virtual environment..."
# Check if venv exists
if [ -d "$SCRIPT_DIR/venv" ]; then
    source "$SCRIPT_DIR/venv/bin/activate"
elif [ -d "$SCRIPT_DIR/.venv" ]; then
    source "$SCRIPT_DIR/.venv/bin/activate"
else
    echo "Virtual environment not found."
    exit 1
fi


echo "Starting fastapi backend"
fastapi run "$SCRIPT_DIR/api/api.py"
