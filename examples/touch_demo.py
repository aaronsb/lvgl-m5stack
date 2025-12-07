# Touch Demo for M5Stack Tough
# Shows a red dot that follows your finger

import lvgl as lv
import lcd_bus
import ili9341
from machine import Pin, SPI, I2C
import time

# Initialize LVGL
lv.init()

# Display setup
bl = Pin(32, Pin.OUT)
bl.value(1)

spi_bus = SPI.Bus(host=2, mosi=23, miso=19, sck=18)
display_bus = lcd_bus.SPIBus(spi_bus=spi_bus, dc=15, cs=5, freq=40000000)

disp = ili9341.ILI9341(
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
disp._ORIENTATION_TABLE = [0, 96, 192, 160]
disp.set_power(True)
disp.init(1)
disp.set_backlight(100)

# Touch controller (CHSC6540 at 0x2E)
TOUCH_ADDR = 0x2E
i2c = I2C(0, scl=Pin(22), sda=Pin(21), freq=400000)

def read_touch():
    """Read touch position from CHSC6540"""
    data = i2c.readfrom_mem(TOUCH_ADDR, 0x02, 5)
    num_points = data[0] & 0x0F
    if num_points > 0:
        x = ((data[1] << 8) | data[2]) & 0x0FFF
        y = ((data[3] << 8) | data[4]) & 0x0FFF
        return (x, y)
    return None

# Create UI
scr = lv.screen_active()
scr.set_style_bg_color(lv.color_hex(0x1a1a2e), 0)

title = lv.label(scr)
title.set_text("Touch Demo")
title.set_style_text_color(lv.color_hex(0xFFFFFF), 0)
title.align(lv.ALIGN.TOP_MID, 0, 10)

label = lv.label(scr)
label.set_text("Touch the screen!")
label.set_style_text_color(lv.color_hex(0x00FF00), 0)
label.center()

# Touch indicator (red circle)
dot = lv.obj(scr)
dot.set_size(40, 40)
dot.set_style_radius(20, 0)
dot.set_style_bg_color(lv.color_hex(0xFF6B6B), 0)
dot.set_style_border_width(2, 0)
dot.set_style_border_color(lv.color_hex(0xFFFFFF), 0)
dot.add_flag(lv.obj.FLAG.HIDDEN)

print("Touch demo running!")

# Main loop
while True:
    touch = read_touch()

    if touch:
        x, y = touch
        label.set_text(f"X:{x} Y:{y}")
        dot.remove_flag(lv.obj.FLAG.HIDDEN)
        dot.set_pos(x - 20, y - 20)
    else:
        dot.add_flag(lv.obj.FLAG.HIDDEN)

    lv.task_handler()
    time.sleep(0.05)
