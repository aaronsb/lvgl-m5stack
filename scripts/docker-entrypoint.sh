#!/bin/bash
set -e

# Get host user's uid/gid from environment or use defaults
USER_ID=${LOCAL_UID:-1000}
GROUP_ID=${LOCAL_GID:-1000}

# Create user with matching uid/gid
groupadd -g "$GROUP_ID" builder 2>/dev/null || true
useradd -u "$USER_ID" -g "$GROUP_ID" -m builder 2>/dev/null || true

# Copy config into build tree
if [ -f /config/M5Stack-Tough.toml ]; then
    cp /config/M5Stack-Tough.toml /build/lvgl_micropython/display_configs/
fi

# Copy custom frozen display.py if it exists
if [ -f /frozen/display.py ]; then
    mkdir -p /build/custom_frozen
    cp /frozen/display.py /build/custom_frozen/
fi

# Give builder user ownership of the build directory (after copying config)
chown -R "$USER_ID:$GROUP_ID" /build

cd /build/lvgl_micropython

# Function to use custom display.py for M5Stack Tough
use_custom_display_py() {
    if [ -f /build/custom_frozen/display.py ]; then
        echo "Using custom display.py with AXP192 and INVON support..."
        cp /build/custom_frozen/display.py build/display.py
        echo "Custom display.py installed"
    else
        echo "Warning: No custom display.py found, using TOML-generated version"
    fi
}

case "$1" in
    build)
        echo "Building LVGL MicroPython for M5Stack Tough..."
        # Clean previous build to ensure TOML changes take effect
        rm -rf build/
        gosu builder python3 make.py esp32 --toml=display_configs/M5Stack-Tough.toml

        # Replace with custom display.py that has AXP192 and INVON support
        use_custom_display_py

        # Rebuild to freeze the custom display.py (build system detects changed file)
        echo "Rebuilding with custom display.py..."
        gosu builder python3 make.py esp32 --toml=display_configs/M5Stack-Tough.toml

        # Copy build artifacts to mounted volume
        if [ -d /output ]; then
            # Copy firmware
            FIRMWARE=$(ls build/lvgl_micropy_*.bin 2>/dev/null | head -1)
            if [ -n "$FIRMWARE" ]; then
                cp "$FIRMWARE" /output/m5tough-lvgl-firmware.bin
                chown "$USER_ID:$GROUP_ID" /output/m5tough-lvgl-firmware.bin
            else
                echo "No combined firmware found"
            fi

            # Copy generated display.py for debugging
            if [ -f build/display.py ]; then
                cp build/display.py /output/generated-display.py
                chown "$USER_ID:$GROUP_ID" /output/generated-display.py
                echo "Copied generated display.py to output"
            fi

            # Copy the TOML config used
            cp display_configs/M5Stack-Tough.toml /output/
            chown "$USER_ID:$GROUP_ID" /output/M5Stack-Tough.toml
        fi
        echo "Build complete!"
        ;;
    shell)
        exec gosu builder /bin/bash
        ;;
    *)
        exec gosu builder "$@"
        ;;
esac
