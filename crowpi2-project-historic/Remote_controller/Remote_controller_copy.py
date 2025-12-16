#!/usr/bin/python
# -*- coding:utf-8 -*-
import time
# import RPi.GPIO as GPIO
from elecrow_ws281x import *
from gpiozero import OutputDevice, InputDevice
import datetime
import pygame
import threading
import random
from Adafruit_LED_Backpack import SevenSegment
import Adafruit_DHT
import HD44780MCP
import MCP230XX
# import alsaaudio
import smbus
import adafruit_dht

# LED strip configuration:
LED_COUNT = 64        # Number of LED pixels.
LED_PIN = 12          # GPIO ir_pin connected to the pixels (18 uses $
LED_FREQ_HZ = 800000  # LED signal frequency in hertz (usually 800$
LED_DMA = 10          # DMA channel to use for generating signal ($
LED_BRIGHTNESS = 10  # Set to 0 for darkest and 255 for brightest
LED_INVERT = False    # True to invert the signal (when using NPN $
LED_CHANNEL = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53

DHT_PIN = 4

pygame.mixer.init()
# GPIO.setwarnings(False)
# GPIO.setmode(GPIO.BCM)

# segment = SevenSegment.SevenSegment(address=0x70)

ir_pin = 20
buzzer_pin = 18
shake_pin = 27

class LCDModule():

    def __init__(self):
        # Define LCD column and row size for 16x2 LCD.
        self.address    = 0x21
        self.lcd_cols   = 16
        self.lcd_rows   = 2
        self.bl_pin     = 7
        # Initialize the LCD using the pins
        self.mcp = MCP230XX.MCP230XX('MCP23008', self.address)
        self.lcd = HD44780MCP.HD44780(self.mcp, 1, -1, 2, dbList = [3, 4, 5, 6], rows = self.lcd_rows, characters = self.lcd_cols, mode = 0, font = 0)
        self.mcp.set_mode(self.bl_pin, 'output')

    def turn_off(self):
        # Turn backlight off
        self.lcd.set_display()
        self.mcp.output(self.bl_pin, 0)

    def turn_on(self):
        # Turn backlight on
        self.mcp.output(self.bl_pin, 1)
        self.lcd.set_display(on = 1, cursor = 1)

    def clear(self):
        # clear the LCD screen
        self.lcd.clear_display()

    def write_lcd(self,text):
        self.turn_on()
        self.lcd.display_string(text)

# define LCD module
lcd_screen = LCDModule()
instance = adafruit_dht.DHT11(DHT_PIN)


# m = alsaaudio.Mixer()
# vol = int(m.getvolume()[0])

# set type of the sensor
sensor = 11
# set pin number

six_RGB_1 = [27,35,28,36]
six_RGB_2 = [18,19,20,21,29,37,45,44,43,42,34,26]
six_RGB_3 = [9,10,11,12,13,14,22,30,38,46,54,53,52,51,50,49,41,33,25,17]
six_RGB_4 = [0,1,2,3,4,5,6,7,15,23,31,39,47,55,63,62,61,60,59,58,57,56,48,40,32,24,16,8]

CH_sub_number = 0
CH_number = 0
CH_add_number = 0
left_number = 0
right_number = 0
play_number = 0
vol_sub_number = 0
vol_add_number = 0
EQ_number = 0
Zero_number = 0
one_hundred_number = 0
two_hundred_number = 0
number_name = 1
nine_number = 0
four_number = 0
five = 0
six = 0
music_go = 0

# GPIO.setup(ir_pin,GPIO.IN,GPIO.PUD_UP)
# GPIO.setup(buzzer_pin, GPIO.OUT)
# GPIO.setup(shake_pin, GPIO.OUT)

ir_sensor       = InputDevice(ir_pin)
buzzer_sensor   = OutputDevice(buzzer_pin)
shake_sensor    = OutputDevice(shake_pin)

print("irm test start...")

humidity = 0
temperature = 0

def get_DHT20():

    lcd_screen.lcd.cursor(cursor = False)
    if instance.temperature is not None and instance.humidity is not None:
        lcd_screen.write_lcd(text=('Temp = {0:0.2f}*c \nHumd = {1:0.2f}%\n'.format(instance.temperature, instance.humidity)))
    else:
        lcd_screen.write_lcd(text=('GET DHT DATA ERROR!'))
        print('GET DHT DATA ERROR!')

    print("Temperature: %-3.1f C" % instance.temperature)
    print("Humidity: %-3.1f C" % instance.humidity)
    time.sleep(1)


def colorWipe(strip, color, wait_ms=50):
    """Wipe color across display a pixel at a time."""
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, color)
        strip.show()
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
        return Color(pos * 3, 255 - pos * 3, 0)
    elif pos < 170:
        pos -= 85
        return Color(255 - pos * 3, 0, pos * 3)
    else:
        pos -= 170
        return Color(0, pos * 3, 255 - pos * 3)


def rainbow(strip, wait_ms=10, iterations=1):
    """Draw rainbow that fades across all pixels at once."""
    for j in range(256 * iterations):
        for i in range(strip.numPixels()):
            strip.setPixelColor(i, wheel((i + j) & 255))
        strip.show()
        time.sleep(wait_ms / 1000.0)

def all_RGB(R,G,B,a):
    for i in range(64):
        strip.setPixelColor(i,Color(R,G,B))
    strip.show()
    time.sleep(a)

def rgb_in(rgb,s,R,G,B):
    for i in rgb :
        strip.setPixelColor(i,Color(R,G,B))
    strip.show()
    time.sleep(s)

    
def one_list(a,b,c):
    one_list = [a]
    for i in range(b):
        one_list.append(one_list[i]+(c))
    rgb_in(one_list,0.1,random.randint(50,255),random.randint(50,255),random.randint(50,255))
    
def one_list_close(a,b,c):
    one_list = [a]
    for i in range(b):
        one_list.append(one_list[i]+(c))
    rgb_in(one_list,0.1,0,0,0)
    
def one():
    for i in range(1):
        for i in range(15):
            all_RGB(random.randint(0,255),random.randint(0,255),random.randint(0,255),0.1)
        all_RGB(0,0,0,0)
        
        for i in range(3):
            one_list(56,0,9)
            one_list(48,1,9)
            one_list(40,2,9)
            one_list(32,3,9)
            one_list(24,4,9)
            one_list(16,5,9)
            one_list(8,6,9)
            one_list(0,7,9)
            one_list(1,6,9)
            one_list(2,5,9)
            one_list(3,4,9)
            one_list(4,3,9)
            one_list(5,2,9)
            one_list(6,1,9)
            one_list(7,0,9)
            
            one_list_close(7,0,9)
            one_list_close(6,1,9)        
            one_list_close(5,2,9)
            one_list_close(4,3,9)
            one_list_close(3,4,9)
            one_list_close(2,5,9)
            one_list_close(1,6,9)
            one_list_close(0,7,9)
            one_list_close(8,6,9)
            one_list_close(16,5,9)
            one_list_close(24,4,9)
            one_list_close(32,3,9)
            one_list_close(40,2,9)
            one_list_close(48,1,9)
            one_list_close(56,0,9)


def all_RGB_run(number):
    a = [0,1,2,3,8,9,10,11,16,17,18,19,24,25,26]
    b = [4,5,6,7,12,13,14,15,20,21,22,23,29,30,31]
    c = [32,33,34,40,41,42,43,48,49,50,51,56,57,58,59]
    d = [37,38,39,44,45,46,47,52,53,54,55,60,61,62,63]
    e = [27,28,35,36]
    
    for i in range(number):
        mod_RGB_no_show(a)
        mod_RGB_no_show(b)
        mod_RGB_no_show(c)
        mod_RGB_no_show(d)
        mod_RGB_no_show(e)
        strip.show()
        time.sleep(0.1)
    all_RGB(0,0,0,0)
    
        
def mod_RGB(a,R,G,B,aa):
    global six
    for i in a:
        strip.setPixelColor(i,Color(R,G,B))
    strip.show()
    time.sleep(aa)

def mod_RGB_no_show(a):
    a_1 = random.randint(50,180)
    a_2 = random.randint(50,180)
    a_3 = random.randint(50,180)
    for i in a:
        strip.setPixelColor(i,Color(a_1,a_2,a_3))
        
def one_hundred(number):
    a = [0,1,8,9,2,3,10,11,4,5,12,13,6,7,14,15,16,17,24,25,22,23,30,31,32,33,40,41,38,39,46,47,48,49,56,57,50,51,58,59,52,53,60,61,54,55,62,63]
    e = [18,19,20,21,26,27,28,29,34,35,36,37,42,43,44,45]
    for i in range(number):
        mod_RGB_no_show(e)
        for i in range(5):
            mod_RGB_no_show(a)
            time.sleep(0.05)
            strip.show()
        mod_RGB_no_show(e)
        strip.show()
    all_RGB(0,0,0,0)

def tree(number):
    for i in range(number):
        a = [35,27,28,36]
        b = [44,43,42,34,26,18,19,20,21,29,37,45]
        c = [53,52,51,50,49,41,33,25,17,9,10,11,12,13,14,22,30,38,46,54]
        d = [62,61,60,59,58,57,56,48,40,32,24,16,8,0,1,2,3,4,5,6,7,15,23,31,39,47,55,63]
        a1 = random.randint(50,255)
        a2 = random.randint(50,255)
        a3 = random.randint(50,255)
        for i in a:
            strip.setPixelColor(i,Color(a1,a2,a3))
            strip.show()
        time.sleep(0.01)

        a1 = random.randint(50,255)
        a2 = random.randint(50,255)
        a3 = random.randint(50,255)
        for i in b:
            strip.setPixelColor(i,Color(a1,a2,a3))
            strip.show()
        time.sleep(0.01)

        a1 = random.randint(50,255)
        a2 = random.randint(50,255)
        a3 = random.randint(50,255)
        for i in c:
            strip.setPixelColor(i,Color(a1,a2,a3))
            strip.show()
            time.sleep(0.01)

        a1 = random.randint(50,255)
        a2 = random.randint(50,255)
        a3 = random.randint(50,255)
        for i in d:
            strip.setPixelColor(i,Color(a1,a2,a3))
            strip.show()
            time.sleep(0.01)
        
        all_RGB(0,0,0,0)
        
        
def two_hundred(number):
    for i in range(1):    
        a = [0,1,8,9]
        a1 = [2,3,10,11]
        a2 = [4,5,12,13]
        a3 = [6,7,14,15]
        b = [16,17,24,25]
        b1 = [22,23,30,31]
        c = [32,33,40,41]
        c1 = [38,39,46,47]
        d = [48,49,56,57]
        d1 = [50,51,58,59]
        d2 = [52,53,60,61]
        d3 = [54,55,62,63]
        e = [18,19,20,21,26,27,28,29,34,35,36,37,42,43,44,45]
        for i in range(number):
            tree_run(a)
            tree_run(a1)
            tree_run(a2)
            tree_run(a3)
            
            
            tree_run(b1)
            tree_run(c1)
            tree_run(d3)
            
            
            tree_run(d2)
            tree_run(d1)
            tree_run(d)
            
            
            tree_run(c)
            tree_run(b)
            
            
            mod_RGB_no_show(e)
            strip.show()
          


     
def tree_run(a):
    mod_RGB_no_show(a)
    strip.show()
    time.sleep(0.01)
    mod_RGB(a,0,0,0,0.005)
    

    
def mod_RGB_run(number):
    for i in range(number):
        mod_RGB(six_RGB_1,random.randint(0,255),random.randint(0,255),random.randint(0,255),0.1)
        mod_RGB(six_RGB_2,random.randint(0,255),random.randint(0,255),random.randint(0,255),0.1)
        mod_RGB(six_RGB_3,random.randint(0,255),random.randint(0,255),random.randint(0,255),0.1)
        mod_RGB(six_RGB_4,random.randint(0,255),random.randint(0,255),random.randint(0,255),0.1)
        mod_RGB(six_RGB_4,0,0,0,0.1)
        mod_RGB(six_RGB_3,0,0,0,0.1)
        mod_RGB(six_RGB_2,0,0,0,0.1)
        mod_RGB(six_RGB_1,0,0,0,0.1)
    all_RGB(0,0,0,0)
    
def music_RGB_list(a,line,line_list):
    while line <= a:
        line_list.append(line)
        line = line + 8
    line_list.sort(reverse=True)

def music_RGB_row(i,row,line_1,line_2,line_3,line_4,line_5,line_6,line_7,line_8):
    if len(line_1)-1 >= i:
        row.append(line_1[i])
    if len(line_2)-1 >= i:
        row.append(line_2[i])
    if len(line_3)-1 >= i:
        row.append(line_3[i])
    if len(line_4)-1 >= i:
        row.append(line_4[i])
    if len(line_5)-1 >= i:
        row.append(line_5[i])
    if len(line_6)-1 >= i:
        row.append(line_6[i])
    if len(line_7)-1 >= i:
        row.append(line_7[i])
    if len(line_8)-1 >= i:
        row.append(line_8[i])



def music_RGB():
    
    global line_list_1
    global line_list_2
    global line_list_3
    global line_list_4
    global line_list_5
    global line_list_6
    global line_list_7
    global line_list_8
    
    global one_color_1
    global one_color_2
    global one_color_3
    
    global two_color_1
    global two_color_2
    global two_color_3
    
    global three_color_1
    global three_color_2
    global three_color_3
    
    global four_color_1
    global four_color_2
    global four_color_3
    
    global five_color_1
    global five_color_2
    global five_color_3
    
    global six_color_1
    global six_color_2
    global six_color_3
    
    global seven_color_1
    global seven_color_2
    global seven_color_3
    
    global eight_color_1
    global eight_color_2
    global eight_color_3    
    
    line_1 = random.randrange(0,64,8)
    line_2 = random.randrange(1,65,8)
    line_3 = random.randrange(2,66,8)
    line_4 = random.randrange(3,67,8)
    line_5 = random.randrange(4,68,8)
    line_6 = random.randrange(5,69,8)
    line_7 = random.randrange(6,70,8)
    line_8 = random.randrange(7,71,8)
    line_list_1 = []
    line_list_2 = []
    line_list_3 = []
    line_list_4 = []
    line_list_5 = []
    line_list_6 = []
    line_list_7 = []
    line_list_8 = []
    music_RGB_list(56,line_1,line_list_1)
    music_RGB_list(57,line_2,line_list_2)
    music_RGB_list(58,line_3,line_list_3)
    music_RGB_list(59,line_4,line_list_4)
    music_RGB_list(60,line_5,line_list_5)
    music_RGB_list(61,line_6,line_list_6)
    music_RGB_list(62,line_7,line_list_7)
    music_RGB_list(63,line_8,line_list_8)

    row_list_1 = []
    row_list_2 = []
    row_list_3 = []
    row_list_4 = []
    row_list_5 = []
    row_list_6 = []
    row_list_7 = []
    row_list_8 = []
    
    music_RGB_row(0,row_list_1,line_list_1,line_list_2,line_list_3,line_list_4,line_list_5,line_list_6,line_list_7,line_list_8)
    music_RGB_row(1,row_list_2,line_list_1,line_list_2,line_list_3,line_list_4,line_list_5,line_list_6,line_list_7,line_list_8)
    music_RGB_row(2,row_list_3,line_list_1,line_list_2,line_list_3,line_list_4,line_list_5,line_list_6,line_list_7,line_list_8)
    music_RGB_row(3,row_list_4,line_list_1,line_list_2,line_list_3,line_list_4,line_list_5,line_list_6,line_list_7,line_list_8)
    music_RGB_row(4,row_list_5,line_list_1,line_list_2,line_list_3,line_list_4,line_list_5,line_list_6,line_list_7,line_list_8)         
    music_RGB_row(5,row_list_6,line_list_1,line_list_2,line_list_3,line_list_4,line_list_5,line_list_6,line_list_7,line_list_8)          
    music_RGB_row(6,row_list_7,line_list_1,line_list_2,line_list_3,line_list_4,line_list_5,line_list_6,line_list_7,line_list_8)
    music_RGB_row(7,row_list_8,line_list_1,line_list_2,line_list_3,line_list_4,line_list_5,line_list_6,line_list_7,line_list_8)

    one_color_1 = random.randint(50,200)
    one_color_2 = random.randint(50,200)
    one_color_3 = random.randint(50,200)
    
    two_color_1 = random.randint(50,200)
    two_color_2 = random.randint(50,200)
    two_color_3 = random.randint(50,200)
    
    three_color_1 = random.randint(50,200)
    three_color_2 = random.randint(50,200)
    three_color_3 = random.randint(50,200)
    
    four_color_1 = random.randint(50,200)
    four_color_2 = random.randint(50,200)
    four_color_3 = random.randint(50,200)

    five_color_1 = random.randint(50,200)
    five_color_2 = random.randint(50,200)
    five_color_3 = random.randint(50,200)
    
    six_color_1 = random.randint(50,200)
    six_color_2 = random.randint(50,200)
    six_color_3 = random.randint(50,200)
    
    seven_color_1 = random.randint(50,200)
    seven_color_2 = random.randint(50,200)
    seven_color_3 = random.randint(50,200)
    
    eight_color_1 = random.randint(50,200)
    eight_color_2 = random.randint(50,200)
    eight_color_3 = random.randint(50,200)
    
    row_show(row_list_1)
    row_show(row_list_2)
    row_show(row_list_3)
    row_show(row_list_4)
    row_show(row_list_5)
    row_show(row_list_6)
    row_show(row_list_7)
    row_show(row_list_7)
    colorWipe(strip,Color(0,0,0),0)
    
    

def row_show(row_1):
    global line_list_1
    global line_list_2
    global line_list_3
    global line_list_4
    global line_list_5
    global line_list_6
    global line_list_7
    global line_list_8
    
    global one_color_1
    global one_color_2
    global one_color_3
    
    global two_color_1
    global two_color_2
    global two_color_3
    
    global three_color_1
    global three_color_2
    global three_color_3
    
    global four_color_1
    global four_color_2
    global four_color_3
    
    global five_color_1
    global five_color_2
    global five_color_3
    
    global six_color_1
    global six_color_2
    global six_color_3
    
    global seven_color_1
    global seven_color_2
    global seven_color_3
    
    global eight_color_1
    global eight_color_2
    global eight_color_3
    

    
    row = row_1
    for i in range(len(row)):
        if row[i] in line_list_1:
            strip.setPixelColor(row[i],Color(one_color_1,one_color_2,one_color_3))
        if row[i] in line_list_2:
            strip.setPixelColor(row[i],Color(two_color_1,two_color_2,two_color_3))
        if row[i] in line_list_3:
            strip.setPixelColor(row[i],Color(three_color_1,three_color_2,three_color_3))
        if row[i] in line_list_4:
            strip.setPixelColor(row[i],Color(four_color_1,four_color_2,four_color_3))
        if row[i] in line_list_5:
            strip.setPixelColor(row[i],Color(five_color_1,five_color_2,five_color_3))
        if row[i] in line_list_6:
            strip.setPixelColor(row[i],Color(six_color_1,six_color_2,six_color_3))
        if row[i] in line_list_7:
            strip.setPixelColor(row[i],Color(seven_color_1,seven_color_2,seven_color_3))
        if row[i] in line_list_8:
            strip.setPixelColor(row[i],Color(eight_color_1,eight_color_2,eight_color_3))
    strip.show()


def gradual(number):
    for i in range(number):    
        a = 50
        left_1 = [0,8]
        right_1 = [23,31]
        left_2 = [32,40]
        right_2 = [55,63]
        for j in range(7):
            rgb_in(left_1,0.005,a,a,0)
            rgb_in(left_2,0.005,a,a,0)
            rgb_in(right_1,0.005,a,a,0)
            rgb_in(right_2,0.005,a,a,0)
            for i in range(2):
                left_1.append(left_1[0]+1)
                left_1.remove(left_1[0])
                right_1.append(right_1[0]-1)
                right_1.remove(right_1[0])
                left_2.append(left_2[0]+1)
                left_2.remove(left_2[0])
                right_2.append(right_2[0]-1)
                right_2.remove(right_2[0])
            a = a + 28
            rgb_in(left_1,0.005,a,a,0)
            rgb_in(left_2,0.005,a,a,0)
            rgb_in(right_1,0.005,a,a,0)
            rgb_in(right_2,0.005,a,a,0)
            
        a = 50
        left_1 = [0,8]
        right_1 = [23,31]
        left_2 = [32,40]
        right_2 = [55,63]
        for j in range(7):
            rgb_in(left_1,0.005,a,0,a)
            rgb_in(left_2,0.005,a,0,a)
            rgb_in(right_1,0.005,a,0,a)
            rgb_in(right_2,0.005,a,0,a)
            for i in range(2):
                left_1.append(left_1[0]+1)
                left_1.remove(left_1[0])
                right_1.append(right_1[0]-1)
                right_1.remove(right_1[0])
                left_2.append(left_2[0]+1)
                left_2.remove(left_2[0])
                right_2.append(right_2[0]-1)
                right_2.remove(right_2[0])
            a = a + 28
            rgb_in(left_1,0.005,a,0,a)
            rgb_in(left_2,0.005,a,0,a)
            rgb_in(right_1,0.005,a,0,a)
            rgb_in(right_2,0.005,a,0,a)
            
        a = 50
        left_1 = [0,8]
        right_1 = [23,31]
        left_2 = [32,40]
        right_2 = [55,63]
        for j in range(7):
            rgb_in(left_1,0.005,0,a,a)
            rgb_in(left_2,0.005,0,a,a)
            rgb_in(right_1,0.005,0,a,a)
            rgb_in(right_2,0.005,0,a,a)
            for i in range(2):
                left_1.append(left_1[0]+1)
                left_1.remove(left_1[0])
                right_1.append(right_1[0]-1)
                right_1.remove(right_1[0])
                left_2.append(left_2[0]+1)
                left_2.remove(left_2[0])
                right_2.append(right_2[0]-1)
                right_2.remove(right_2[0])
            a = a + 28
            rgb_in(left_1,0.005,0,a,a)
            rgb_in(left_2,0.005,0,a,a)
            rgb_in(right_1,0.005,0,a,a)
            rgb_in(right_2,0.005,0,a,a)
          
        for i in range(3):
            a = random.randint(0,255)
            b = random.randint(0,255)
            c = random.randint(0,255)
            left_1 = [0,1]
            right_1 = [58,59]
            left_2 = [4,5]
            right_2 = [62,63]
            for j in range(7):
                rgb_in(left_1,0.005,a,b,c)
                rgb_in(left_2,0.005,a,b,c)
                rgb_in(right_1,0.005,a,b,c)
                rgb_in(right_2,0.005,a,b,c)
                for i in range(2):
                    left_1.append(left_1[0]+8)
                    left_1.remove(left_1[0])
                    right_1.append(right_1[0]-8)
                    right_1.remove(right_1[0])
                    left_2.append(left_2[0]+8)
                    left_2.remove(left_2[0])
                    right_2.append(right_2[0]-8)
                    right_2.remove(right_2[0])
                rgb_in(left_1,0.005,a,b,c)
                rgb_in(left_2,0.005,a,b,c)
                rgb_in(right_1,0.005,a,b,c)
                rgb_in(right_2,0.005,a,b,c)
            
            
            
        

    
    
    

def exec_cmd(key_val):
    happy_smiley = [2,3,4,5,9,14,16,18,21,23,24,31,32,34,37,39,40,42,43,44,45,47,49,54,58,59,60,61]
    heart = [1,6,8,9,10,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,41,42,43,44,45,46,50,51,52,53,59,60]
    sad_smiley = [2,3,4,5,9,14,16,18,21,23,24,31,32,34,35,36,37,39,40,42,45,47,49,54,58,59,60,61]
    small_heart = [17,22,24,25,30,31,32,33,34,37,38,39,41,42,43,44,45,46,50,51,52,53,59,60]
    
    global CH_sub_number
    global CH_number
    global CH_add_number
    global left_number
    global right_number
    global play_number
    global vol_sub_number
    global vol_add_number
    global EQ_number
    global Zero_number
    global one_hundred_number
    global two_hundred_number
    global vol
    global four_number
    global five
    global number_name
    global music_go
    
    if(key_val==0x45):
        print("Button CH-")
        CH_add_number = 0
        CH_number = 0
        CH_sub_number = CH_sub_number + 1
        # if CH_sub_number % 2 == 1:
        #     colorWipe(strip,Color(0,0,0),0)
        #     for i in heart:
        #         strip.setPixelColor(i,Color(255,0,0))
        #     strip.show()
        # else:
        #     colorWipe(strip,Color(0,0,0),0)
            
    elif(key_val==0x46):
        print("Button CH")
        CH_add_number = 0
        CH_sub_number = 0
        CH_number = CH_number + 1
        # if CH_number % 2 == 1:
        #     colorWipe(strip,Color(0,0,0),0)
        #     for i in happy_smiley:
        #         strip.setPixelColor(i,Color(0,255,0))
        #         strip.show()
        # else:
        #     colorWipe(strip,Color(0,0,0),0)
            
    elif(key_val==0x47):
        print("Button CH+")
        CH_number = 0
        CH_sub_number = 0
        CH_add_number = CH_add_number + 1
        # if CH_add_number % 2 == 1:
        #     colorWipe(strip,Color(0,0,0),0)
        #     for i in sad_smiley:
        #         strip.setPixelColor(i,Color(0,0,255))
        #         strip.show()
        # else:
        #     colorWipe(strip,Color(0,0,0),0)
            
    elif(key_val==0x44):
        print("Button PREV")
        left_number = left_number + 1
        if left_number % 2 == 1:
            # GPIO.output(buzzer_pin,GPIO.HIGH)
            buzzer_sensor.on()
        else:
            # GPIO.output(buzzer_pin, GPIO.LOW)
            buzzer_sensor.off()
        
    elif(key_val==0x40):
        print("Button NEXT")
        right_number = right_number + 1
        if right_number % 2 == 1:
            # GPIO.output(shake_pin,GPIO.HIGH)
            shake_sensor.on()
        else:
            # GPIO.output(shake_pin, GPIO.LOW)
            shake_sensor.off()
        
    elif(key_val==0x43):
        print("Button PLAY/PAUSE")
        play_number = play_number + 1
        if play_number % 2 == 1:
            pygame.mixer.music.load("/home/pi/Videos/music/%s.mp3" % number_name)
            pygame.mixer.music.play()
            print("play")
            music_go = 1
        else:
            pygame.mixer.music.stop()
            print("stop")
            number_name = 1
            music_go = 0
            
    elif(key_val==0x07):
        #pygame.mixer.music.stop()
        if music_go == 1:
            if number_name > 1:
                number_name = number_name - 1
                pygame.mixer.music.load("/home/pi/Videos/music/%s.mp3" % number_name)
                pygame.mixer.music.play()
            else:
                pygame.mixer.music.load("/home/pi/Videos/music/%s.mp3" % number_name)
                pygame.mixer.music.play()
        else:
            print("music no play")
    
    elif(key_val==0x15):
        if music_go == 1:
            if number_name < 9:
                number_name = number_name + 1
                pygame.mixer.music.load("/home/pi/Videos/music/%s.mp3" % number_name)
                pygame.mixer.music.play()
            else:
                pygame.mixer.music.load("/home/pi/Videos/music/%s.mp3" % number_name)
                pygame.mixer.music.play()
        else:
            print("music no play")
    elif(key_val==0x09):
        print("EQ")
        EQ_number = EQ_number + 1
        if (EQ_number % 2) == 1:
#             humidity, temperature = Adafruit_DHT.read_retry(sensor, dht_pin)
            # get_DHT20()
            pass
#             if humidity is not None and temperature is not None:
#                 lcd_screen.write_lcd(text=('Temp = {0:0.1f}*c \nHumd = {1:0.1f}%\n'.format(temperature, humidity)))
        else:
            lcd_screen.clear()
            lcd_screen.turn_off()
            
    elif(key_val==0x16):
        print("Button 0")
        one_hundred(10)
        two_hundred(10)
        one()
        theaterChase(strip, Color(127, 127, 127))  # White theater chase
        theaterChase(strip, Color(127, 0, 0))  # Red theater chase
        theaterChase(strip, Color(0, 0, 127))  # Blue theater chase
        colorWipe(strip,Color(0,0,0),0)
        rainbow(strip)
        colorWipe(strip,Color(0,0,0),0)
        for p in range(3):
            for j in range(5,250,5):
                for i in heart:
                    strip.setPixelColor(i,Color(j,0,0))
                strip.show()
                time.sleep(0.01)
                
            for j in range(250,5,-5):
                for i in heart:
                    strip.setPixelColor(i,Color(j,0,0))
                strip.show()
                time.sleep(0.01)
        colorWipe(strip,Color(0,0,0),0)
        all_RGB_run(40)
        all_RGB(0,0,0,0)
        mod_RGB_run(4)
        all_RGB(0,0,0,0)
        for i in range(25):
            music_RGB()
        all_RGB(0,0,0,0)
        gradual(3)
        all_RGB(0,0,0,0)
        tree(3)
        all_RGB(0,0,0,0)
        
    elif(key_val==0x19):
        print("Button 100+")
        one_hundred(25)
        
    elif(key_val==0x0d):
        print("Button 200+")
        for i in range(4):
            two_hundred(10)
        all_RGB(0,0,0,0)  
        
    elif(key_val==0x0c):
        print("Button 1")
        one()

            
    elif(key_val==0x18):
        print("Button 2")
        for i in range(2):
            theaterChase(strip, Color(127, 127, 127))  # White theater chase
            theaterChase(strip, Color(127, 0, 0))  # Red theater chase
            theaterChase(strip, Color(0, 0, 127))  # Blue theater chase
            colorWipe(strip,Color(0,0,0),0)
        
    elif(key_val==0x5e):
        print("Button 3")
        for i in range(3):
            rainbow(strip)
        colorWipe(strip,Color(0,0,0),0)
        
    elif(key_val==0x08):
        heart_right = 0
        print("Button 4")
        colorWipe(strip,Color(0,0,0),0)
        while True:
            print(heart_right)
            if heart_right == 0:
                for j in range(5,250,5):
                    if heart_right == 0:
                        for i in heart:
                            strip.setPixelColor(i,Color(j,0,0))
                            if return_number(0x08):
                                heart_right = 1
                                continue
                        strip.show()
                        time.sleep(0.01)
                    else:
                        continue
                    
                for j in range(250,5,-5):
                    if heart_right == 0:
                        for i in heart:
                            strip.setPixelColor(i,Color(j,0,0))
                            if return_number(0x08):
                                heart_right = 1
                                continue
                        strip.show()
                        time.sleep(0.01)
                    else:
                        continue
            else:
                break
        colorWipe(strip,Color(0,0,0),0)
        
        

    elif(key_val==0x1c):
        five = 0
        print("Button 5")
        all_RGB_run(100)
        all_RGB(0,0,0,0)

        
    elif(key_val==0x5a):
        six = 0
        print("Button 6")
        for i in range(2):
            mod_RGB_run(5)
        all_RGB(0,0,0,0)
        
    elif(key_val==0x42):
        print("Button 7")
        # 5s
        for i in range(50):
            music_RGB()

        
    elif(key_val==0x52):
        print("Button 8")
        gradual(5)
        all_RGB(0,0,0,0)
        
    elif(key_val==0x4a):
        print("Button 9")
        for i in range(1):
            tree(10)
        all_RGB(0,0,0,0)
        

def return_number(data_number):
    # if GPIO.input(ir_pin) == 0:
    if ir_sensor.value == 0:
        count = 0
        # while GPIO.input(ir_pin) == 0 and count < 200:
        while ir_sensor.value == 0 and count < 200:
            count += 1
            time.sleep(0.00006)

        count = 0
        # while GPIO.input(ir_pin) == 1 and count < 80:
        while ir_sensor.value == 1 and count < 80:
            count += 1
            time.sleep(0.00006)

        idx = 0
        cnt = 0
        data = [0,0,0,0]
        for i in range(0,32):
            count = 0
            # while GPIO.input(ir_pin) == 0 and count < 15:
            while ir_sensor.value == 0 and count < 15:
                count += 1
                time.sleep(0.00006)

            count = 0
            # while GPIO.input(ir_pin) == 1 and count < 40:
            while ir_sensor.value == 1 and count < 40:
                count += 1
                time.sleep(0.00006)

            if count > 8:
                data[idx] |= 1<<cnt
            if cnt == 7:
                cnt = 0
                idx += 1
            else:
                cnt += 1
        if data[0]+data[1] == 0xFF and data[2]+data[3] == 0xFF:
            print("Get the key: 0x%02x" %data[2])
            if data[2] == data_number:
                return True
            else:
                return False

    

def cleanup():

    # GPIO.cleanup()
    ir_sensor.close()
    buzzer_sensor.close()
    shake_sensor.close()

def delay(times):
   time.sleep(times/500.0)

def colorWipe(strip, color, wait_ms=50):
    """Wipe color across display a pixel at a time."""
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, color)
        strip.show()
        time.sleep(wait_ms / 1000.0)

lcd_screen = LCDModule()

# Intialize the library (must be called once before other functions).
# segment.begin()
strip = PixelStrip(64, 10)
strip.begin()

try:
    while True:
        if ir_sensor.value == 0:
            count = 0
            while ir_sensor.value == 0 and count < 200:
                count += 1
                time.sleep(0.00006)

            count = 0
            while ir_sensor.value == 1 and count < 80:
                count += 1
                time.sleep(0.00006)

            idx = 0
            cnt = 0
            data = [0,0,0,0]
            for i in range(0,32):
                count = 0
                while ir_sensor.value == 0 and count < 15:
                    count += 1
                    time.sleep(0.00006)

                count = 0
                while ir_sensor.value == 1 and count < 40:
                    count += 1
                    time.sleep(0.00006)

                if count > 8:
                    data[idx] |= 1<<cnt
                if cnt == 7:
                    cnt = 0
                    idx += 1
                else:
                    cnt += 1
            if data[0]+data[1] == 0xFF and data[2]+data[3] == 0xFF:
                print("Get the key: 0x%02x" %data[2])
                exec_cmd(data[2])

except KeyboardInterrupt:
    # colorWipe(strip,Color(0,0,0),0)
    # GPIO.cleanup();
    ir_sensor.close()
    buzzer_sensor.close()
    shake_sensor.close()
    lcd_screen.clear()
    lcd_screen.turn_off()
    pygame.mixer.music.stop()
