#!/usr/bin/env python
# Raspberry Pi Minecraft Block NFC Writer
# Author: Tony DiCola
# Copyright (c) 2015 Adafruit Industries
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import signal
import time
from mfrc522 import SimpleMFRC522
import Adafruit_CharLCD as LCD
import spidev
import sys

# Define LCD column and row size for 16x2 LCD.
lcd_columns = 16
lcd_rows    = 2

# Initialize the LCD using the pins
lcd = LCD.Adafruit_CharLCDBackpack(address=0x21)

# Open SPI bus
spi = spidev.SpiDev()
spi.open(0,1)
spi.max_speed_hz=1000000

class ButtonMatrix():

    def __init__(self):

        # Define key channels
        self.key_channel = 4
        self.delay = 0.1

        self.adc_key_val = [30,90,160,230,280,330,400,470,530,590,650,720,780,840,890,960]
        self.key = -1
        self.oldkey = -1
        self.num_keys = 16

        '''
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
        '''
        self.indexes = {
                12:7,
                13:8,
                14:9,
                15:6,
                10:6,
                9:5,
                8:4,
                11:8,
                4:1,
                5:2,
                6:3,
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
        print("button %s pressed" % btnIndex)
        # prevent button presses too close together
        time.sleep(.3)
        return btnIndex
        
# initial the button matrix
buttons = ButtonMatrix()
# turn LCD backlight on
lcd.set_backlight(0)

# clear LCD before showing new value
lcd.clear()

# Configure the key to use for writing to the MiFare card.  You probably don't
# need to change this from the default below unless you know your card has a
# different key associated with it.
CARD_KEY = [0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF]

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
    ('9',9)
]

run = True
rdr = SimpleMFRC522()

def end_read(signal,frame):
    global run
    print("\nCtrl+C captured, ending read.")
    run = False
    rdr.cleanup()

signal.signal(signal.SIGINT, end_read)

print("Starting")
lcd.message("Please place\nthe card")

# Step 1, wait for card to be present.
print('Numbers NFC writer')
print('')
print('== STEP 1 =========================')
print('Place the card to be written on the RC522 NFC Reader/Wrtier...')

while run:
    rdr.wait4Tag(2)
    (error, data) = rdr.READER.MFRC522_Request(rdr.READER.PICC_REQIDL)
    if not error:
        print("[-] Card Detected: " + format(data, "02x"))

    (error, uid) = rdr.READER.MFRC522_Anticoll()
    if not error:
        print("[-] Card read UID: "+str(uid[0])+","+str(uid[1])+","+str(uid[2])+","+str(uid[3]))

        print('==============================================================')
        print('WARNING: DO NOT REMOVE CARD FROM RC522 UNTIL FINISHED WRITING!')
        print('==============================================================')
        print('')

        print('== STEP 2 =========================')
        print('Now pick a number to write to the card.')
        
        # clear lcd
        lcd.clear()
        # show calculated value on LCD
        lcd.message("Choose a number ..")

        number_choice = None
        while number_choice is None:
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
                        number_choice = buttons.activateButton(key)
                        # clear LCD before showing new value
                        lcd.clear()
                        if(number_choice <= 10 and number_choice >= 0):
                            # show calculated value on LCD
                            lcd.message("Number: %s" % number_choice)
                        else:
                            lcd.message("Wrong number ..")
        # Assume a number must have been entered.
        try:
            number_choice = int(number_choice)
        except ValueError:
            # Something other than a number was entered.  Try again.
            print('Error! Unrecognized option.')
            continue
        # Check choice is within bounds of numbers.
        if not (0 <= number_choice < len(NUMBERS)):
            print('Error! Block number must be within 0 to {0}.'.format(len(NUMBERS)-1))
            continue

        # Block was chosen, look up its name and ID.
        number_name, number_id = NUMBERS[number_choice]
        print('You chose the number name: {0}'.format(number_name))
        print('')
        
        time.sleep(1.5)

        # Confirm writing the block type.
        print('== STEP 3 =========================')
        print('Confirm you are ready to write to the card:')
        print('Number: {0}'.format(number_name))
        print('Confirm card write (Y or N)?')
        # ask to confirm on LCD
        lcd.clear()
        lcd.message("Confirm number %s?" % number_name)
        choice = None
        while choice is None:
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
                        choice = buttons.activateButton(key)
                        # clear LCD before showing new value
                        lcd.clear()
                        if(choice != 16):
                            # show calculated value on LCD
                            lcd.message('Fail!')
                            time.sleep(1.5)
                            lcd.clear()
                            # turn off LCD
                            lcd.set_backlight(1)
                            # leave program
                            sys.exit(0)
                        else:
                            print("Writing card (DO NOT REMOVE CARD FROM RC522)...")
                            # Write the card!
                            # First authenticate block 4.
                            rdr.READER.MFRC522_SelectTag(uid)
                            # set authorization key
                            status = rdr.READER.MFRC522_Auth(rdr.READER.PICC_AUTHENT1A, 8, CARD_KEY, uid)

                            # Next build the data to write to the card.
                            # Format is as follows:
                            # - Bytes 0-3 are a header with ASCII value 'MCPI'
                            # - Byte 4 is the block ID byte
                            # - Byte 5 is 0 if block has no subtype or 1 if block has a subtype
                            # - Byte 6 is the subtype byte (optional, only if byte 5 is 1)
                            if status == rdr.READER.MI_OK:

                                data = bytearray(16)
                                data[0:4] = b'MCPI'  # Header 'MCPI'
                                data[4]   = number_id & 0xFF
                                # Finally write the card.
                                rdr.READER.MFRC522_Write(8, data)
                                print('Wrote card successfully! You may now remove the card from the RC522.')
                                # clear LCD
                                lcd.clear()
                                # write success on LCD()
                                # show calculated value on LCD
                                lcd.message('Success!')
                                time.sleep(1.5)
                                lcd.clear()
                                # turn off LCD
                                lcd.set_backlight(1)
                                run = False
                            
                            else:
                                print("Authentification error")
                                continue