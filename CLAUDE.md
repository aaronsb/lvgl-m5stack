# Development Notes

## Build Commands

```bash
./scripts/docker-build.sh           # Build with Docker cache
./scripts/docker-build.sh --rebuild # Clean rebuild
```

Do NOT invoke `docker build` directly.

## Key Insight: TOML → display.py → Firmware

The TOML config generates `display.py` which gets frozen into firmware. Changes to TOML require rebuilding firmware.

## Verified Working Display Config

```python
# This is what the TOML generates and what works:
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
display.init(1)  # rotation 1 = 90 degrees
```

## Debugging Tips

- Generated display.py is copied to `output/generated-display.py` for inspection
- Build logs saved to `output/build-*.log`
- I2C section in TOML caused crashes - keep it commented out until touch is needed
