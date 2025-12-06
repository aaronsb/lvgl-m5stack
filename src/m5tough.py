"""M5Stack Tough display driver setup"""
from machine import Pin, SPI
from ili9341 import Display, color565

# Pin definitions for M5Stack Tough
PIN_SPI_MOSI = 23
PIN_SPI_SCLK = 18
PIN_LCD_CS = 5
PIN_LCD_DC = 15
PIN_LCD_RST = 33
PIN_LCD_BL = 32

def init_display():
    """Initialize the M5Stack Tough display.

    Returns configured Display object ready to use.
    """
    # Backlight on
    bl = Pin(PIN_LCD_BL, Pin.OUT)
    bl.value(1)

    # SPI bus
    spi = SPI(2, baudrate=40000000, sck=Pin(PIN_SPI_SCLK), mosi=Pin(PIN_SPI_MOSI))

    # Display - ILI9342C settings for M5Stack Tough
    display = Display(
        spi,
        dc=Pin(PIN_LCD_DC),
        cs=Pin(PIN_LCD_CS),
        rst=Pin(PIN_LCD_RST),
        width=320,
        height=240,
        rotation=180,
        mirror=True,
        bgr=False
    )

    # ILI9342C requires inversion enabled for correct colors
    display.write_cmd(0x21)  # INVON

    return display

# Re-export color565 for convenience
rgb = color565
