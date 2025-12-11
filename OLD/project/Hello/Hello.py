import time
import HD44780MCP
import MCP230XX
from gpiozero import *

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

# define sound pin
sound_pin = 24
# setup pin as INPUT
sound = DigitalInputDevice(sound_pin)

try:
    while True:
        # check if sound detected or not
        # the sound pin always HIGH unless sound detected, it goes LOW
        sound.wait_for_active()
        message = 'Hello'
        lcd_screen.write_lcd(message)
        lcd_screen.lcd.cursor(cursor = False)
        for i in range(lcd_screen.lcd_cols-len(message)):
            time.sleep(0.5)
            lcd_screen.lcd.scroll_right()
        for i in range(lcd_screen.lcd_cols-len(message)):
            time.sleep(0.5)
            lcd_screen.lcd.scroll_left()
        # Turn backlight off.
        time.sleep(2)
        lcd_screen.clear()
        lcd_screen.turn_off()

    else:
        # no sound detected turn off LCD
        lcd_screen.clear()
        lcd_screen.turn_off()
except KeyboardInterrupt:
    lcd_screen.clear()
    lcd_screen.turn_off()

