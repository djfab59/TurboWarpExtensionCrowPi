#coding:utf-8
import time
import RPi.GPIO as GPIO
import adafruit_dht
import HD44780MCP
import MCP230XX

sensor = 11
pin = 4
humidity = 0
temperature = 0
GPIO.setmode(GPIO.BCM)

instance = adafruit_dht.DHT11(pin)

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


if instance.temperature is not None and instance.humidity is not None:
	lcd_screen.write_lcd(text=('Temp = {0:0.2f}*c \nHumd = {1:0.2f}%\n'.format(instance.temperature, instance.humidity)))
else:
	print('Failed to get reading. Try again!')
	lcd_screen.write_lcd(text='Failed reading.\nTry again!')
