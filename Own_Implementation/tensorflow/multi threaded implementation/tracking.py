# Detection thread

# imports

# import own
import utils.logging_data as LOG
from math import hypot
import math
import cv2

import sys
import threading


class Tracking(threading.Thread):
    tracker_test = None
    tracker = None
    frame = None
    old_detection_box = None
    
    def __init__(self, name = None,  shared_variables = None):
        threading.Thread.__init__(self)
        self.name = name
        self.shared_variables = shared_variables
        
       

    def run(self):
        #  wait for initial detection
        while not self.shared_variables.detection_done:
            pass
        
        # initiate tracker
        self.create_custom_tracker()
        
        while self.shared_variables.running:
           # print('tracking')
           # print (self.shared_variables.name)
            if self.shared_variables.camera_capture.isOpened():
                ret_val, self.frame = self.shared_variables.camera_capture.read()

                self.object_custom_tracking()

      

    # Create_custom_tracker
    #
    # Create custom tracker
    #
    def create_custom_tracker(self):
        self.tracker = cv2.TrackerBoosting_create()
        #self.tracker = cv2.TrackerMIL_create()
        #self.tracker = cv2.TrackerKCF_create()
        #self.tracker = cv2.TrackerTLD_create()
        #self.tracker = cv2.TrackerMedianFlow_create()

    # Update_custom_tracker
    #
    # Set and reset custom tracker
    #
    def update_custom_tracker(self):
        
        self.create_custom_tracker()
        self.tracker_test = self.tracker.init( self.frame, self.shared_variables.detection_box)

    def distance_between_boxes(self, box1, box2):
        print (int(abs(math.hypot(box2[0]-box1[0], box2[1]-box1[1]))))
        return int(abs(math.hypot(box2[0]-box1[0], box2[1]-box1[1])))

    # Object_Custom_tracking
    #
    # This function uses the OpenCV tracking form uncommented in update_custom_tracking
    #
    def object_custom_tracking(self):
        #print("Tracking")

    
    # See if detection is done
        if self.shared_variables.detection_done:
            self.update_custom_tracker()
            self.shared_variables.detection_done = False         

    # Calculate

        self.tracker_test, face_box = self.tracker.update(self.frame) 

    # Display tracker box
        if self.tracker_test:
            self.shared_variables.face_box = face_box
            self.shared_variables.tracking_box = face_box
            self.old_detection_box = face_box


            
        # Tracking success
        #    topLeft = (int(face_box[0]), int(face_box[1]))
        #    bottomRight = (int(face_box[0] + face_box[2]), int(face_box[1] + face_box[3]))
        #    cv2.rectangle(frame, topLeft,bottomRight, (255,0,0), 2,1 )
        

