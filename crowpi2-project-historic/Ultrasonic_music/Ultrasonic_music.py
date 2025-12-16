from gpiozero import OutputDevice, InputDevice, DistanceSensor
from gpiozero import TonalBuzzer
from gpiozero.tones import Tone
import time
import math
import random
from elecrow_ws281x import *


tonePin = 18
# b = TonalBuzzer(tonePin)
distancesensor = DistanceSensor(echo = 26,trigger = 16, max_distance = 10)
a = 0

rp = PixelStrip(64, 10)
rp.begin()

def tone(pin,pitch,duration):
    b = TonalBuzzer(tonePin)
    if(pitch == 0):
        delay(duration)
        b.close()
        return
    b.play(pitch)
    delay(duration)
    b.close()
    delay(1)

def delay(times):
   time.sleep(times/500.0)


def colorWipe(strip, r, g, b, wait_ms=50):
    """Wipe color across display a pixel at a time."""
    strip.fill(r, g, b)

        
        
def distance():
    return round(distancesensor.distance * 100, 2)

def if_dis(number1,number2,light,pitch,duration):
    global a
    if a > number1 and a <= number2:
        print(distance())
        colorWipe(rp,0,0,0,0)

        rp.fill(red, green, blue, 255, light[0], light[-1])
        time.sleep(duration/1000.0)
        tone(tonePin, pitch,duration)
    
light_8 = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63]
light_7 = [8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63]
light_6 = [16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63]
light_5 = [24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63]
light_4 = [32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63]
light_3 = [40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63]
light_2 = [48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63]
light_1 = [56,57,58,59,60,61,62,63]

colorWipe(rp,0,0,0,0)

try:
    while True:
        a = distance()
        red = random.randint(10,254)
        green = random.randint(10,254)
        blue = random.randint(10,254)
        if_dis(0,5,light_1,262,50)
        if_dis(5,10,light_2,294,50)
        if_dis(10,15,light_3,330,50)
        if_dis(15,20,light_4,349,50)
        if_dis(20,25,light_5,392,50)
        if_dis(25,30,light_6,440,50)
        if_dis(30,35,light_7,494,50)
        if_dis(35,40,light_8,0,50)
        if a > 40 or a < 0:
            colorWipe(rp,0,0,0,0)
            tone(tonePin, 0, 50)
except KeyboardInterrupt:
    tone(tonePin, 0, 50)
    rp.clear()

