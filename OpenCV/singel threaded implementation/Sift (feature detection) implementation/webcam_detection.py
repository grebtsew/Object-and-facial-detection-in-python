import numpy as np
import cv2

'''
Scale-Invariant Feature Transform is a feature detection algorithm in computer vision to detect and describe local features in images.

Source :
https://docs.opencv.org/3.4/da/df5/tutorial_py_sift_intro.html
'''

cap = cv2.VideoCapture(0)

# endless loop of detections
while True:

    ret, img = cap.read()

    gray= cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    sift = cv2.xfeatures2d.SIFT_create()
    kp = sift.detect(gray,None)
    img=cv2.drawKeypoints(gray,kp,img)

    cv2.imshow('img',img)
    cv2.waitKey(1)

cv2.destroyAllWindows()
