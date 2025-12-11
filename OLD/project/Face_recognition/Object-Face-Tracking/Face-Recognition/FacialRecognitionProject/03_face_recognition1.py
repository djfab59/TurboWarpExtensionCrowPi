''''
Real Time Face Recogition
    ==> Each face stored on dataset/ dir, should have a unique numeric integer ID as 1, 2, 3, etc                       
    ==> LBPH computed model (trained faces) should be on trainer/ dir
Based on original code by Anirban Kar: https://github.com/thecodacus/Face-Recognition    

Developed by Marcelo Rovai - MJRoBot.org @ 21Feb18  

'''

import cv2
import numpy as np
import os
import threading
import time
from rpi_ws281x import PixelStrip, Color
import RPi.GPIO as GPIO

count = 0
class RGB_Matrix:

    def __init__(self):

        # LED strip configuration:
        self.LED_COUNT = 64        # Number of LED pixels.
        self.LED_PIN = 12          # GPIO pin connected to the pixels (18 uses PWM!).
        self.LED_FREQ_HZ = 800000  # LED signal frequency in hertz (usually 800khz)
        self.LED_DMA = 10          # DMA channel to use for generating signal (try 10)
        self.LED_BRIGHTNESS = 10  # Set to 0 for darkest and 255 for brightest
        self.LED_INVERT = False    # True to invert the signal (when using NPN transistor level shift)
        self.LED_CHANNEL = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53

        self.RIGHT_BORDER = [7,15,23,31,39,47,55,63]
        self.LEFT_BORDER = [0,8,16,24,32,40,48,56]

    # Define functions which animate LEDs in various ways.
    def clean(self,strip):
        # wipe all the LED's at once
        for i in range(strip.numPixels()):
            strip.setPixelColor(i, Color(0, 0, 0))
        strip.show()
    def clean_up(self,strip):
	clean = []
	for pixel in clean:
            strip.setPixelColor(pixel, Color(0,0,0))
	strip.show()
    def run_clean(self):
         # Create NeoPixel object with appropriate configuration.
         strip = PixelStrip(self.LED_COUNT, self.LED_PIN, self.LED_FREQ_HZ, self.LED_DMA, self.LED_INVERT, self.LED_BRIGHTNESS, self.LED_CHANNEL)
         # Intialize the library (must be called once before other functions).
         strip.begin()
         # do stuff
         try:
             print('test animations.')
             self.clean_up(strip)
         except KeyboardInterrupt:
             # clean the matrix LED before interruption
             self.clean(strip)



    def demo_happy(self,strip):

        happy_smiley = [2,3,4,5,9,14,16,18,21,23,24,31,32,34,37,39,40,42,43,44,45,47,49,54,58,59,60,61]

	# show the happy smiley on the RGB screen
        for pixel in happy_smiley:
            strip.setPixelColor(pixel, Color(255,255,255))

        strip.show()
#        time.sleep(2.5)
        #self.clean(strip)



    def demo_sad(self,strip):

        sad_smiley = [2,3,4,5,9,14,16,18,21,23,24,31,32,34,35,36,37,39,40,42,45,47,49,54,58,59,60,61]



        # show the sad smiley on the RGB screen
        for pixel in sad_smiley:
            strip.setPixelColor(pixel, Color(255,0,0))

        strip.show()
 #       time.sleep(2.5)
        #self.clean(strip)

    def run_happy(self):
         # Create NeoPixel object with appropriate configuration.
         strip = PixelStrip(self.LED_COUNT, self.LED_PIN, self.LED_FREQ_HZ, self.LED_DMA, self.LED_INVERT, self.LED_BRIGHTNESS, self.LED_CHANNEL)
         # Intialize the library (must be called once before other functions).
         strip.begin()
         # do stuff
         try:
             print('test animations.')
             self.demo_happy(strip)
         except KeyboardInterrupt:
             # clean the matrix LED before interruption
             self.clean(strip)
    def run_sad(self):
         # Create NeoPixel object with appropriate configuration.
         strip = PixelStrip(self.LED_COUNT, self.LED_PIN, self.LED_FREQ_HZ, self.LED_DMA, self.LED_INVERT, self.LED_BRIGHTNESS, self.LED_CHANNEL)
         # Intialize the library (must be called once before other functions).
         strip.begin()
         # do stuff
         try:
             print('test animations.')
             self.demo_sad(strip)
         except KeyboardInterrupt:
             # clean the matrix LED before interruption
             self.clean(strip)


matrix = RGB_Matrix()

recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read('trainer/trainer.yml')
cascadePath = "haarcascade_frontalface_default.xml"
faceCascade = cv2.CascadeClassifier(cascadePath);

font = cv2.FONT_HERSHEY_SIMPLEX
#font = cv2.

#iniciate id counter
id = 1

# names related to ids: example ==> Marcelo: id=1,  etc
names = ['None', 'Tony', 'wilson', 'Tony', 'Z', 'W'] 

# Initialize and start realtime video capture
cam = cv2.VideoCapture(0)
cam.set(3, 800) # set video widht
#640
cam.set(4, 640) # set video height
#480

# Define min window size to be recognized as a face
minW = 0.1*cam.get(3)
#3
minH = 0.1*cam.get(4)
#4

try:
  while True:

    ret, img =cam.read()
    #img = cv2.flip(img, -1) # Flip vertically

    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

    faces = faceCascade.detectMultiScale( 
        gray,
        scaleFactor = 1.2,
        minNeighbors = 5,
        minSize = (int(minW), int(minH)),
       )

    for(x,y,w,h) in faces:

        cv2.rectangle(img, (x,y), (x+w,y+h), (0,255,0), 2)

        id, confidence = recognizer.predict(gray[y:y+h,x:x+w])
        # Check if confidence is less them 100 ==> "0" is perfect match 
        if (confidence < 51):
	    t3 = threading.Thread(target = matrix.run_clean)
	    t3.start()
	    #t1 = threading.Thread(target = matrix.run_happy)
	    #t1.start()
	    cv2.rectangle(img, (x,y), (x+w,y+h), (0,255,0), 2)
            id = names[id]
            confidence = "  {0}%".format(round(100 - confidence))
	    cv2.putText(img, str(id), (x+5,y-5), font, 1, (0,255,0), 2)
	    #os.system("~/Desktop/AI-succed-gif")
	    print("\n Successful")
	    #cv2.imshow('camera',img) 
	    count = count + 1
	    if count > 10:
                cam.release()
                cv2.destroyAllWindows()
                os.system("/home/pi/Desktop/AI-succeed-gif")
		t1 = threading.Thread(target = matrix.run_happy)
                t1.start()
	        #GPIO.cleanup()
		time.sleep(3)
	        matrix.run_clean()

        else:
	    count = 0
	    t2 = threading.Thread(target = matrix.run_sad)
	    t2.start()
	    cv2.rectangle(img, (x,y), (x+w,y+h), (0,0,255), 2)
            id = "unknown"
            confidence = "  {0}%".format(round(100 - confidence))
            cv2.putText(img, str(id), (x+5,y-5), font, 1, (0,0,255), 2)
       # cv2.putText(img, str(id), (x+5,y-5), font, 1, (255,255,255), 2)
        cv2.putText(img, str(confidence), (x+5,y+h-5), font, 1, (255,255,0), 1)  
    
    cv2.imshow('camera',img) 

    k = cv2.waitKey(10) & 0xff # Press 'ESC' for exiting video
    if k == 27:
        break

  # Do a bit of cleanup
  print("\n [INFO] Exiting Program and cleanup stuff")
  cam.release()
  cv2.destroyAllWindows()
except KeyboardInterrupt:
  GPIO.cleanup()
  matrix.run_clean()
  



