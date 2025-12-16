import time
from elecrow_ws281x import *


RIGHT_BORDER = [7,15,23,31,39,47,55,63]
LEFT_BORDER = [0,8,16,24,32,40,48,56]

# Define functions which animate LEDs in various ways.
def colorWipe(strip, color, wait_ms=50):
    """Wipe color across display a pixel at a time."""
    strip.fillColor(color)
    time.sleep(wait_ms / 1000.0)

def theaterChase(strip, color, wait_ms=50, iterations=10):
    """Movie theater light style chaser animation."""
    for j in range(iterations):
        for q in range(3):
            for i in range(0, strip.numPixels(), 3):
                strip.setPixelColor(i + q, color)
            strip.show()
            time.sleep(wait_ms / 1000.0)
            for i in range(0, strip.numPixels(), 3):
                strip.setPixelColor(i + q, 0)

def wheel(pos):
    """Generate rainbow colors across 0-255 positions."""
    if pos < 85:
        return pos * 3, 255 - pos * 3, 0
    elif pos < 170:
        pos -= 85
        return 255 - pos * 3, 0, pos * 3
    else:
        pos -= 170
        return 0, pos * 3, 255 - pos * 3

def rainbow(strip, wait_ms=10, iterations=1):
    """Draw rainbow that fades across all pixels at once."""
    list = [0] * (64*3)
    for j in range(256 * iterations):
        for i in range(strip.numPixels()):
            list[i*3+0], list[i*3+1], list[i*3+2] = wheel((i + j) & 255)
        strip.sendAllPixRGB(list)
        time.sleep(wait_ms / 1000.0)

# Create NeoPixel object with appropriate configuration.
strip = PixelStrip(64, 10)
# Intialize the library (must be called once before other functions).
strip.begin()
# start animation
'''
print('Color wipe animations.')
colorWipe(strip, Color(255, 0, 0))  # Red wipe
colorWipe(strip, Color(0, 255, 0))  # Blue wipe
colorWipe(strip, Color(0, 0, 255))  # Green wipe
'''
# print('Theater chase animations.')
run_time = 0
while run_time<2:
    theaterChase(strip, Color(127, 127, 127))  # White theater chase
    theaterChase(strip, Color(127, 0, 0))  # Red theater chase
    theaterChase(strip, Color(0, 0, 127))  # Blue theater chase
# print('Rainbow animations.')
    rainbow(strip)
    run_time += 1
# print('Wipe LEDs')
    colorWipe(strip, Color(0, 0, 0), 10)
