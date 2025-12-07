#!/bin/bash
# Build M5Stack Tough LVGL firmware using Docker
# Outputs minimal progress info; full log saved to file
# Usage: ./docker-build.sh [--rebuild]
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
LOG_DIR="$PROJECT_DIR/output"
LOG_FILE="$LOG_DIR/build-$(date +%Y%m%d-%H%M%S).log"

# Parse arguments
DOCKER_BUILD_OPTS=""
if [[ "$1" == "--rebuild" ]]; then
    DOCKER_BUILD_OPTS="--no-cache"
    echo "Rebuild mode: ignoring Docker cache"
fi

cd "$PROJECT_DIR"
mkdir -p "$LOG_DIR"

echo "M5Stack Tough LVGL Build"
echo "========================"
echo "Log: $LOG_FILE"
echo ""

# Phase 1: Docker image
echo "[1/3] Building Docker image..."
docker build $DOCKER_BUILD_OPTS -t m5tough-lvgl . >> "$LOG_FILE" 2>&1
echo "      Done."

# Phase 2: Firmware compilation
echo "[2/3] Compiling firmware (this takes several minutes)..."
docker run --rm \
    -e LOCAL_UID=$(id -u) \
    -e LOCAL_GID=$(id -g) \
    -v "$PROJECT_DIR/display_configs:/config:ro" \
    -v "$PROJECT_DIR/frozen:/frozen:ro" \
    -v "$PROJECT_DIR/output:/output" \
    m5tough-lvgl build >> "$LOG_FILE" 2>&1
echo "      Done."

# Phase 3: Check results
echo "[3/3] Checking output..."
FIRMWARE="$LOG_DIR/m5tough-lvgl-firmware.bin"
if [ -f "$FIRMWARE" ]; then
    SIZE=$(ls -lh "$FIRMWARE" | awk '{print $5}')
    echo ""
    echo "SUCCESS - Firmware ready:"
    echo "  $FIRMWARE ($SIZE)"
    echo ""
    echo "Flash with:"
    echo "  esptool.py --port /dev/ttyACM0 --baud 460800 erase_flash"
    echo "  esptool.py --port /dev/ttyACM0 --baud 460800 write_flash 0x0 $FIRMWARE"
else
    echo ""
    echo "FAILED - No firmware produced. Check log:"
    echo "  $LOG_FILE"
    exit 1
fi
