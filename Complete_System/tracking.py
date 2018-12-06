
import utils.logging_data as LOG
import math
import cv2
import sys
import threading
import datetime

'''
This file contains code for tracking objects from detection thread
Takes a box and an image
Can change type of tracker, see below
'''

# Tracking
# Class that handles tracking thread
#
class Tracking(threading.Thread):
    tracker_test = None
    tracker = None
    frame = None

    UPDATE_TIME = 25
    update_timer = 0

    start_time = None
    end_time = None
    index = 0

    # Initiate thread
    # parameters name , shared_variables reference
    #
    def __init__(self, name = None,  shared_variables = None, index = 0 ):
        threading.Thread.__init__(self)
        self.name = name
        self.shared_variables = shared_variables
        self.index = index
        LOG.info("Start tracking " + str(self.index), "SYSTEM-"+self.shared_variables.name)

    # Run
    # Thread run function
    #
    def run(self):

        #  wait for initial detection
        while self.shared_variables.detection_box[self.index] is None:
            pass

        # initiate tracker
        self.create_custom_tracker()

        # tracking loop
        while self.shared_variables.system_running:

            self.start_time = datetime.datetime.now()

            self.frame = self.shared_variables.frame[self.index]
            self.object_custom_tracking()
            self.end_time = datetime.datetime.now()

            if self.shared_variables.debug :
                LOG.debug("Tracking time : " + str(self.end_time - self.start_time),"SYSTEM-"+self.shared_variables.name)

        LOG.info("Stopped tracking "+str(self.index), "SYSTEM-"+self.shared_variables.name)


    # Create_custom_tracker
    #
    # Create custom tracker, can chage tracking method here
    # will need cv2 and cv2-contrib to work!
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

        if len(self.shared_variables.detection_box[self.index]) > 0:
            self.tracker_test = self.tracker.init( self.frame, tuple(self.shared_variables.detection_box[self.index][0]))
        else:
            self.tracker_test = False

    def distance_between_boxes(self, box1, box2):
        #print (int(abs(math.hypot(box2[0]-box1[0], box2[1]-box1[1]))))
        return int(abs(math.hypot(box2[0]-box1[0], box2[1]-box1[1])))

    # Object_Custom_tracking
    #
    # This function uses the OpenCV tracking form uncommented in update_custom_tracking
    #
    def object_custom_tracking(self):
       # print("Tracking")


    # See if detection is done
        if self.shared_variables.face_found[self.index] and self.update_timer > self.UPDATE_TIME:
            self.update_custom_tracker()
            self.update_timer = 0

        # When to check for new detections
        self.update_timer += 1

    # Calculate
        self.tracker_test, face_box = self.tracker.update(self.frame)

    # Display tracker box
        if self.tracker_test:
            self.shared_variables.tracking_box[self.index] = face_box

        else:
            pass
