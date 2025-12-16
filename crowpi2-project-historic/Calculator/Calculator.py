#!/usr/bin/python
# -*- coding: utf-8 -*-
# Author : original author stenobot
# Original Author Github: https://github.com/stenobot/SoundMatrixPi
# http://elecrow.com/
from __future__ import division
import RPi.GPIO as GPIO
import time
import spidev
import HD44780MCP
import MCP230XX
import os


# Open SPI bus
spi = spidev.SpiDev()
spi.open(0,1)
spi.max_speed_hz=1000000

class ButtonMatrix():

    def __init__(self):

        self.calculated = ""

        # GPIO.setmode(GPIO.BCM)

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
            self.calculated = self.calculated + "*"
        elif(btnIndex == 8):
            self.calculated = self.calculated + "/"
        elif(btnIndex == 12):
            self.calculated = self.calculated + "+"
        elif(btnIndex == 16):
            self.calculated = self.calculated + "-"
        elif(btnIndex == 15):
            # calculate
            self.calculated = str(eval(self.calculated))
        return self.calculated

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
lcd_screen.turn_on()

# initial the button matrix
buttons = ButtonMatrix()

try:
    while True:
            # get buttons press from SPI
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
                        lcd_screen.write_lcd(calculated)
            time.sleep(buttons.delay)

except KeyboardInterrupt:
    lcd_screen.clear()
    lcd_screen.turn_off()
    GPIO.cleanup()
