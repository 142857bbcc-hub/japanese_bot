#!/bin/bash

set -euo pipefail

APP_NAME="kana_bot"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SOURCE_FILE="${1:-$SCRIPT_DIR/kana_bot.py}"
OUTPUT_FILE="$SCRIPT_DIR/$APP_NAME"

if [ ! -f "$SOURCE_FILE" ]; then
    echo "Error: source file not found: $SOURCE_FILE"
    echo "Pass the path to your Python file as the first argument."
    exit 1
fi

if ! command -v python3 >/dev/null 2>&1; then
    echo "Error: python3 is not installed or not on your PATH."
    exit 1
fi

BUILD_DIR="$(mktemp -d)"
cleanup() {
    rm -rf "$BUILD_DIR"
}
trap cleanup EXIT

unset PLAYWRIGHT_BROWSERS_PATH

echo "==> Creating temporary virtual environment..."
python3 -m venv "$BUILD_DIR/venv"
source "$BUILD_DIR/venv/bin/activate"

echo "==> Installing dependencies (playwright, pyinstaller)..."
python -m pip install --quiet --upgrade pip
python -m pip install --quiet playwright pyinstaller

echo "==> Installing the Playwright Chromium browser..."
python -m playwright install chromium

cat > "$BUILD_DIR/rthook_playwright.py" << 'PYEOF'
import os
import sys
from pathlib import Path

if "PLAYWRIGHT_BROWSERS_PATH" not in os.environ:
    if sys.platform == "darwin":
        browsers_path = Path.home() / "Library" / "Caches" / "ms-playwright"
    elif sys.platform == "win32":
        local_app_data = os.environ.get("LOCALAPPDATA")
        base = Path(local_app_data) if local_app_data else Path.home() / "AppData" / "Local"
        browsers_path = base / "ms-playwright"
    else:
        browsers_path = Path.home() / ".cache" / "ms-playwright"
    os.environ["PLAYWRIGHT_BROWSERS_PATH"] = str(browsers_path)
PYEOF

echo "==> Building executable with PyInstaller..."
python -m PyInstaller \
    --noconfirm \
    --clean \
    --onefile \
    --name "$APP_NAME" \
    --collect-all playwright \
    --runtime-hook "$BUILD_DIR/rthook_playwright.py" \
    --distpath "$BUILD_DIR/dist" \
    --workpath "$BUILD_DIR/build" \
    --specpath "$BUILD_DIR" \
    "$SOURCE_FILE"

if [ ! -f "$BUILD_DIR/dist/$APP_NAME" ]; then
    echo "Error: build finished but the executable was not found."
    exit 1
fi

echo "==> Placing executable in $SCRIPT_DIR ..."
if [ -e "$OUTPUT_FILE" ]; then
    echo "    Existing $APP_NAME found - replacing it."
    rm -f "$OUTPUT_FILE"
fi

cp "$BUILD_DIR/dist/$APP_NAME" "$OUTPUT_FILE"
chmod +x "$OUTPUT_FILE"

echo ""
echo "Done! Executable created at:"
echo "    $OUTPUT_FILE"
echo "Run it with:  \"$OUTPUT_FILE\""