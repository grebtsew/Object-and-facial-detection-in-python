# Detection thread

# imports
import utils.logging_data as LOG
import cv2
from imutils import face_utils
import dlib
from keras.models import load_model
from scipy.spatial import distance as dist
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
    pnet = None
    rnet = None
    onet = None
    landmarks_model_path = '../../model/shape_predictor_68_face_landmarks.dat'
    face_detector = None
    landmarks_predictor = None

    #face_cascade_path = 'model/haarcascade_frontalface_alt.xml'

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

    # Convert_dlib_box_to_OpenCV_box(box)
    # @param takes in a dlib box
    # @return returns a box for OpenCV
    def convert_dlib_box_to_openCV_box(self, box):
        return (int(box.left()), int(box.top()), int(box.right() - box.left()),
                         int(box.bottom() - box.top()) )



    # Object_detection
    # @ returns True if detections successful
    # @ returns False if no face found
    #
    # This function uses dlib to make a face detection.
    # Then transform the result to OpenCV
    #
    def object_detection(self):

        #image = imutils.resize(image, width=500)
       # gray = cv2.cvtColor(self.shared_variables.frame, cv2.COLOR_BGR2GRAY)

        # detect faces in the grayscale image
        box_arr = self.face_detector(self.shared_variables.frame, 1)


        # No face
        if(not len(box_arr) ):
            face_found = False
            return face_found, None, None, None

        # determine the facial landmarks for the face region
        shape = self.landmarks_predictor(self.shared_variables.frame, box_arr[0])
        landmarks = face_utils.shape_to_np(shape)

        # convert box
        face_box = self.convert_dlib_box_to_openCV_box(box_arr[0])
        face_found = True

        score = 100
        #success, face_box, landmarks, score
        return face_found, face_box, landmarks, score


    #Run
    #Detection function
    def run(self):
        if not self.Loaded_model:
            LOG.log("Loading modell",self.shared_variables.name)

                # Load model
            self.face_detector = dlib.get_frontal_face_detector()
            self.landmarks_predictor = dlib.shape_predictor(self.landmarks_model_path)

                #face_cascade = cv2.CascadeClassifier(face_cascade_path)
            self.Loaded_model = True

        LOG.log("Start detections",self.shared_variables.name)

        #wait for first cam frame
        while self.shared_variables.frame is None:
            pass

            # Start Loop
        while self.shared_variables.detection_running:
            if self.shared_variables.camera_capture.isOpened():
                self.start_time = datetime.datetime.now()

                frame = self.shared_variables.frame

                if self.do_flipp_test:
                    frame = imutils.rotate(frame, self.flipp_test_degree*self.flipp_test_nr)

                    # Do detection
                success, face_box, landmarks, score = self.object_detection()

                    # if found faces
                if success:


                    self.shared_variables.detection_score = score

                    self.no_face_count = 0

                        # Save frames
                    self.shared_variables.detection_frame = frame
                    self.shared_variables.tracking_and_detection_frame = frame

                        # Save landmark
                    self.shared_variables.landmarks = landmarks


                        # Save boxes
                    self.shared_variables.face_box = face_box
                    self.shared_variables.detection_box = face_box

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
                        LOG.log("Start detection",self.shared_variables.name)

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
