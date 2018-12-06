import utils.logging_data as LOG
import tensorflow as tf
import cv2
from tensorflow.python.platform import gfile
from utils import detect_and_align
import imutils
import os
import sys
import threading
import numpy as np
import re
import time
import datetime

'''
Tensorflow detection
This file contains a tensorflow MTCNN implementation
make sure models are reachable
code assumes from:
https://github.com/habrman/FaceRecognition
'''

#Detection
# Class that handle detection in own thread
class Detection(threading.Thread):
    pnet = None
    rnet = None
    onet = None
    model_path = None

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
    index = 0

    # Get model path
    # return path to current model or highest in model folder if not found
    def get_model_path(self):
        # get model from current file
        for root, dirs, files in os.walk("../../model/current/"):
            for file in files:
                if file.endswith(".pb"):
                    return os.path.join("../../model/current/", file)
        # get model from all model folder
        for root, dirs, files in os.walk("../../model/"):
            for file in files:
                if file.endswith(".pb"):
                    return os.path.join("../../model/", file)

        raise Exception('No model found in model/ or model/current!')

    # Initiate thread
    # parameters name, and shared_variables reference
    def __init__(self, name=None,  shared_variables = None):
        threading.Thread.__init__(self)
        self.name = name
        self.shared_variables = shared_variables
        self.sleep_time = self.SHORT_SLEEP
        self.model_path = self.get_model_path()
        self.index = int(name)
        LOG.info("Loading Tensorflow modell " + str(self.index), "SYSTEM-"+self.shared_variables.name)


    # Convert_tensorflow_box_to_OpenCV_box(box)
    # @param takes in a tensorflow box
    # @return returns a box for OpenCV
    def convert_tensorflow_box_to_openCV_box(self, box):
        return (box[0], box[1], box[2] - box[0], box[3] - box[1])

    def convert_to_dlib_landmarks(self, landmarks):
        res = []
        for i in range(5):

            x = int(landmarks[0, i])
            y = int(landmarks[0, i + 5])
            res.append([x, y])
        return res

    #Run
    #Detection function
    def run(self):
        with tf.Session() as sess:
            LOG.info("Loading Tensorflow modell " + str(self.index),"SYSTEM-"+self.shared_variables.name)

            # Load model
            self.pnet, self.rnet, self.onet = detect_and_align.create_mtcnn(sess, None)

            self.Loaded_model = True

            LOG.info("Start tf detections " + str(self.index),"SYSTEM-"+self.shared_variables.name)

            # Start Loop
            while self.shared_variables.system_running:

                self.start_time = datetime.datetime.now()

                frame = self.shared_variables.frame[self.index]

                if self.do_flipp_test:
                    frame = imutils.rotate(frame, self.flipp_test_degree*self.flipp_test_nr)

                # Do detection
                face_patches, padded_bounding_boxes, landmarks, score = detect_and_align.align_image(frame, self.pnet, self.rnet, self.onet)

                # if found faces
                if len(face_patches) > 0:

                    self.shared_variables.detection_score[self.index] = score

                    self.no_face_count = 0

                    # Save landmark
                    #self.shared_variables.landmarks[self.index] = self.convert_to_dlib_landmarks(landmarks)
                    self.shared_variables.set_landmarks(self.convert_to_dlib_landmarks(landmarks), self.index)

                    # Convert box from Tensorflow to OpenCV
                    i = 0
                    while i < len(padded_bounding_boxes):
                        face_box.append(self.convert_tensorflow_box_to_openCV_box(padded_bounding_boxes[i]))
                        i += 1

                    # Save boxes
                    self.shared_variables.face_box[self.index] = face_box

                    self.shared_variables.set_detection_box(face_box, self.index)
                    #self.shared_variables.detection_box[self.index] = face_box

                    self.shared_variables.face_found[self.index] = True

                    # Do flipp test on detection
                    if self.shared_variables.flipp_test[self.index] and self.do_flipp_test:
                            # save flipp as success
                            degree = self.shared_variables.flipp_test_degree[self.index] + self.flipp_test_nr*self.flipp_test_degree

                            degree = degree - (degree % 360)*360

                            self.shared_variables.flipp_test_degree[self.index] = degree


                            # log frame change
                            LOG.info("Flipp test successful add degree :" + str(self.flipp_test_nr*self.flipp_test_degree),self.shared_variables.name)

                            # end flipp test
                            self.do_flipp_test = False
                            self.flipp_test_nr = 1


                    # Wake tracking thread
                #    if not self.shared_variables.tracking_running:
                    #    self.sleep_time = self.SHORT_SLEEP

                else:
                    # No face
                    self.shared_variables.face_found[self.index] = False

                    # if max face misses has been done, stop tracking and do less detections
                    if self.no_face_count >= self.NO_FACE_MAX :

                        # do flipp test
                        if self.shared_variables.flipp_test[self.index]:

                            # doing flipp test
                            if self.do_flipp_test:
                                self.flipp_test_nr = self.flipp_test_nr + 1

                                # flipp test did not find anything
                                if self.flipp_test_nr*self.flipp_test_degree >= 360:
                                    self.do_flipp_test = False
                                    self.flipp_test_nr = 1

                                    #self.sleep_time = self.LONG_SLEEP
                                    #self.shared_variables.tracking_running = False
                                    #LOG.log("Initiate energy save",self.shared_variables.name)

                            else:
                                self.do_flipp_test = True

                        else:
                            #self.sleep_time = self.LONG_SLEEP
                            #self.shared_variables.tracking_running = False
                            #LOG.log("Initiate energy save",self.shared_variables.name)
                            pass
                    else:
                        self.no_face_count = self.no_face_count + 1

                    if self.no_face_count >= self.flipp_test_long_intervall and self.shared_variables.flipp_test[self.index]:
                       self.no_face_count = 0

            self.end_time = datetime.datetime.now()

            # Debug detection time
            if self.shared_variables.debug:
                LOG.debug('TF Detection time:' + str(self.end_time - self.start_time),self.shared_variables.name)

            time.sleep(self.sleep_time) # sleep if wanted
        LOG.info('Ending tf detection' + str(self.index),"SYSTEM-"+self.shared_variables.name)
