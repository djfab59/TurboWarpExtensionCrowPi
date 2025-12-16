import time
import datetime
import pygame
import threading
import random
import os
from gpiozero import OutputDevice
from elecrow_ws281x import *
from Adafruit_LED_Backpack import SevenSegment

pygame.init()
pygame.mixer.init()

segment = SevenSegment.SevenSegment(address=0x70)
heart = [1,6,8,9,10,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,41,42,43,44,45,46,50,51,52,53,59,60]

buzzer_pin = 18
shake_pin = 27


buzzer_sensor = OutputDevice(buzzer_pin)
shake_sensor = OutputDevice(shake_pin)


print("Press CTRL+C to exit")

now = datetime.datetime.now()
hour = now.hour
minute = now.minute
second = now.second

segment.clear()
segment.set_digit(0, int(hour / 10))    
segment.set_digit(1, hour % 10)         
segment.set_digit(2, int(minute / 10))  
segment.set_digit(3, minute % 10)        
segment.set_colon(2)
segment.write_display()
time.sleep(1)

class RGB_Matrix:

    def __init__(self):
        # Create NeoPixel object with appropriate configuration.
        self.strip = PixelStrip(64, 10)
        # Intialize the library (must be called once before other functions).
        self.strip.begin()

        self.RIGHT_BORDER = [7,15,23,31,39,47,55,63]
        self.LEFT_BORDER = [0,8,16,24,32,40,48,56]

    # Define functions which animate LEDs in various ways.
    def clean(self):
        # wipe all the LED's at once
        self.strip.clear()


    def wheel(self, pos):
        """Generate rainbow colors across 0-255 positions."""
        if pos < 85:
            return pos * 3, 255 - pos * 3, 0
        elif pos < 170:
            pos -= 85
            return 255 - pos * 3, 0, pos * 3
        else:
            pos -= 170
            return 0, pos * 3, 255 - pos * 3

    def rainbow(self, strip, wait_ms=10, iterations=1):
        """Draw rainbow that fades across all pixels at once."""
        list = [0] * (64*3)
        for j in range(256 * iterations):
            for i in range(strip.numPixels()):
                list[i*3+0], list[i*3+1], list[i*3+2] = self.wheel((i + j) & 255)
            strip.sendAllPixRGB(list)
            time.sleep(wait_ms / 1000.0)
    
    def theaterChase(self,strip, color, wait_ms=50, iterations=10):
        """Movie theater light style chaser animation."""
        for j in range(iterations):
            for q in range(3):
                for i in range(0, strip.numPixels(), 3):
                    strip.setPixelColor(i + q, color)
                strip.show()
                time.sleep(wait_ms / 1000.0)
                for i in range(0, strip.numPixels(), 3):
                    strip.setPixelColor(i + q, 0)
    

    def demo(self,strip):    
        self.theaterChase(strip, Color(127, 127, 127))  # White theater chase
        self.theaterChase(strip, Color(127, 0, 0))  # Red theater chase
        self.theaterChase(strip, Color(0, 0, 127))  # Blue theater chase
        
        self.rainbow(strip)

        self.clean()

    def run(self):
        # do stuff
        try:
            print('test animations.')
            for i in range(3):
                self.demo(self.strip)
            while True:
                self.strip.sendPos2Show(heart, 255, 0, 0)
        except KeyboardInterrupt:
             # clean the matrix LED before interruption
             self.clean()


def count_down(times):
    segment.clear()
    segment.set_digit(0, times)    
    segment.set_digit(1, times)         
    segment.set_digit(2, times)  
    segment.set_digit(3, times)        
    #segment.set_colon(second % 2)
    segment.write_display()
    buzzer_sensor.on()
    time.sleep(0.5)
    buzzer_sensor.off()
    time.sleep(0.5)

def cleanup():
    buzzer_sensor.close()
    shake_sensor.close()


def delay(times):
   time.sleep(times/500.0)

def colorWipe(strip, color, wait_ms=50):
    """Wipe color across display a pixel at a time."""
    strip.fillColor(color)

# Intialize the library (must be called once before other functions).
segment.begin()
matrix = RGB_Matrix()

try:
    while True:
        for i in range(4,-1,-1):
            count_down(i)
        break
    segment.clear()
    segment.write_display() 
    buzzer_sensor.on()
    shake_sensor.on()
    time.sleep(1)
    buzzer_sensor.off()
    shake_sensor.off()
    
    pygame.mixer.music.load('/usr/share/code/project/Happy_birthday/1.mp3')
    pygame.mixer.music.play()
    matrix.run()
    input()
 
except KeyboardInterrupt:
    matrix.clean()
    segment.clear()
    segment.write_display()
    pygame.mixer.music.stop() 
    os.system('killall -9 ffmpeg')
    buzzer_sensor.close()
    shake_sensor.close()


