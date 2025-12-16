# import RPi.GPIO as GPIO
from gpiozero import Buzzer
import smbus
import time
import HD44780MCP
import MCP230XX
from elecrow_ws281x import *

bus = smbus.SMBus(1)
buzzer_pin = 18
buzzer_sensor = Buzzer(buzzer_pin)

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

class LightSensor():

    def __init__(self):

        # Define some constants from the datasheet

        self.DEVICE = 0x5c # Default device I2C address

        self.POWER_DOWN = 0x00 # No active state
        self.POWER_ON = 0x01 # Power on
        self.RESET = 0x07 # Reset data register value

        # Start measurement at 4lx resolution. Time typically 16ms.
        self.CONTINUOUS_LOW_RES_MODE = 0x13
        # Start measurement at 1lx resolution. Time typically 120ms
        self.CONTINUOUS_HIGH_RES_MODE_1 = 0x10
        # Start measurement at 0.5lx resolution. Time typically 120ms
        self.CONTINUOUS_HIGH_RES_MODE_2 = 0x11
        # Start measurement at 1lx resolution. Time typically 120ms
        # Device is automatically set to Power Down after measurement.
        self.ONE_TIME_HIGH_RES_MODE_1 = 0x20
        # Start measurement at 0.5lx resolution. Time typically 120ms
        # Device is automatically set to Power Down after measurement.
        self.ONE_TIME_HIGH_RES_MODE_2 = 0x21
        # Start measurement at 1lx resolution. Time typically 120ms
        # Device is automatically set to Power Down after measurement.
        self.ONE_TIME_LOW_RES_MODE = 0x23

    def convertToNumber(self, data):

        # Simple function to convert 2 bytes of data
        # into a decimal number
        return ((data[1] + (256 * data[0])) / 1.2)

    def readLight(self):

        data = bus.read_i2c_block_data(self.DEVICE,self.ONE_TIME_HIGH_RES_MODE_1)
        return self.convertToNumber(data)


def buzz():
    # Make buzzer sound
    buzzer_sensor.on()
    time.sleep(0.5)
    buzzer_sensor.off()

# define ws2812b
rp = PixelStrip(64, 10)
rp.begin()

def RGB_on():
    rp.fill(255,255,255)
		
def RGB_off():
    rp.fill(0,0,0)
    




# define light sensor
sensor = LightSensor()
# configure low light
low_light = 40

try:
    while True:
        sensor_data = sensor.readLight()
        a = int(sensor_data)
        lcd_screen.write_lcd(text="Light Level:\n%s lux             " % a)
        print("Light Level : " + str(int(sensor.readLight())) + " lux                       ")
        if(sensor_data < 40):
            # the light level is too low, activate buzzer
            RGB_on()
        else:
            RGB_off()
        time.sleep(0.5)
except KeyboardInterrupt:
    lcd_screen.clear()
    lcd_screen.turn_off()
    rp.clear()
    buzzer_sensor.close()