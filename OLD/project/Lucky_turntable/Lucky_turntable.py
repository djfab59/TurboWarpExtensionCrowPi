# -*- coding: utf-8 -*-
#!/usr/bin/env python
import threading
import time
import sys
# import RPi.GPIO as GPIO
from gpiozero import OutputDevice
import smbus
import math
import datetime
import pygame

pygame.mixer.init()

# set GPIO BCM mode
# GPIO.setmode(GPIO.BCM)

# class Servo:
# 
#     def __init__( self, pin, direction ):
# 
#         # set GPIO BCM mode
#         GPIO.setmode(GPIO.BCM)
# 
#         GPIO.setup( pin, GPIO.OUT )
#         self.pin = int( pin )
#         self.direction = int( direction )
#         self.servo = GPIO.PWM( self.pin, 50 )
#         self.servo.start(0.0)
# 
#     def cleanup( self ):
# 
#         self.servo.ChangeDutyCycle(self._henkan(0))
#         time.sleep(0.3)
#         self.servo.stop()
#         GPIO.cleanup()
# 
#     def currentdirection( self ):
# 
#         return self.direction
# 
#     def _henkan( self, value ):
# 
#         return 0.05 * value + 7.0
# 
#     def setdirection( self, direction, speed ):
# 
#         for d in range( self.direction, direction, int(speed) ):
#             self.servo.ChangeDutyCycle( self._henkan( d ) )
#             self.direction = d
#             time.sleep(0.1)
#             self.servo.ChangeDutyCycle( self._henkan( direction ) )
#             self.direction = direction

class Stepmotor:

    def __init__(self):

        # set GPIO BCM mode
        # GPIO.setmode(GPIO.BCM)

        # These are the pins which will be used on the Raspberry Pi
        self.pin_A = OutputDevice(5)
        self.pin_B = OutputDevice(6)
        self.pin_C = OutputDevice(13)
        self.pin_D = OutputDevice(25)
        self.interval = 0.0011

        # Declare pins as output
        # GPIO.setup(self.pin_A,GPIO.OUT)
        # GPIO.setup(self.pin_B,GPIO.OUT)
        # GPIO.setup(self.pin_C,GPIO.OUT)
        # GPIO.setup(self.pin_D,GPIO.OUT)
        # GPIO.output(self.pin_A, False)
        # GPIO.output(self.pin_B, False)
        # GPIO.output(self.pin_C, False)
        # GPIO.output(self.pin_D, False)
        self.pin_A.off()
        self.pin_B.off()
        self.pin_C.off()
        self.pin_D.off()

    def Step1(self):

        # GPIO.output(self.pin_D, True)
        self.pin_D.on()
        time.sleep(self.interval)
        # GPIO.output(self.pin_D, False)
        self.pin_D.off()

    def Step2(self):

        # GPIO.output(self.pin_D, True)
        # GPIO.output(self.pin_C, True)
        self.pin_D.on()
        self.pin_C.on()
        time.sleep(self.interval)
        # GPIO.output(self.pin_D, False)
        # GPIO.output(self.pin_C, False)
        self.pin_D.off()
        self.pin_C.off()

    def Step3(self):

        # GPIO.output(self.pin_C, True)
        self.pin_C.on()
        time.sleep(self.interval)
        # GPIO.output(self.pin_C, False)
        self.pin_C.off()

    def Step4(self):

        # GPIO.output(self.pin_B, True)
        # GPIO.output(self.pin_C, True)
        self.pin_B.on()
        self.pin_C.on()
        time.sleep(self.interval)
        # GPIO.output(self.pin_B, False)
        # GPIO.output(self.pin_C, False)
        self.pin_B.off()
        self.pin_C.off()

    def Step5(self):

        # GPIO.output(self.pin_B, True)
        self.pin_B.on()
        time.sleep(self.interval)
        # GPIO.output(self.pin_B, False)
        self.pin_B.off()

    def Step6(self):

        # GPIO.output(self.pin_A, True)
        # GPIO.output(self.pin_B, True)
        self.pin_A.on()
        self.pin_B.on()
        time.sleep(self.interval)
        # GPIO.output(self.pin_A, False)
        # GPIO.output(self.pin_B, False)
        self.pin_A.off()
        self.pin_B.off()

    def Step7(self):

        # GPIO.output(self.pin_A, True)
        self.pin_A.on()
        time.sleep(self.interval)
        # GPIO.output(self.pin_A, False)
        self.pin_A.off()

    def Step8(self):

        # GPIO.output(self.pin_D, True)
        # GPIO.output(self.pin_A, True)
        self.pin_D.on()
        self.pin_A.on()
        time.sleep(self.interval)
        # GPIO.output(self.pin_D, False)
        # GPIO.output(self.pin_A, False)
        self.pin_D.off()
        self.pin_A.off()

    def turn(self,count):
        for i in range (int(count)):
            self.Step1()
            self.Step2()
            self.Step3()
            self.Step4()
            self.Step5()
            self.Step6()
            self.Step7()
            self.Step8()

    def turnSteps(self, count):
        # Turn n steps
        # (supply with number of steps to turn)
        for i in range (count):
            self.turn(1)

    def turnDegrees(self, count):
        # Turn n degrees (small values can lead to inaccuracy)
        # (supply with degrees to turn)
        self.turn(round(count*512/360,0))

    def turnDistance(self, dist, rad):
        # Turn for translation of wheels or coil (inaccuracies involved e.g. due to thickness of rope)
        # (supply with distance to move and radius in same metric)
        self.turn(round(512*dist/(2*math.pi*rad),0))

    def close(self):
        self.pin_A.close()
        self.pin_B.close()
        self.pin_C.close()
        self.pin_D.close()

motor = Stepmotor()

def step():

    print("moving started")
    print("360 turn")
    for i in range(7):
        motor.turnDegrees(360)
    print("moving stopped")

def main():
    print("moving started")
    print("360 turn")
    for i in range(7):
        motor.turnDegrees(360)
    print("moving stopped")
    pygame.mixer.music.stop()


try:
    if __name__ == "__main__":
        number_name = 2
        pygame.mixer.music.load("/usr/share/code/project/Lucky_turntable/%s.mp3" % number_name)
        pygame.mixer.music.play()
#         pygame.mixer.music.stop()
        
        main()

        
except KeyboardInterrupt:
    motor.close()

    



