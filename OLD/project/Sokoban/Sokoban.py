import time
import spidev
# import RPi.GPIO as GPIO
from gpiozero import InputDevice
import spidev
import os
import operator
from elecrow_ws281x import *

x_channel = 1
y_channel = 0

delay = 0.1

touch_pin = 17
touch_sensor = InputDevice(touch_pin)
 
# Open SPI bus
spi = spidev.SpiDev()
spi.open(0,1)
spi.max_speed_hz=1000000


# Open SPI bus
spi = spidev.SpiDev()
spi.open(0,1)
spi.max_speed_hz=1000000

# Function to read SPI data from MCP3008 chip
# Channel must be an integer 0-7
def ReadChannel(channel):
  adc = spi.xfer2([1,(8+channel)<<4,0])
  data = ((adc[1]&3) << 8) + adc[2]
  return data

# Define functions which animate LEDs in various ways.
def colorWipe(strip, color, wait_ms=50):
    """Wipe color across display a pixel at a time."""
    strip.fillColor(color)
    

def sprite(red_locat,green_locat,blue_locat):
    global sprite_number
    sprite_number_up = [0,1,2,3,4,5,6,7]
    sprite_number_down = [56,57,58,59,60,61,62,63]
    sprite_number_left = [0,8,16,24,32,40,48,56]
    sprite_number_right = [7,15,23,31,39,47,55,63]


# Read the  data
    x_value = ReadChannel(x_channel)
    y_value = ReadChannel(y_channel)
    if x_value > 650:
        print("Left")
        sprite_number = sprite_number - 1
        if (sprite_number + 1) in sprite_number_left:
            sprite_number = sprite_number + 1
        if sprite_number in red_locat:
            sprite_number = sprite_number + 1

        if sprite_number in green_locat:
            if (sprite_number - 1) in red_locat or (sprite_number - 1) in green_locat:
                sprite_number = sprite_number + 1
            elif sprite_number in sprite_number_left:
                sprite_number = sprite_number + 1
            else:
                green_locat.remove(sprite_number)
                green_locat.append((sprite_number - 1))
                
    if x_value < 400:
        print("Right")
        sprite_number = sprite_number + 1
        if (sprite_number - 1) in sprite_number_right:
            sprite_number = sprite_number - 1
        if sprite_number in red_locat:
            sprite_number = sprite_number - 1 
        if sprite_number in green_locat:
            if (sprite_number + 1) in red_locat or (sprite_number + 1) in green_locat:
                sprite_number = sprite_number - 1
            elif sprite_number in sprite_number_right:
                sprite_number = sprite_number - 1
            else:
                green_locat.remove(sprite_number)
                green_locat.append((sprite_number + 1))
                
    show(blue_locat,0,0,255)
    show(green_locat,0,255,0)
    show(red_locat,255,0,0)

    strip.setPixelColor(sprite_number,Color(255,255,255))
    strip.show()

    time.sleep(0.05)
    strip.setPixelColor(sprite_number,Color(0,0,0))
    time.sleep(0.05)
                
                
                
    if y_value > 650:
        print("Up")
        sprite_number = sprite_number - 8
        if (sprite_number + 8) in sprite_number_up:
            sprite_number = sprite_number + 8
        if sprite_number in red_locat:
            sprite_number = sprite_number + 8
            
        if sprite_number in green_locat:
            if (sprite_number - 8) in red_locat or (sprite_number - 8) in green_locat:
                sprite_number = sprite_number + 8
            elif sprite_number in sprite_number_up:
                sprite_number = sprite_number + 8
            else:
                green_locat.remove(sprite_number)
                green_locat.append((sprite_number - 8))
    
    if y_value < 400:
        print("Down")
        sprite_number = sprite_number + 8
        if (sprite_number - 8) in sprite_number_down:
            sprite_number = sprite_number - 8
        if sprite_number in red_locat:
            sprite_number = sprite_number - 8
            
        if sprite_number in green_locat:
            if (sprite_number + 8) in red_locat or (sprite_number + 8) in green_locat:
                sprite_number = sprite_number - 8
            elif sprite_number in sprite_number_down:
                sprite_number = sprite_number - 8
            else:
                green_locat.remove(sprite_number)
                green_locat.append((sprite_number + 8))

    show(blue_locat,0,0,255)
    show(green_locat,0,255,0)
    show(red_locat,255,0,0)

    strip.setPixelColor(sprite_number,Color(255,255,255))
    strip.show()

    time.sleep(0.05)
    strip.setPixelColor(sprite_number,Color(0,0,0))
    strip.show()
    time.sleep(0.05)
    
def show(show_what,red,green,blue):
    strip.sendPos2Show(show_what, red, green, blue)


def customs_pass(customs):
    strip.sendPos2Show(customs, 0, 255, 255)
    time.sleep(2)
    strip.fill()
    
def map_pass1():
    strip.fill()
    global sprite_number_blue_1
    global sprite_number_red_1
    global sprite_number_green_1
    global sprite_number

    sprite_number_red_1 = [16,17,18,19,25,31,38,44,46,57]
    sprite_number_blue_1 = [1,7,37]
    sprite_number_green_1 = [12,33,50]
    sprite_number = 0

def map_pass2():
    colorWipe(strip,Color(0,0,0),1)
    global sprite_number_blue_2
    global sprite_number_red_2
    global sprite_number_green_2
    global sprite_number
    sprite_number_blue_2 = [1,29,45]
    sprite_number_red_2 = [16,17,18,19,20,38,44,46,61]
    sprite_number_green_2 = [12,33,53]
    sprite_number = 1

def map_pass3():
    colorWipe(strip,Color(0,0,0),1)
    global sprite_number_blue_3
    global sprite_number_red_3
    global sprite_number_green_3
    global sprite_number
    sprite_number_blue_3 = [36,44,52]
    sprite_number_red_3 = [10,11,12,13,14,22,23,31,39,47,55,54,62,61,60,59,58,50,49,41,33,25,17,18,28]
    sprite_number_green_3 = [35,36,37]
    sprite_number = 19

def box_right():
    for i in right_smiley:
        strip.setPixelColor(i,Color(0,255,0))
    strip.show()
    

strip = PixelStrip(64, 10)
strip.begin()

right_smiley = [40,49,58,51,44,37,30,23]
worry_smiley = [9,18,27,36,45,54,14,21,28,35,42,49]


customs_1 = [18,11,4,12,20,28,36,44,52,57,58,59,60,61,62,63]
customs_2 = [2,3,4,5,13,21,29,37,36,35,34,42,50,58,59,60,61]
customs_3 = [10,11,12,13,21,29,34,35,36,37,45,53,58,59,60,61]

colorWipe(strip,Color(0,0,0),1)



try:
    colorWipe(strip,Color(0,0,0),1)
    customs_pass(customs_1)
    while True:
        map_pass1()
        while (touch_sensor.value) == 0:
            sprite(sprite_number_red_1,sprite_number_green_1,sprite_number_blue_1)
            sprite_number_blue_1.sort(reverse=True)
            sprite_number_green_1.sort(reverse=True)
            if operator.eq(sprite_number_green_1,sprite_number_blue_1) == 1:
                time.sleep(1)
                colorWipe(strip,Color(0,0,0),1)
                customs_pass(customs_2)
                while True:
                    map_pass2()
                    while (touch_sensor.value) == 0:
                        sprite(sprite_number_red_2,sprite_number_green_2,sprite_number_blue_2)
                        sprite_number_blue_2.sort(reverse=True)
                        sprite_number_green_2.sort(reverse=True)
                        if operator.eq(sprite_number_green_2,sprite_number_blue_2) == 1:
                            time.sleep(1)
                            colorWipe(strip,Color(0,0,0),1)
                            customs_pass(customs_3)
                            while True:
                                map_pass3()
                                while (touch_sensor.value) == 0:
                                    sprite(sprite_number_red_3,sprite_number_green_3,sprite_number_blue_3)
                                    sprite_number_blue_3.sort(reverse=True)
                                    sprite_number_green_3.sort(reverse=True)
                                    if operator.eq(sprite_number_green_3,sprite_number_blue_3) == 1:
                                        time.sleep(1)
                                        colorWipe(strip,Color(0,0,0),1)
                                        while True:
                                            box_right()


except KeyboardInterrupt:
    colorWipe(strip,Color(0,0,0),1)
    touch_sensor.close()
    

                         
