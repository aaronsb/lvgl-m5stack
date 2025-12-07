# M5Stack Tough Display Configuration
# Custom display.py with AXP192 power management and ILI9342C color fix

# First: Enable LCD power via AXP192
from machine import I2C, Pin as _Pin
_i2c = I2C(0, scl=_Pin(22), sda=_Pin(21), freq=400000)
_i2c.writeto_mem(0x34, 0x28, b'\xcc')  # TFT voltage 3.0V
_reg12 = _i2c.readfrom_mem(0x34, 0x12, 1)[0]
_i2c.writeto_mem(0x34, 0x12, bytes([_reg12 | 0x0C]))  # Enable LDO2/3
del _i2c, _Pin, _reg12

from micropython import const
import lvgl as lv

_SPI_BUS_HOST = const(2)
_SPI_BUS_MOSI = const(23)
_SPI_BUS_MISO = const(19)
_SPI_BUS_SCK = const(18)
_DISPLAY_BUS_FREQ = const(40000000)
_DISPLAY_BUS_DC = const(15)
_DISPLAY_BUS_CS = const(5)
_DISPLAY_WIDTH = const(320)
_DISPLAY_HEIGHT = const(240)
_DISPLAY_BACKLIGHT_PIN = const(32)
_DISPLAY_RESET_PIN = const(33)
_DISPLAY_RGB565_BYTE_SWAP = const(1)

import machine

spi_bus = machine.SPI.Bus(
    host=_SPI_BUS_HOST,
    mosi=_SPI_BUS_MOSI,
    miso=_SPI_BUS_MISO,
    sck=_SPI_BUS_SCK
)

import lcd_bus

display_bus = lcd_bus.SPIBus(
    spi_bus=spi_bus,
    freq=_DISPLAY_BUS_FREQ,
    dc=_DISPLAY_BUS_DC,
    cs=_DISPLAY_BUS_CS
)

import ili9341

display = ili9341.ILI9341(
    data_bus=display_bus,
    display_width=_DISPLAY_WIDTH,
    display_height=_DISPLAY_HEIGHT,
    backlight_pin=_DISPLAY_BACKLIGHT_PIN,
    reset_pin=_DISPLAY_RESET_PIN,
    backlight_on_state=ili9341.STATE_HIGH,
    color_space=lv.COLOR_FORMAT.RGB565,
    color_byte_order=ili9341.BYTE_ORDER_BGR,
    rgb565_byte_swap=_DISPLAY_RGB565_BYTE_SWAP
)

display._ORIENTATION_TABLE = [0, 96, 192, 160]
display.set_power(True)
display.init(1)

# ILI9342C requires INVON for correct colors
display_bus.tx_param(0x21, bytes())

display.set_backlight(100)

import task_handler

task_handler.TaskHandler()
