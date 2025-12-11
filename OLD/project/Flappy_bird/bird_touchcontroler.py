import RPi.GPIO as GPIO
import time
import pyautogui

# store the GPIO control pins
TOUCH_PIN = 11




# set GPIO mode to GPIO BOARD
GPIO.setmode(GPIO.BOARD)

# set gpio buttons as INPUT
GPIO.setup(TOUCH_PIN, GPIO.IN)

try:
    while True:

        if(GPIO.input(TOUCH_PIN)):
            pyautogui.press("space")
            
except KeyboardInterrupt:
    GPIO.cleanup()

