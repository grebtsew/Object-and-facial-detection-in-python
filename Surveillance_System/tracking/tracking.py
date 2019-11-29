# Tracking thread

# imports
import numpy as np
import time
from math import hypot
import math
import cv2
import sys
import threading
import datetime

# Tracking
# Class that handles tracking thread
#
class Tracking(threading.Thread):
    tracker_test = None
    tracker = None
    frame = None
    box = []
    start_time = None
    end_time = None
    first = True
    tracking_done = False
    # Initiate thread
    # parameters name , shared_variables reference
    #
    def __init__(self, name = None,  shared_variables = None, frame = None, box = []):
        threading.Thread.__init__(self)
        self.name = name
        self.shared_variables = shared_variables
        # initiate tracker
        self.box = box
        self.create_custom_tracker()
        self.running = True
        self.update_custom_tracker(frame,box)
        self.kalman = cv2.KalmanFilter(4, 2, 0)
        self.kalman.measurementMatrix = np.array([[1,0,0,0],
                                             [0,1,0,0]],np.float32)

        self.kalman.transitionMatrix = np.array([[1,0,1,0],
                                            [0,1,0,1],
                                            [0,0,1,0],
                                            [0,0,0,1]],np.float32)

        self.kalman.processNoiseCov = np.array([[1,0,0,0],
                                           [0,1,0,0],
                                           [0,0,1,0],
                                           [0,0,0,1]],np.float32) * 0.03



    # Run
    # Thread run function
    #
    def run(self):


        # tracking loop
        while self.running:
            #print(self.shared_variables.frame is not None, self.shared_variables.tracking_lock)

            if self.shared_variables.frame is not None:
                self.frame = self.shared_variables.frame
                self.object_custom_tracking()

                self.shared_variables.tracking_lock = False
            else:
                time.sleep(0.1)

    # Create_custom_tracker
    #
    # Create custom tracker, can chage tracking method here
    # will need cv2 and cv2-contrib to work!
    #
    def create_custom_tracker(self):
        self.tracker = cv2.TrackerKCF_create()

    # Update_custom_tracker
    #
    # Set and reset custom tracker
    #
    def update_custom_tracker(self, frame, box):
        self.create_custom_tracker()
        self.tracker_test = self.tracker.init( frame, box)

    # Object_Custom_tracking
    #
    # This function uses the OpenCV tracking form uncommented in update_custom_tracking
    #
    def object_custom_tracking(self):

    # Calculate
        self.tracker_test, box = self.tracker.update(self.frame)

    # Display tracker box
        if self.tracker_test:

            #print(prediction)
            #print(box)
            #print(self.box)
            #print(int(prediction[0]), int(prediction[1]))
            if self.first:
                A = self.kalman.statePost
                A[0:4] = np.array([[np.float32(box[0])], [np.float32(box[1])],[0],[0]])
                # A[4:8] = 0.0
                self.kalman.statePost = A
                self.kalman.statePre = A
                self.first = False

            current_measurement = np.array([[np.float32(box[0])], [np.float32(box[1])]])
            self.kalman.correct(current_measurement)
            prediction = self.kalman.predict()
            self.box = [int(prediction[0]), int(prediction[1]), box[2], box[3]]

            #print("track")
        else:
            #print("untrack")
            self.shared_variables.tracking_threads.remove(self)
            self.running = False
