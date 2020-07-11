# Detection thread

# Models are from http://alereimondo.no-ip.org/OpenCV/34/
# Check it out, there are plenty of them!
# Useful and fast

'''
If you wanna train your own models check this out!
https://docs.opencv.org/3.4/dc/d88/tutorial_traincascade.html
'''

# Code from https://docs.opencv.org/3.4/d7/d8b/tutorial_py_face_detection.html

# imports
import logging_data as LOG
import cv2

import imutils
import os
import sys
import threading
import numpy as np
import re
import time
import datetime

#Detection
# Class that handle detection in own thread
class Detection(threading.Thread):

    face_cascade = []
    facial_features_cascade = []

    # Flipp testing camera
    flipp_test_nr = 1
    flipp_test_degree = 90
    do_flipp_test = False
    flipp_test_long_intervall = 12

    # Calculate time
    start_time = None
    end_time = None

    # Thread sleep times
    sleep_time = 0.1
    LONG_SLEEP = 2
    SHORT_SLEEP = 0.5

    # Number of detection fails to start energy save
    no_face_count = 0
    NO_FACE_MAX = 10
    Loaded_model = False

    # Initiate thread
    # parameters name, and shared_variables reference
    def __init__(self, name=None,  shared_variables = None):
        threading.Thread.__init__(self)
        self.name = name
        self.shared_variables = shared_variables
        self.sleep_time = self.SHORT_SLEEP


    #Run
    #Detection function
    def run(self):
        # Load model
        LOG.log("Loading modell",self.shared_variables.name)

        face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
        facial_features_cascade = cv2.CascadeClassifier('haarcascade_facial_features.xml')
        
        LOG.log("Start detections",self.shared_variables.name)

        # Start Loop
        while self.shared_variables.detection_running:

            if self.shared_variables.camera_capture.isOpened():
                self.start_time = datetime.datetime.now()

               # ret_val, frame = self.shared_variables.camera_capture.read()
                frame = self.shared_variables.frame

                if self.do_flipp_test:
                    frame = imutils.rotate(frame, self.flipp_test_degree*self.flipp_test_nr)

                # Do detection
                if frame is not None :
                    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

                    landmarksAndFaces = []


                    face_patches = face_cascade.detectMultiScale(gray, 1.3, 5)

                    for (x,y,w,h) in face_patches:

                        roi_gray = gray[y:y+h, x:x+w]

                        # To dont use landmarks, instead use boxes
                        for (ex,ey,ew,eh) in facial_features_cascade.detectMultiScale(roi_gray):
                             landmarksAndFaces.append( [x + ex,  y + ey, ew, eh] )

                        landmarksAndFaces.append(face_patches[0].tolist())

                    # if found faces
                    if len(face_patches) > 0:

                        self.no_face_count = 0

                        self.shared_variables.face_found = True

                        # Save frames
                        self.shared_variables.detection_frame = frame
                        self.shared_variables.tracking_and_detection_frame = frame



                        # Save boxes
                        self.shared_variables.face_box = landmarksAndFaces
                        self.shared_variables.detection_box = landmarksAndFaces

                        # Do flipp test on detection
                        if self.shared_variables.flipp_test and self.do_flipp_test:
                                # save flipp as success
                                degree = self.shared_variables.flipp_test_degree + self.flipp_test_nr*self.flipp_test_degree

                                degree = degree - (degree % 360)*360

                                self.shared_variables.flipp_test_degree = degree


                                # log frame change
                                LOG.log("Flipp test successful add degree :" + str(self.flipp_test_nr*self.flipp_test_degree),self.shared_variables.name)

                                # end flipp test
                                self.do_flipp_test = False
                                self.flipp_test_nr = 1


                        # Wake tracking thread
                        if not self.shared_variables.tracking_running:
                            self.sleep_time = self.SHORT_SLEEP
                            self.shared_variables.start_tracking_thread()

                    else:
                        # No face
                        self.shared_variables.face_found = False

                        # if max face misses has been done, stop tracking and do less detections
                        if self.no_face_count >= self.NO_FACE_MAX and self.shared_variables.tracking_running:

                            # do flipp test
                            if self.shared_variables.flipp_test:

                                # doing flipp test
                                if self.do_flipp_test:
                                    self.flipp_test_nr = self.flipp_test_nr + 1

                                    # flipp test did not find anything
                                    if self.flipp_test_nr*self.flipp_test_degree >= 360:
                                        self.do_flipp_test = False
                                        self.flipp_test_nr = 1

                                        self.sleep_time = self.LONG_SLEEP
                                        self.shared_variables.tracking_running = False
                                        LOG.log("Initiate energy save",self.shared_variables.name)

                                else:
                                    self.do_flipp_test = True

                            else:
                                self.sleep_time = self.LONG_SLEEP
                                self.shared_variables.tracking_running = False
                                LOG.log("Initiate energy save",self.shared_variables.name)

                        else:
                            self.no_face_count = self.no_face_count + 1

                        if self.no_face_count >= self.flipp_test_long_intervall and self.shared_variables.flipp_test:
                           self.no_face_count = 0

                self.end_time = datetime.datetime.now()

                # Debug detection time
                if self.shared_variables.debug_detection or self.shared_variables.debug:
                    LOG.log('Detection time:' + str(self.end_time - self.start_time),self.shared_variables.name)

                    time.sleep(self.sleep_time) # sleep if wanted
