"""M5Stack Tough Demo - Display + Touch"""
from m5tough import init_display, rgb
from touch import Touch
import time

display = init_display()
touch = Touch()

# Colors
BG_COLOR = rgb(20, 20, 40)
SPRITE_COLOR = rgb(255, 100, 50)
SPRITE_OUTLINE = rgb(255, 255, 255)

# Screen dimensions
SCREEN_W = 320
SCREEN_H = 240

# Sprite size
SIZE = 24

# UI layout - reserve top area for header
HEADER_H = 90
TOUCH_AREA_Y = HEADER_H

def draw_header():
    """Draw the header with title and color bars"""
    # Title bar
    display.fill_rectangle(0, 0, SCREEN_W, 50, rgb(0, 80, 160))
    display.draw_text8x8(10, 10, "M5Stack Tough", rgb(255, 255, 255))
    display.draw_text8x8(10, 25, "MicroPython - No UIFlow!", rgb(200, 220, 255))
    display.draw_text8x8(10, 40, "Direct hardware control", rgb(150, 180, 220))

    # Color bars
    bar_w = 100
    bar_h = 30
    y = 55
    display.fill_rectangle(5, y, bar_w, bar_h, rgb(255, 0, 0))
    display.fill_rectangle(110, y, bar_w, bar_h, rgb(0, 255, 0))
    display.fill_rectangle(215, y, bar_w, bar_h, rgb(0, 0, 255))

def draw_touch_area():
    """Draw the touch interaction area"""
    display.fill_rectangle(0, TOUCH_AREA_Y, SCREEN_W, SCREEN_H - TOUCH_AREA_Y, BG_COLOR)
    display.draw_text8x8(10, TOUCH_AREA_Y + 10, "Touch below to move sprite", rgb(150, 150, 150))

def draw_sprite(x, y):
    """Draw crosshair sprite"""
    # Horizontal bar
    display.fill_rectangle(x - SIZE//2, y - 2, SIZE, 4, SPRITE_COLOR)
    # Vertical bar
    display.fill_rectangle(x - 2, y - SIZE//2, 4, SIZE, SPRITE_COLOR)
    # Center dot
    display.fill_rectangle(x - 3, y - 3, 6, 6, SPRITE_OUTLINE)

def erase_sprite(x, y):
    """Erase sprite completely"""
    # Erase a slightly larger area to catch any edges
    display.fill_rectangle(x - SIZE//2 - 2, y - SIZE//2 - 2, SIZE + 4, SIZE + 4, BG_COLOR)

def clamp_to_touch_area(x, y):
    """Clamp coordinates to valid touch area, return None if outside"""
    margin = SIZE // 2 + 2

    # Check if touch is in the touch area
    if y < TOUCH_AREA_Y + margin:
        return None

    # Clamp to bounds
    x = max(margin, min(SCREEN_W - margin, x))
    y = max(TOUCH_AREA_Y + margin, min(SCREEN_H - margin, y))

    return (x, y)

# Initial draw
display.fill_rectangle(0, 0, SCREEN_W, SCREEN_H, BG_COLOR)
draw_header()
draw_touch_area()

print("Touch demo running - touch the lower area!")
print("Ctrl+C to exit")

last_pos = None

try:
    while True:
        raw_pos = touch.read()

        if raw_pos is not None:
            pos = clamp_to_touch_area(*raw_pos)

            if pos is not None:
                x, y = pos

                # Always erase old position first if it exists and differs
                if last_pos is not None and last_pos != (x, y):
                    erase_sprite(*last_pos)

                # Draw at new position
                draw_sprite(x, y)
                last_pos = (x, y)
            else:
                # Touch is outside valid area - erase sprite
                if last_pos is not None:
                    erase_sprite(*last_pos)
                    last_pos = None

        else:
            # No touch - erase sprite if it exists
            if last_pos is not None:
                erase_sprite(*last_pos)
                last_pos = None

        time.sleep_ms(16)  # ~60fps

except KeyboardInterrupt:
    print("\nDone!")
