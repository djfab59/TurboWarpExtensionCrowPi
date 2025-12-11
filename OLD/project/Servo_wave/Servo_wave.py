# # -*- coding: utf-8 -*-
# #!/usr/bin/env python
# import threading
# import time
# import sys
# # import RPi.GPIO as GPIO
# from gpiozero import OutputDevice, Servo, AngularServo
# import smbus
# import math
# import datetime


# # set GPIO BCM mode
# # GPIO.setmode(GPIO.BCM)

# class Servo_sensor:

#     def __init__( self, pin, direction ):

#         # set GPIO BCM mode
#         # GPIO.setmode(GPIO.BCM)

#         # GPIO.setup( pin, GPIO.OUT )
#         # self.pin = int( pin )
#         # self.servo = GPIO.PWM( self.pin, 50 )
#         # self.servo.start(0.0)
#         self.direction = int( direction )
#         # self.servo = Servo(pin)
#         self.servo = AngularServo(pin, min_angle=-90, max_angle=90)

#     def cleanup( self ):
#         self.servo.close()
#         # self.servo.ChangeDutyCycle(self._henkan(0))
#         # time.sleep(0.3)
#         # self.servo.stop()
#         # GPIO.cleanup()

#     def currentdirection( self ):

#         return self.direction

#     def _henkan( self, value ):

#         return 0.05 * value + 7.0

#     def setdirection( self, direction, speed ):

#         for d in range( self.direction, direction, int(speed) ):
#             self.servo.ChangeDutyCycle( self._henkan( d ) )
#             self.direction = d
#             time.sleep(0.1)
#             self.servo.ChangeDutyCycle( self._henkan( direction ) )
#             self.direction = direction


# # def moveServo():

# #     servo_pin = 19
# #     s = Servo_sensor(servo_pin,0)
# #     for i in range(14):
# #         print("Turn left ...")
# #         s.setdirection( 100, 80 )
# #         #10
# #         time.sleep(1)
# #         print("Turn right ...")
# #         s.setdirection( -100, -80 )
# #         time.sleep(1)
# #     s.cleanup()


# # def main():


# #     moveServo()


# try:
#     servo_pin = 19
#     s = Servo_sensor(servo_pin,0)
#     for i in range(14):
#         print("Turn left ...")
#         s.setdirection( 100, 80 )
#         #10
#         time.sleep(1)
#         print("Turn right ...")
#         s.setdirection( -100, -80 )
#         time.sleep(1)
#     s.cleanup()
        
# except KeyboardInterrupt:
# #     s = Servo(a,0)
#     s.cleanup()
    



from gpiozero import Servo
import time

servo = Servo(19)
while True:
    servo.min()
    time.sleep(1)
    servo.mid()
    time.sleep(1)
    servo.max()
    time.sleep(1)