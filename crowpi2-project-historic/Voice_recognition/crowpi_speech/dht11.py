import time
import HD44780MCP
import MCP230XX
import smbus2

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

pin = 4
address = 0x38 #Put your device's address here


def get_DHT20():
   i2cbus = smbus2.SMBus(1)
   time.sleep(0.5)
      
   data = i2cbus.read_i2c_block_data(address,0x71,1)
   if (data[0] | 0x08) == 0:
      print('Initialization error')
      
   i2cbus.write_i2c_block_data(address,0xac,[0x33,0x00])
   time.sleep(0.1)
      
   data = i2cbus.read_i2c_block_data(address,0x71,7)
      
   Traw = ((data[3] & 0xf) << 16) + (data[4] << 8) + data[5]
   temperature = 200*float(Traw)/2**20 - 50
      
   Hraw = ((data[3] & 0xf0) >> 4) + (data[1] << 12) + (data[2] << 4)
   humidity = 100*float(Hraw)/2**20

   return humidity, temperature

try:
    while True:
        temp,humi = get_DHT20()
        if temp is not None and humi is not None:
            print("displaying weather information on LCD!")
    #             lcd_screen.clear()
            lcd_screen.write_lcd(text=('Temp = {0:0.2f}*c \nHumd = {1:0.2f}%\n'.format(temp, humi)))
            print("Temperature: %-3.1f C" % temp)
            print("Humidity: %-3.1f %%" % humi)
            time.sleep(3)
            lcd_screen.clear()
            lcd_screen.turn_off()
            break
        else:
            continue

except KeyboardInterrupt:
    print("Cleanup")
    lcd_screen.turn_off()
