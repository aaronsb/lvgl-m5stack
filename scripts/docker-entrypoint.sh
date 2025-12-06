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

cd /build/lvgl_micropython

case "$1" in
    build)
        echo "Building LVGL MicroPython for M5Stack Tough..."
        gosu builder python3 make.py esp32 --display-config=M5Stack-Tough.toml

        # Copy output to mounted volume
        if [ -d /output ]; then
            cp -r build/*.bin /output/ 2>/dev/null || echo "No .bin files found"
            chown -R "$USER_ID:$GROUP_ID" /output/
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
