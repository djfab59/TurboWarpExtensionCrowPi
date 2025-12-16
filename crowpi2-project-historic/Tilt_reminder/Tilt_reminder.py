# # import RPi.GPIO as GPIO
# from gpiozero import InputDevice
# import time
# from rpi_ws281x import PixelStrip, Color

# # LED strip configuration:
# LED_COUNT = 64        # Number of LED pixels.
# LED_PIN = 12          # GPIO pin connected to the pixels (18 uses $
# LED_FREQ_HZ = 800000  # LED signal frequency in hertz (usually 800$
# LED_DMA = 10          # DMA channel to use for generating signal ($
# LED_BRIGHTNESS = 10  # Set to 0 for darkest and 255 for brightest
# LED_INVERT = False    # True to invert the signal (when using NPN $
# LED_CHANNEL = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53

# tilt_pin = 22
# # define sound pin

# # set GPIO mode to GPIO.BOARD
# # GPIO.setmode(GPIO.BCM)
# # setup pin as INPUT
# # GPIO.setup(tilt_pin, GPIO.IN)
# tilt_sensor = InputDevice(tilt_pin)

# def colorWipe(strip, color, wait_ms=50):
#     """Wipe color across display a pixel at a time."""
#     for i in range(strip.numPixels()):
#         strip.setPixelColor(i, color)
#         strip.show()
#         time.sleep(wait_ms / 1000.0)

# strip = PixelStrip(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
# # Intialize the library (must be called once before other functions).
# strip.begin()
    
# sprite_number_left = [24,17,10,3,33,42,51,25,26,27,28,29,30]
# sprite_number_right = [31,22,13,4,38,45,52,30,29,28,27,26,25]
# sprite_number_del_left = [3,10,17,24,33,42,51]
# sprite_number_del_right = [4,13,22,31,38,45,52]

# colorWipe(strip,Color(0,0,0),10)
# try:
#     while True:
#         # if(GPIO.input(tilt_pin) == True):
#         if(tilt_sensor.value == True):
#             for i in sprite_number_del_right:
#                 strip.setPixelColor(i,Color(0,0,0))
#             for i in sprite_number_left:   
#                 strip.setPixelColor(i,Color(255,0,0))
#             strip.show()
#         else:
#             for i in sprite_number_del_left:
#                 strip.setPixelColor(i,Color(0,0,0))
#             for i in sprite_number_right:   
#                 strip.setPixelColor(i,Color(0,255,0))
#             strip.show()        
# except KeyboardInterrupt:
#     colorWipe(strip,Color(0,0,0),10)
#     # GPIO.cleanup()
#     tilt_sensor.close()



from gpiozero import InputDevice
import time
from elecrow_ws281x import *

tilt_pin = 22
tilt_sensor = InputDevice(tilt_pin)

rp = PixelStrip(64, 10)
rp.begin()

def colorWipe(strip, r, g, b, wait_ms=50):
    """Wipe color across display a pixel at a time."""
    for i in range(strip.numPixels()):
        strip.setPixelColorRGB(i, r, g, b)
        strip.show()
        # time.sleep(wait_ms / 1000.0)

    
sprite_number_left = [24,17,10,3,33,42,51,25,26,27,28,29,30]
sprite_number_right = [31,22,13,4,38,45,52,30,29,28,27,26,25]
sprite_number_del_left = [3,10,17,24,33,42,51]
sprite_number_del_right = [4,13,22,31,38,45,52]

colorWipe(rp,0,0,0,0)

try:
    while True:
        if(tilt_sensor.value == True):
            for i in sprite_number_del_right:
                rp.setPixelColorRGB(i,0,0,0)
            for i in sprite_number_left:
                rp.setPixelColorRGB(i,255,0,0)
            rp.show()
        else:
            for i in sprite_number_del_left:
                rp.setPixelColorRGB(i,0,0,0)
            for i in sprite_number_right:
                rp.setPixelColorRGB(i,0,255,0)
            rp.show()        
except KeyboardInterrupt:
    colorWipe(rp,0,0,0,0)
    rp.clear()
    tilt_sensor.close()