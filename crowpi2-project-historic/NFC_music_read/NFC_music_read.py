import socket
import time
import signal
from mfrc522 import SimpleMFRC522
import HD44780MCP
import MCP230XX
import pygame
import sys

CARD_KEY = [0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF]
# init the mp3 player
pygame.mixer.init()
NUMBERS = [
    ('0',0),
    ('1',1),
    ('2',2),
    ('3',3),
    ('4',4),
    ('5',5),
    ('6',6),
    ('7',7),
    ('8',8),
    ('9',9),
    ('10',10)
]
run = True
rdr = SimpleMFRC522()

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

def end_read(signal,frame):
    try:
        global run
        print("\nCtrl+C captured, ending read.")
        run = False
        sys.exit(0)
    except KeyboardInterrupt:
        rdr.cleanup()
        pygame.mixer.music.stop()

signal.signal(signal.SIGINT, end_read)

lcd_screen.clear()
lcd_screen.write_lcd("checking...")

while run:
    rdr.wait4Tag(2)
    (error, data) = rdr.READER.MFRC522_Request(rdr.READER.PICC_REQIDL)

    if not error:
        print("[-] Card Detected: " + format(data, "02x"))

    (error, uid) = rdr.READER.MFRC522_Anticoll()
    if not error:
        # Found a card, now try to read block 4 to detect the number type.
        print("[-] Card read UID: "+str(uid[0])+","+str(uid[1])+","+str(uid[2])+","+str(uid[3]))
        
        # First authenticate block 4.
        rdr.READER.MFRC522_SelectTag(uid)
        error = rdr.READER.MFRC522_Auth(rdr.READER.PICC_AUTHENT1A, 8, CARD_KEY, uid)

        data = None
        if error == rdr.READER.MI_OK:
            data = rdr.READER.MFRC522_Read(8)

        if data[0:4] != [77, 67, 80, 73]:
            print('Card is written with wrong data, cannot be identified!')
            continue
            # Parse out the block type and subtype.
        number_id = data[4]
        # Find the block name (it's ugly to search for it, but there are only 10 numbers).
        for number in NUMBERS:
            if number[1] == number_id:
                number_name = number[0]
                print('Found number!')
                break
        print('Number value: {0}'.format(number_name))
        try:
            lcd_screen.clear()
            lcd_screen.write_lcd("%s.mp3"%number_name)
            time.sleep(1)
            lcd_screen.turn_off()
            pygame.mixer.music.load("/home/pi/Videos/music/%s.mp3" % number_name)
            pygame.mixer.music.play()
            input()

        except KeyboardInterrupt:
            time.sleep(1)
            lcd_screen.turn_off()
            pygame.mixer.music.stop()
            continue

