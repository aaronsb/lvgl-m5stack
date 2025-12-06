"""Touch Controller driver for M5Stack Tough"""
from machine import I2C, Pin
import time

class Touch:
    """Touch controller for M5Stack Tough (address 0x2E)"""

    ADDR = 0x2E

    def __init__(self, i2c=None, sda=21, scl=22):
        if i2c is None:
            self.i2c = I2C(0, sda=Pin(sda), scl=Pin(scl), freq=100000)
        else:
            self.i2c = i2c

        # Verify device is present
        devices = self.i2c.scan()
        if self.ADDR not in devices:
            raise RuntimeError(f"Touch not found at 0x{self.ADDR:02x}. Found: {[hex(d) for d in devices]}")

    def read(self):
        """Read touch state.

        Returns (x, y) tuple if touched, None if not touched.
        """
        # Send read command and get 8 bytes
        self.i2c.writeto(self.ADDR, bytes([0]))
        time.sleep_ms(5)
        data = self.i2c.readfrom(self.ADDR, 8)

        # Byte 2 = touch count
        num_points = data[2]

        if num_points == 0:
            return None

        # Extract X and Y (12-bit values)
        # Format: high nibble of byte 3/5 may be event type, low nibble is coord high bits
        x = ((data[3] & 0x0F) << 8) | data[4]
        y = ((data[5] & 0x0F) << 8) | data[6]

        return (x, y)

    def touched(self):
        """Return True if screen is being touched."""
        return self.read() is not None
