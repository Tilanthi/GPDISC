#!/bin/bash
# Build the standalone GPDISC.app for Apple Silicon (arm64).
#
#   bash app/build_mac.sh
#
# Produces dist/GPDISC.app — double-clickable, runs the consultation
# front door locally with no Python, no internet, and no LLM required
# on the target machine. Run ON the target-generation Mac (universal2
# builds would additionally need x86_64 toolchains).
set -euo pipefail
cd "$(dirname "$0")/.."

echo "== installing build dependency (local venv not required) =="
python3 -m pip install --quiet --upgrade pyinstaller

echo "== building GPDISC.app (arm64, windowed) =="
python3 -m PyInstaller \
    --noconfirm \
    --clean \
    --name "GPDISC" \
    --windowed \
    --target-platform arm64 \
    --add-data "app/index.html:." \
    --hidden-import gpdisc_core \
    app/gpdisc_app.py

echo
echo "Done: dist/GPDISC.app"
echo "Copy it wherever you like, e.g.:  cp -R dist/GPDISC.app /Applications/"
echo "First launch after moving: right-click -> Open (Gatekeeper), then it opens normally."
