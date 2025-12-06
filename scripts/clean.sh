#!/bin/bash
# Clean build artifacts and optionally Docker cache
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"

cd "$PROJECT_DIR"

echo "Cleaning local build artifacts..."
rm -rf lvgl_micropython/
rm -rf output/
rm -rf build/
rm -f *.bin

if [ "$1" = "--docker" ]; then
    echo "Removing Docker image..."
    docker rmi m5tough-lvgl 2>/dev/null || true
    echo "To fully clean Docker build cache: docker builder prune"
fi

echo "Clean complete."
