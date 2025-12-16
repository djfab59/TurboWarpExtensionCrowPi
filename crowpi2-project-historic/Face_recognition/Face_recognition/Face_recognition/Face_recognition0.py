''''
Capture multiple Faces from multiple users to be stored on a DataBase (dataset directory)
    ==> Faces will be stored on a directory: dataset/ (if does not exist, pls create one)
    ==> Each face will have a unique numeric integer ID as 1, 2, 3, etc                       

Based on original code by Anirban Kar: https://github.com/thecodacus/Face-Recognition    

Developed by Marcelo Rovai - MJRoBot.org @ 21Feb18    

'''

import cv2
import os
import time



cam = cv2.VideoCapture(0)
cam.set(3, 1000) # set video width
cam.set(4, 750) # set video height

face_detector = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

# For each person, enter one numeric face id
face_id = 1
#input('\n enter user id end press <return> ==>  ')

#print("\n**************************************************************************")
#print("")
print("Initializing face capture. Point your face at the camera, look the camera and wait about 10 seconds...")
#print("")
#print("**************************************************************************\n")
#print("")
time.sleep(2)
# Initialize individual sampling face count
count = 0

font = cv2.FONT_HERSHEY_SIMPLEX
while(True):

    ret, img = cam.read()
    # img = cv2.flip(img, -1) # flip video image vertically
    # print('ret', ret)
    # print('img', img)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_detector.detectMultiScale(gray, 1.3, 5)
    
    message1 = "Capturing..."
    #message2 = "camera and wait about 10 seconds..."
    #cv2.putText(img, message1, (15,30), font, 1, (255,255,255), 2)
   # cv2.putText(img, message2, (15,60), font, 1, (255,255,255), 2)
    for (x,y,w,h) in faces:

        cv2.rectangle(img, (x,y), (x+w,y+h), (255,0,0), 2)
        count += 1

        # Save the captured image into the datasets folder
        cv2.namedWindow("image", cv2.WINDOW_NORMAL)
        cv2.imwrite("dataset/User." + str(face_id) + '.' + str(count) + ".jpg", gray[y:y+h,x:x+w])
        cv2.moveWindow("image",1100,250)
        cv2.putText(img, message1, (x+5,y-5), font, 1, (255,255,255), 2)
        

        cv2.imshow('image', img)
    

    k = cv2.waitKey(100) & 0xff # Press 'ESC' for exiting video
    if k == 27:
        break
    elif count >= 30: # Take 30 face sample and stop video
         break

# Do a bit of cleanup
#print("\n**************************************************************************")
#print("")
print("Successful capture, exiting Program and cleanup stuff")
print("")
#print("**************************************************************************\n")
cam.release()
cv2.destroyAllWindows()
os.system("sudo python 02_face_training.py")
os.system("sudo python 03_face_recognition1.py")

