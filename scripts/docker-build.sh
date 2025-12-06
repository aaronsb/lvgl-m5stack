#!/bin/bash
# Build M5Stack Tough LVGL firmware using Docker
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"

cd "$PROJECT_DIR"

# Build the container (uses cache if available)
echo "Building Docker image..."
docker build -t m5tough-lvgl .

# Create output directory
mkdir -p output

# Run the build with host user's uid/gid
echo "Building firmware..."
docker run --rm \
    -e LOCAL_UID=$(id -u) \
    -e LOCAL_GID=$(id -g) \
    -v "$PROJECT_DIR/display_configs:/config:ro" \
    -v "$PROJECT_DIR/output:/output" \
    m5tough-lvgl build

echo ""
echo "Firmware available in: $PROJECT_DIR/output/"
ls -la output/*.bin 2>/dev/null || echo "No firmware files found"
