# M5Stack Tough Display Test
# Uses AXP192 for power management
# Based on working m5tough.py config: bgr=False, INVON required

from machine import I2C, Pin, SPI
import lvgl as lv
import lcd_bus
import ili9341

# AXP192 power management - enable LCD power
i2c = I2C(0, scl=Pin(22), sda=Pin(21), freq=400000)
i2c.writeto_mem(0x34, 0x28, b'\xcc')  # TFT voltage 3.0V
reg12 = i2c.readfrom_mem(0x34, 0x12, 1)[0]
i2c.writeto_mem(0x34, 0x12, bytes([reg12 | 0x0C]))  # Enable LDO2/3
print('AXP192 power enabled')

# Initialize LVGL
lv.init()

# Setup SPI and display
spi_bus = SPI.Bus(host=2, mosi=23, miso=19, sck=18)
display_bus = lcd_bus.SPIBus(spi_bus=spi_bus, dc=15, cs=5, freq=40000000)

# ILI9342C on M5Stack Tough uses RGB (not BGR) based on old working code
disp = ili9341.ILI9341(
    data_bus=display_bus,
    display_width=320,
    display_height=240,
    backlight_pin=32,
    reset_pin=33,
    backlight_on_state=ili9341.STATE_HIGH,
    color_space=lv.COLOR_FORMAT.RGB565,
    color_byte_order=ili9341.BYTE_ORDER_BGR,  # Try BGR with INVON
    rgb565_byte_swap=True
)

disp._ORIENTATION_TABLE = [0, 96, 192, 160]
disp.set_power(True)
disp.init(1)

# ILI9342C requires INVON (0x21) for correct colors - send via display bus
# Using empty bytes instead of None to avoid crash
display_bus.tx_param(0x21, bytes())
print('Sent INVON command')

# Create red screen with white text
scr = lv.screen_active()
scr.set_style_bg_color(lv.color_hex(0xFF0000), 0)

label = lv.label(scr)
label.set_text('M5STACK TOUGH')
label.set_style_text_color(lv.color_hex(0xFFFFFF), 0)
label.center()

import task_handler
th = task_handler.TaskHandler()

print('Display initialized - should be RED screen with white text')
