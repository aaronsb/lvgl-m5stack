# M5Stack Tough LVGL Firmware Project

## Build System

**Always use the Docker build script for firmware builds:**

```bash
./scripts/docker-build.sh           # Normal build (uses Docker cache)
./scripts/docker-build.sh --rebuild # Force rebuild without cache
```

Do NOT invoke `docker build` directly.

## Key Files

- `display_configs/M5Stack-Tough.toml` - Display/touch configuration
- `scripts/docker-build.sh` - Build script
- `scripts/docker-entrypoint.sh` - Container entrypoint
- `Dockerfile` - Build environment
- `output/` - Build output (firmware .bin, logs)

## Hardware

M5Stack Tough ESP32 with ILI9342C display (320x240):
- SPI: host=2 (VSPI), MOSI=23, MISO=19, SCK=18
- LCD: CS=5, DC=15, RST=33, BL=32, 40MHz
- I2C: SDA=21, SCL=22
- Touch: I2C address 0x2E

## LVGL Display Configuration (Verified Working)

```python
import lvgl as lv
import machine
import lcd_bus
import ili9341

lv.init()

spi_bus = machine.SPI.Bus(host=2, mosi=23, miso=19, sck=18)
display_bus = lcd_bus.SPIBus(spi_bus=spi_bus, freq=40000000, dc=15, cs=5)

display = ili9341.ILI9341(
    data_bus=display_bus,
    display_width=320,
    display_height=240,
    backlight_pin=32,
    reset_pin=33,
    backlight_on_state=ili9341.STATE_HIGH,
    color_space=lv.COLOR_FORMAT.RGB565,
    color_byte_order=ili9341.BYTE_ORDER_BGR,
    rgb565_byte_swap=True
)

display._ORIENTATION_TABLE = [0, 96, 192, 160]
display.set_power(True)
display.init(1)  # rotation 1 = 90 degrees
display.set_backlight(100)

import task_handler
task_handler.TaskHandler()
```

## Flashing

```bash
source venv/bin/activate
esptool.py --port /dev/ttyACM0 --baud 460800 erase_flash
esptool.py --port /dev/ttyACM0 --baud 460800 write_flash 0x0 output/m5tough-lvgl-firmware.bin
```

## Device Communication

```bash
source venv/bin/activate
mpremote connect /dev/ttyACM0
```
