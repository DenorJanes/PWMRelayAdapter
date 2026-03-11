#!/bin/bash
# setup script for sova_relay project

set -euo pipefail

# This script should be run from the repository root directory (/root/sova_relay).
# It creates a Python virtual environment, installs dependencies, and sets up
# a systemd service unit for the adapter.

PROJECT_ROOT="$(pwd)"
VENV_DIR="$PROJECT_ROOT/venv"
SERVICE_NAME="sova_relay_adapter.service"
SYSTEMD_PATH="/lib/systemd/system/$SERVICE_NAME"

echo "[*] Project root: $PROJECT_ROOT"

# create venv if it doesn't exist
if [ ! -d "$VENV_DIR" ]; then
    echo "[*] Creating virtual environment..."
    python3 -m venv "$VENV_DIR"
else
    echo "[*] Virtual environment already exists, skipping creation."
fi

# activate and install
# shellcheck disable=SC1090
source "$VENV_DIR/bin/activate"

# upgrade pip and install the package (editable). this pulls in all
# dependencies declared in pyproject.toml; requirements.txt is no longer
# required.
echo "[*] Upgrading pip and installing package + dependencies..."
pip install --upgrade pip
pip install -e .

# install systemd unit
if [ -f "systemd/$SERVICE_NAME" ]; then
    echo "[*] Installing systemd service unit..."
    sudo cp "systemd/$SERVICE_NAME" "$SYSTEMD_PATH"
    sudo systemctl daemon-reload
    sudo systemctl enable "$SERVICE_NAME"
    sudo systemctl start "$SERVICE_NAME"
    echo "[*] Systemd service installed and started."
else
    echo "[!] Service file systemd/$SERVICE_NAME not found, skipping systemd setup."
fi

echo "[*] Setup complete. To run manually from the project root:
# activate the virtualenv first
source \"$VENV_DIR/bin/activate\"
# you can control verbosity with SOVA_RELAY_LOG_LEVEL (e.g. DEBUG)
python -m sova_relay"
