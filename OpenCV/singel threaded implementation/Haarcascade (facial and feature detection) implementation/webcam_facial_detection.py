import numpy as np
import cv2

# Models are from http://alereimondo.no-ip.org/OpenCV/34/
# Check it out, there are plenty of them!
# Useful and fast

'''
If you wanna train your own models check this out!
https://docs.opencv.org/3.4/dc/d88/tutorial_traincascade.html
'''

# Code from https://docs.opencv.org/3.4/d7/d8b/tutorial_py_face_detection.html

face_cascade = cv2.CascadeClassifier('./haarcascade_frontalface_default.xml')

facial_features_cascade = cv2.CascadeClassifier('./haarcascade_facial_features.xml')


cap = cv2.VideoCapture(0)

# endless loop of detections
while True:

    ret, img = cap.read()

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    for (x,y,w,h) in faces:
        cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
        roi_gray = gray[y:y+h, x:x+w]
        roi_color = img[y:y+h, x:x+w]

        facials = facial_features_cascade.detectMultiScale(roi_gray)

        for (ex,ey,ew,eh) in facials:
            cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,100,0),2)


    cv2.imshow('img',img)
    cv2.waitKey(1)

cv2.destroyAllWindows()
