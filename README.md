# M5Stack Tough - LVGL MicroPython Firmware

Pre-built LVGL MicroPython firmware for M5Stack Tough. No UIFlow, no cloud accounts - just flash and code.

## Quick Start

### 1. Download Firmware

Get the latest `m5tough-lvgl-firmware.bin` from [Releases](../../releases).

### 2. Flash to Device

```bash
pip install esptool
esptool.py --port /dev/ttyACM0 --baud 460800 erase_flash
esptool.py --port /dev/ttyACM0 --baud 460800 write_flash 0x0 m5tough-lvgl-firmware.bin
```

### 3. Write Your App

```python
import display  # Auto-initializes display + LVGL
import lvgl as lv

# Create UI
scr = lv.screen_active()
scr.set_style_bg_color(lv.color_hex(0x003366), 0)

label = lv.label(scr)
label.set_text("Hello M5Stack!")
label.set_style_text_color(lv.color_hex(0xFFFFFF), 0)
label.center()
```

Upload with: `mpremote connect /dev/ttyACM0 cp main.py :`

## Hardware

- **MCU**: ESP32-D0WDQ6-V3 with PSRAM
- **Display**: ILI9342C 320x240 (ILI9341 compatible)
- **Touch**: Capacitive @ I2C 0x2E (not yet configured)
- **Power**: AXP192 @ I2C 0x34

### Pin Reference

| Function | GPIO |
|----------|------|
| SPI MOSI | 23   |
| SPI MISO | 19   |
| SPI SCLK | 18   |
| LCD CS   | 5    |
| LCD DC   | 15   |
| LCD RST  | 33   |
| LCD BL   | 32   |
| I2C SDA  | 21   |
| I2C SCL  | 22   |

## Building from Source

For developers who want to modify the firmware:

```bash
./scripts/docker-build.sh           # Build using Docker
./scripts/docker-build.sh --rebuild # Force clean rebuild
```

Output: `output/m5tough-lvgl-firmware.bin`

### Project Structure

```
├── display_configs/
│   └── M5Stack-Tough.toml    # Hardware configuration (baked into firmware)
├── scripts/
│   ├── docker-build.sh       # Build script
│   └── docker-entrypoint.sh  # Container entrypoint
├── Dockerfile                # Build environment
└── output/                   # Build artifacts (gitignored)
```

## How It Works

The TOML configuration defines your hardware setup. The build system:

1. Reads `M5Stack-Tough.toml`
2. Generates a `display.py` module with initialization code
3. Freezes it into the MicroPython firmware
4. Compiles C-based display drivers (much faster than Python)

When you `import display` on the device, it auto-configures SPI, the display driver, and starts LVGL's render loop.

## License

MIT
