"""Simple demo using M5Stack Tough"""
from m5tough import init_display, rgb

display = init_display()

# Clear screen
display.fill_rectangle(0, 0, 320, 240, rgb(0, 0, 0))

# Draw some stuff
display.fill_rectangle(20, 20, 280, 60, rgb(0, 100, 200))
display.draw_text8x8(30, 40, "M5Stack Tough", rgb(255, 255, 255))
display.draw_text8x8(30, 55, "MicroPython - No UIFlow!", rgb(200, 200, 200))

# Color bars
display.fill_rectangle(20, 100, 80, 40, rgb(255, 0, 0))
display.fill_rectangle(120, 100, 80, 40, rgb(0, 255, 0))
display.fill_rectangle(220, 100, 80, 40, rgb(0, 0, 255))

display.draw_text8x8(20, 160, "Direct hardware access", rgb(255, 255, 0))
display.draw_text8x8(20, 180, "No accounts needed", rgb(0, 255, 255))

print("Demo running!")
