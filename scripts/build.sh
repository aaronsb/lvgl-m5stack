#!/bin/bash
# Build LVGL MicroPython firmware for M5Stack Tough
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
BUILD_DIR="$PROJECT_DIR/lvgl_micropython"
CONFIG="$PROJECT_DIR/display_configs/M5Stack-Tough.toml"

# Clone lvgl_micropython if not present
if [ ! -d "$BUILD_DIR" ]; then
    echo "Cloning lvgl_micropython..."
    git clone --depth 1 https://github.com/lvgl-micropython/lvgl_micropython.git "$BUILD_DIR"
fi

# Copy our config into the build tree
cp "$CONFIG" "$BUILD_DIR/display_configs/"

cd "$BUILD_DIR"

echo "Building LVGL MicroPython for M5Stack Tough..."

python3 make.py esp32 --display-config=M5Stack-Tough.toml

echo ""
echo "Build complete!"
echo ""
echo "To flash:"
echo "  esptool.py --port /dev/ttyACM0 erase_flash"
echo "  esptool.py --port /dev/ttyACM0 --baud 460800 write_flash 0x0 build/*.bin"
