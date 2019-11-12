# Tracking thread

# imports
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

    start_time = None
    end_time = None

    # Initiate thread
    # parameters name , shared_variables reference
    #
    def __init__(self, name = None,  shared_variables = None):
        threading.Thread.__init__(self)
        self.name = name
        self.shared_variables = shared_variables

    # Run
    # Thread run function
    #
    def run(self):

        #  wait for initial detection
        while not self.shared_variables.detection_done:
            pass

        # initiate tracker
        self.create_custom_tracker()

        # tracking loop
        while self.shared_variables.tracking_running:

            if self.shared_variables.camera_capture.isOpened():
                self.start_time = datetime.datetime.now()

                #ret_val, self.frame = self.shared_variables.camera_capture.read()
                self.frame = self.shared_variables.frame
                self.object_custom_tracking()
                self.end_time = datetime.datetime.now()

                if self.shared_variables.debug or self.shared_variables.debug_tracking:
                    LOG.log("Tracking time : " + str(self.end_time - self.start_time),self.shared_variables.name)



    # Create_custom_tracker
    #
    # Create custom tracker, can chage tracking method here
    # will need cv2 and cv2-contrib to work!
    #
    def create_custom_tracker(self):
        #higher object tracking accuracy and can tolerate slower FPS throughput
        self.tracker = cv2.TrackerCSRT_create()
        #faster FPS throughput but can handle slightly lower object tracking accuracy
        #self.tracker = cv2.TrackerKCF_create()
        #MOSSE when you need pure speed
        #self.tracker = cv2.TrackerMOSSE_create()

    # Update_custom_tracker
    #
    # Set and reset custom tracker
    #
    def update_custom_tracker(self):

        self.create_custom_tracker()

        self.tracker_test = self.tracker.init( self.frame, self.shared_variables.detection_box)

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
        if self.shared_variables.detection_done:
            self.update_custom_tracker()
            self.shared_variables.detection_done = False

    # Calculate
        self.tracker_test, face_box = self.tracker.update(self.frame)

    # Display tracker box
        if self.tracker_test:
            self.shared_variables.face_box = face_box
            self.shared_variables.tracking_box = face_box
            self.shared_variables.tracking_and_detection_frame = self.frame

         #   print ("tracked s%s" % (threading.get_ident()))
        else:
            pass
