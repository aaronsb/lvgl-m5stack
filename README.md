# M5Stack Tough - LVGL MicroPython

Direct hardware control for M5Stack Tough with LVGL graphics - no UIFlow, no cloud accounts.

## Hardware

- **MCU**: ESP32-D0WDQ6-V3 with PSRAM
- **Display**: ILI9342C 320x240 (ILI9341 compatible)
- **Touch**: Capacitive @ I2C 0x2E
- **Power**: AXP192 @ I2C 0x34

## Quick Start

### Option 1: Download Pre-built Firmware

Check [Releases](../../releases) for pre-built firmware binaries.

```bash
pip install esptool
esptool.py --port /dev/ttyACM0 erase_flash
esptool.py --port /dev/ttyACM0 --baud 460800 write_flash 0x0 firmware.bin
```

### Option 2: Build from Source

```bash
./scripts/build.sh
```

### Option 3: Docker Build (recommended)

```bash
docker build -t m5tough-lvgl .
docker run --rm -v $(pwd)/output:/output m5tough-lvgl
# Firmware will be in ./output/
```

## Pure MicroPython (no LVGL)

For basic display/touch without the full LVGL stack:

```bash
# Flash generic MicroPython
esptool.py --port /dev/ttyACM0 erase_flash
esptool.py --port /dev/ttyACM0 --baud 460800 write_flash 0x1000 \
    https://micropython.org/resources/firmware/ESP32_GENERIC-20241129-v1.24.1.bin

# Upload drivers
mpremote connect /dev/ttyACM0 fs mkdir /lib
mpremote connect /dev/ttyACM0 fs cp src/*.py :/lib/

# Run demo
mpremote connect /dev/ttyACM0 run src/main.py
```

## Project Structure

```
├── display_configs/
│   └── M5Stack-Tough.toml    # LVGL display config
├── src/
│   ├── m5tough.py            # Display init helper
│   ├── touch.py              # Touch driver
│   └── main.py               # Demo app
├── scripts/
│   └── build.sh              # Local build script
├── Dockerfile                 # Container build
└── README.md
```

## Display Notes

The ILI9342C requires:
- `rotation=180`, `mirror=True`, `bgr=False`
- Send `INVON` (0x21) command after init for correct colors

## Pin Reference

| Function | GPIO |
|----------|------|
| SPI MOSI | 23 |
| SPI SCLK | 18 |
| LCD CS | 5 |
| LCD DC | 15 |
| LCD RST | 33 |
| LCD BL | 32 |
| I2C SDA | 21 |
| I2C SCL | 22 |

## License

MIT
