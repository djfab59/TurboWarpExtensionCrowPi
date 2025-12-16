from gpiozero import InputDevice
import time
import os
import HD44780MCP
import MCP230XX

motion_pin = 23

motion_sensor = InputDevice(motion_pin)

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

try:
    while True:
       if(motion_sensor.value == 0):
             lcd_screen.write_lcd("checking...\n                ")
       elif(motion_sensor.value == 1):
             lcd_screen.clear()
             lcd_screen.write_lcd("recording...")
             ts = int(time.time())
             os.system("ffmpeg -t 7 -f v4l2 -framerate 60 -video_size 1280x720 -i /dev/video0 /home/pi/Videos/%s.avi"%ts)
             lcd_screen.clear()
             lcd_screen.write_lcd("recorded")
             time.sleep(1)
             lcd_screen.turn_off()
             os.system("vlc /home/pi/Videos/%s.avi"%ts)
             break
       time.sleep(0.1)
except KeyboardInterrupt:
    motion_sensor.close()
    lcd_screen.turn_off()

# import subprocess
# import os 
# import sys

# subprocess.call("sudo python /usr/share/code/project/PIR_activated_video/PIR_activated_video01.py", shell=True)


