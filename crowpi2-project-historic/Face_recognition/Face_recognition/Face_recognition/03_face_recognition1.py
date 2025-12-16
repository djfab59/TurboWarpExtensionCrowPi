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
import re

from elecrow_ws281x import *

count = 0
class RGB_Matrix:

    def __init__(self):

        self.strip = PixelStrip(64, 10)
        self.strip.begin()

        self.RIGHT_BORDER = [7,15,23,31,39,47,55,63]
        self.LEFT_BORDER = [0,8,16,24,32,40,48,56]

    # Define functions which animate LEDs in various ways.
    def clean(self,strip):
        # wipe all the LED's at once
        strip.clear()

    def run_clean(self):
        # # Create NeoPixel object with appropriate configuration.
        self.clean(self.strip)



    def demo_happy(self,strip):
        happy_smiley = [2,3,4,5,9,14,16,18,21,23,24,31,32,34,37,39,40,42,43,44,45,47,49,54,58,59,60,61]
	    # show the happy smiley on the RGB screen
        self.strip.sendPos2Show(happy_smiley, 0, 255, 0)

    def demo_sad(self,strip):
        sad_smiley = [2,3,4,5,9,14,16,18,21,23,24,31,32,34,35,36,37,39,40,42,45,47,49,54,58,59,60,61]
        # show the sad smiley on the RGB screen
        self.strip.sendPos2Show(sad_smiley, 0, 255, 0)


    def run_happy(self):
        try:
            self.demo_happy(self.strip)
        except KeyboardInterrupt:
            # clean the matrix LED before interruption
            self.clean(self.strip)

    def run_sad(self):
        try:
            #print('test animations.')
            self.demo_sad(self.strip)
        except KeyboardInterrupt:
            # clean the matrix LED before interruption
            self.clean(self.strip)


matrix = RGB_Matrix()

recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read('trainer/trainer.yml')
cascadePath = "haarcascade_frontalface_default.xml"
# cascadePath = "haarcascade_frontalcatface.xml"
faceCascade = cv2.CascadeClassifier(cascadePath);

font = cv2.FONT_HERSHEY_SIMPLEX
#font = cv2.

#iniciate id counter
id = 1

# names related to ids: example ==> Marcelo: id=1,  etc
names = ['None', 'Customer', 'z', 'Tony', 'Z', 'W'] 

# Initialize and start realtime video capture
cam = cv2.VideoCapture(0)
cam.set(3, 1000) # set video widht
#640
cam.set(4, 750) # set video height
#480

# Define min window size to be recognized as a face
minW = 0.1*cam.get(3)
#3
minH = 0.1*cam.get(4)
#4

global successOneTime

successOneTime = False

try:
    time.sleep(1.5)
    print("\nPlease look at the camera to start testing...")
    time.sleep(1.5)
    cv2.namedWindow("image", cv2.WINDOW_NORMAL)
  
    while not successOneTime:
    
        ret, img =cam.read()
        #img = cv2.flip(img, -1) # Flip vertically
        gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

        faces = faceCascade.detectMultiScale( 
            gray,
            scaleFactor = 1.1,
            minNeighbors = 4,
            minSize = (int(minW), int(minH)),
        )

        for(x,y,w,h) in faces:

            cv2.rectangle(img, (x,y), (x+w,y+h), (0,255,0), 2)


            id, confidence = recognizer.predict(gray[y:y+h,x:x+w])
            # Check if confidence is less them 100 ==> "0" is perfect match 
            if (confidence < 50):
                t3 = threading.Thread(target = matrix.run_clean)
                t3.start()
                #t1 = threading.Thread(target = matrix.run_happy)
                #t1.start()
                cv2.rectangle(img, (x,y), (x+w,y+h), (0,255,0), 2)
                id = names[id]
                confidence = "  {0}%".format(round(100 - int(re.search(r'\d+', str(confidence)).group())))
                cv2.putText(img, str(id), (x+5,y-5), font, 1, (0,255,0), 2)
                count = count + 1
                if count > 15:
                    print("\nSuccessful! Welcome %s!"%id)
                    cam.release()
                    cv2.destroyAllWindows()
                    # os.system("/usr/share/code/project/Face_recognition/Face_recognition/Face_recognition/AI-succeed-gif")
                    t1 = threading.Thread(target = matrix.run_happy)
                    t1.start()
                    time.sleep(3)
                    matrix.run_clean()
                    successOneTime = True

            else:
                count = 0
                t2 = threading.Thread(target = matrix.run_sad)
                t2.start()
                cv2.rectangle(img, (x,y), (x+w,y+h), (0,0,255), 2)
                id = "unknown"
                confidence = "  {0}%".format(round(100 - int(100 - int(re.search(r'\d+', str(confidence)).group()))))
                # cv2.putText(img, str(id), (x+5,y-5), font, 1, (0,0,255), 2)
        # cv2.putText(img, str(id), (x+5,y-5), font, 1, (255,255,255), 2)
        # cv2.putText(img, str(confidence), (x+5,y+h-5), font, 1, (0,0,255), 1) 
        cv2.namedWindow("camera", cv2.WINDOW_NORMAL)
        cv2.moveWindow("camera",1100,250)
        cv2.imshow('camera',img)
        
    #    print("1")

        k = cv2.waitKey(10) & 0xff # Press 'ESC' for exiting video
        if k == 27:
            matrix.run_clean()
            break



    # Do a bit of cleanup
    print("Exiting Program and cleanup stuff")
    cam.release()
    cv2.destroyWindow('camera')
    cv2.destroyAllWindows()
    
except KeyboardInterrupt:
    matrix.run_clean()
  



