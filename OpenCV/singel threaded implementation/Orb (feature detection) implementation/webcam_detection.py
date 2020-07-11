import numpy as np
import cv2
from matplotlib import pyplot as plt

cap = cv2.VideoCapture(0)
# Initiate STAR detector
orb = cv2.ORB_create()

while True:
    ret, frame = cap.read()

    # find the keypoints with ORB

    kp = orb.detect(frame)

    # compute the descriptors with ORB
    kp, des = orb.compute(frame, kp)

    # draw only keypoints location,not size and orientation
    img2 = cv2.drawKeypoints(frame,kp,outImage = None, color=(0,255,0), flags=0)
    
    cv2.imshow("orb", img2)
    cv2.waitKey(1)
    