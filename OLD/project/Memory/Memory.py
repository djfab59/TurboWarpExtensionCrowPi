import time
import random
import spidev
# import RPi.GPIO as GPIO
from gpiozero import InputDevice
import HD44780MCP
import MCP230XX
import spidev
from elecrow_ws281x import *
import os


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


x_channel = 1
y_channel = 0

delay = 0.05

sprite_number = 0
touch_right = 0
a = []
True_on = []

win = -1
button_number = 0
input_number = 0

TOUCH_PIN = 17
touch_sensor = InputDevice(TOUCH_PIN)
 
# Open SPI bus
spi = spidev.SpiDev()
spi.open(0,1)
spi.max_speed_hz=1000000


# Open SPI bus
spi = spidev.SpiDev()
spi.open(0,1)
spi.max_speed_hz=1000000

class ButtonMatrix():

    def __init__(self):

        self.calculated = ""

        # Define key channels
        self.key_channel = 4
        self.delay = 0.1

        self.adc_key_val = [30,90,160,230,280,330,400,470,530,590,650,720,780,840,890,960]
        self.key = -1
        self.oldkey = -1
        self.num_keys = 16

        self.indexes = {
            12:1,
            13:2,
            14:3,
            15:4,
            10:5,
            9:6,
            8:7,
            11:8,
            4:9,
            5:10,
            6:11,
            7:12,
            0:13,
            1:14,
            2:15,
            3:16
        }

    def ReadChannel(self,channel):
        # Function to read SPI data from MCP3008 chip
        # Channel must be an integer 0-7
        adc = spi.xfer2([1,(8+channel)<<4,0])
        data = ((adc[1]&3) << 8) + adc[2]
        return data
    
    def GetAdcValue(self):
        adc_key_value = self.ReadChannel(self.key_channel)
        return adc_key_value

    def GetKeyNum(self,adc_key_value):
        for num in range(0,16):
            if adc_key_value < self.adc_key_val[num]:
                return num
        if adc_key_value >= self.num_keys:
            num = -1
            return num

    def activateButton(self, btnIndex):
        # get the index from SPI
        btnIndex = int(btnIndex)
        # correct the index to better format
        btnIndex = self.indexes[btnIndex]
        # run calculator function
        self.calculate(btnIndex)
        print("button %s pressed" % btnIndex)
        # prevent button presses too close together
        time.sleep(.3)
        return self.calculated

    def calculate(self,btnIndex):
        global button_number
        global input_number
        # get the index from SPI
        btnIndex = int(btnIndex)
        # numbers
        if(btnIndex == 1):
            self.calculated = self.calculated + "7"
        elif(btnIndex == 2):
            self.calculated = self.calculated + "8"
        elif(btnIndex == 3):
            self.calculated = self.calculated + "9"
        elif(btnIndex == 5):
            self.calculated = self.calculated + "6"
        elif(btnIndex == 6):
            self.calculated = self.calculated + "5"
        elif(btnIndex == 7):
            self.calculated = self.calculated + "4"
        elif(btnIndex == 9):
            self.calculated = self.calculated + "1"
        elif(btnIndex == 10):
            self.calculated = self.calculated + "2"
        elif(btnIndex == 11):
            self.calculated = self.calculated + "3"
        elif(btnIndex == 13):
            self.calculated = self.calculated + "0"
        # reset
        elif(btnIndex == 14):
            self.calculated = ""
        # functions
        elif(btnIndex == 4):
            self.calculated = self.calculated + " "
        elif(btnIndex == 8):
            self.calculated = self.calculated + " "
        elif(btnIndex == 12):
            self.calculated = self.calculated + " "
        elif(btnIndex == 16):
            self.calculated = self.calculated + " "
        elif(btnIndex == 15):
            # calculate
            self.calculated = str(eval(self.calculated))
            button_number = 1
            input_number = self.calculated
        return self.calculated


 
# Function to read SPI data from MCP3008 chip
# Channel must be an integer 0-7
def ReadChannel(channel):
  adc = spi.xfer2([1,(8+channel)<<4,0])
  data = ((adc[1]&3) << 8) + adc[2]
  return data

# Define functions which animate LEDs in various ways.
def colorWipe(strip, color, wait_ms=50):
    """Wipe color across display a pixel at a time."""
    # for i in range(strip.numPixels()):
    #     strip.setPixelColor(i, color)
    #     strip.show()
    strip.fillColor(color)
    time.sleep(wait_ms / 1000.0)

def sprite():
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
        if sprite_number in sprite_number_left:
            sprite_number = sprite_number
        else:
            sprite_number = sprite_number - 1
    if x_value < 400:
        print("Right")
        if sprite_number in sprite_number_right:
            sprite_number = sprite_number
        else:
            sprite_number = sprite_number + 1
    if y_value > 650:
        print("Up")
        if sprite_number in sprite_number_up:
            sprite_number = sprite_number
        else:
            sprite_number = sprite_number - 8
    if y_value < 400:
        print("Down")
        if sprite_number in sprite_number_down:
            sprite_number = sprite_number
        else:
            sprite_number = sprite_number + 8

    # Wait before repeating loop
    time.sleep(delay)
    
    strip.setPixelColor(sprite_number,Color(255,255,255))
    # strip.show()
    time.sleep(0.03)
    strip.setPixelColor(sprite_number,Color(0,0,0))
    # strip.show()
    time.sleep(0.03)

def random_sprite(number):
    global a
    for i in range(0,number,1):
        a.append(random.randint(0,63))
        while a.count(a[i]) == 2:
            a[i] = (random.randint(0,63))

#     for i in range(0,number,1):
#         strip.setPixelColor(a[i],Color(255,0,255))
#     strip.show()
        
    for j in range(0,64,1):
        if j in a:
            strip.setPixelColor(j,Color(255,0,0))
            # strip.show()
            time.sleep(0.05)
        else:
            strip.setPixelColor(j,Color(255,255,255))
            # strip.show()
            time.sleep(0.05)
    
    colorWipe(strip,Color(0,0,0),10)
    time.sleep(1)
    # strip.show()

def touch_on():
    global True_on
    global touch_right
    global win
    True_go = 0
    # if(GPIO.input(TOUCH_PIN) == 1):
    if(touch_sensor.value):
        True_on.append(sprite_number)
        time.sleep(0.3)
        print(True_on)
        if(True_on[touch_right] in a):
            touch_right = touch_right + 1
            if touch_right == len(a):
                win = 1
                True_go = 1
        else:
            win = 0
            True_go = 1
        
        while True_go == 0:
            x_value = ReadChannel(x_channel)
            y_value = ReadChannel(y_channel)
            strip.setPixelColor(sprite_number,Color(0,255,0))
            # strip.show()
            if(x_value > 650 or x_value < 400 or y_value > 650 or y_value < 400):
#                 True_on.append(sprite_number)
                sprite()
                True_go = 1

    # for i in range(0,len(True_on),1):
    #     strip.setPixelColor(True_on[i],Color(0,255,0))
    strip.sendPos2Show(True_on, 0, 255, 0)
        

def button_input():
    adc_key_value = buttons.GetAdcValue()
    key = buttons.GetKeyNum(adc_key_value)
    if key != buttons.oldkey:
        time.sleep(0.05)
        adc_key_value = buttons.GetAdcValue()
        key = buttons.GetKeyNum(adc_key_value)
        if key != buttons.oldkey:
            oldkey = key
            if key >= 0:
                # button pressed, activate it
                calculated = buttons.activateButton(key)
                print(calculated)
                # clear LCD before showing new value
                lcd_screen.clear()
                # show calculated value on LCD
                
                lcd_screen.write_lcd('input number:'+calculated)
    time.sleep(buttons.delay)




# initial the button matrix
buttons = ButtonMatrix()
# Intialize the library (must be called once before other functions).
strip = PixelStrip(64, 10)
strip.begin()

right_smiley = [40,49,58,51,44,37,30,23]
worry_smiley = [9,18,27,36,45,54,14,21,28,35,42,49]

# main
colorWipe(strip,Color(0,0,0),10)

lcd_screen.write_lcd('input number:')


while button_number == 0:
    button_input()

true_false = 1

random_sprite(int(input_number))
try:
    while true_false == 1:
        sprite()
        touch_on()
        if win == 0:
#             break
            true_false = -1
        if win == 1:
            colorWipe(strip,Color(0,0,0),10)
            while true_false == 1:
                for i in right_smiley:
                    strip.setPixelColor(i,Color(0,255,0))
                    strip.show()
                time.sleep(3)
#                 break
                true_false = 0
    colorWipe(strip,Color(0,0,0),10)
    if true_false == -1:
        for i in worry_smiley:
            strip.setPixelColor(i,Color(255,0,0))
            strip.show()
        time.sleep(3)
        colorWipe(strip,Color(0,0,0),10)
    lcd_screen.turn_off() 
except KeyboardInterrupt:
    # colorWipe(strip,Color(0,0,0),10)
    # GPIO.cleanup()
    strip.fill()
    touch_sensor.close()
    lcd_screen.clear()
    lcd_screen.turn_off()
