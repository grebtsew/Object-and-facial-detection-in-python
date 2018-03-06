# Detection thread

# imports
import utils.logging_data as LOG
import tensorflow as tf
import cv2

from tensorflow.python.platform import gfile
from utils import detect_and_align

import os
import sys
import threading
import numpy as np
import re
import time

#Detection
# Class that handle detection in own thread
class Detection(threading.Thread):
    pnet = None
    rnet = None
    onet = None
    model_path = 'model/20170512-110547.pb'

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
       
        
    # Convert_tensorflow_box_to_OpenCV_box(box)
    # @param takes in a tensorflow box
    # @return returns a box for OpenCV
    def convert_tensorflow_box_to_openCV_box(self, box):
        return (box[0], box[1], box[2] - box[0], box[3] - box[1])

    #Run
    #Detection function
    def run(self):
        with tf.Session() as sess:
            if not self.Loaded_model:
                LOG.log("Loading modell",self.shared_variables.name)

                # Load model
                self.pnet, self.rnet, self.onet = detect_and_align.create_mtcnn(sess, None)
                model_exp = os.path.expanduser(self.model_path)
                if (os.path.isfile(model_exp)):
                    with gfile.FastGFile(model_exp, 'rb') as f:
                        graph_def = tf.GraphDef()
                        graph_def.ParseFromString(f.read())
                        tf.import_graph_def(graph_def, name='')

                # Training references     
                images_placeholder = tf.get_default_graph().get_tensor_by_name("input:0")
                embeddings = tf.get_default_graph().get_tensor_by_name("embeddings:0")
                phase_train_placeholder = tf.get_default_graph().get_tensor_by_name("phase_train:0")
                self.Loaded_model = True
        
            LOG.log("Start detections",self.shared_variables.name)

            # Start Loop
            while self.shared_variables.detection_running:
                
                if self.shared_variables.camera_capture.isOpened():
                   # ret_val, frame = self.shared_variables.camera_capture.read()
                    frame = self.shared_variables.frame
                    # Do detection
                    face_patches, padded_bounding_boxes, landmarks = detect_and_align.align_image(frame, self.pnet, self.rnet, self.onet)

                    # if found faces
                    if len(face_patches) > 0:

                        # Session
                        face_patches = np.stack(face_patches)
                        feed_dict = {images_placeholder: face_patches, phase_train_placeholder: False}
                        embs = sess.run(embeddings, feed_dict=feed_dict)

                        self.no_face_count = 0

                        # Save frames
                        self.shared_variables.detection_frame = frame
                        self.shared_variables.tracking_and_detection_frame = frame

                        # Save landmark
                        self.shared_variables.landmarks = landmarks
                        
                        # Convert box from Tensorflow to OpenCV
                        face_box = self.convert_tensorflow_box_to_openCV_box(padded_bounding_boxes[0])

                        # Save boxes
                        self.shared_variables.face_box = face_box
                        self.shared_variables.detection_box = face_box
                        
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
                            self.sleep_time = self.LONG_SLEEP
                            self.shared_variables.tracking_running = False
                            LOG.log("Initiate energy save",self.shared_variables.name)
                        else:
                            self.no_face_count = self.no_face_count + 1

                
                time.sleep(self.sleep_time) # sleep if wanted   
