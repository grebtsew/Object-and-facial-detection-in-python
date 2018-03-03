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


class Detection(threading.Thread):

    pnet = None
    rnet = None
    onet = None
    model_path = 'model/20170512-110547.pb'
    sleep_time = 0
    
    def __init__(self, name=None,  shared_variables = None):
        threading.Thread.__init__(self)
        self.name = name
        self.shared_variables = shared_variables
       
        
    # Convert_tensorflow_box_to_OpenCV_box(box)
    # @param takes in a tensorflow box
    # @return returns a box for OpenCV
    def convert_tensorflow_box_to_openCV_box(self, box):
        return (box[0], box[1], box[2] - box[0], box[3] - box[1])


    def run(self):
        with tf.Session() as sess:

            LOG.log("Loading modell","SYSTEM")
      
            self.pnet, self.rnet, self.onet = detect_and_align.create_mtcnn(sess, None)
            model_exp = os.path.expanduser(self.model_path)
            if (os.path.isfile(model_exp)):
                with gfile.FastGFile(model_exp, 'rb') as f:
                    graph_def = tf.GraphDef()
                    graph_def.ParseFromString(f.read())
                    tf.import_graph_def(graph_def, name='')
             
            images_placeholder = tf.get_default_graph().get_tensor_by_name("input:0")
            embeddings = tf.get_default_graph().get_tensor_by_name("embeddings:0")
            phase_train_placeholder = tf.get_default_graph().get_tensor_by_name("phase_train:0")            
         
        # set up tensorflow model
        #load_model(model_path)

            LOG.log("Start detektions","SYSTEM")
        
            while self.shared_variables.running:
                              
            #print('Detection')
           # print (self.shared_variables.name)
                if self.shared_variables.camera_capture.isOpened():
                    ret_val, frame = self.shared_variables.camera_capture.read()
    
                # Do detection
                    face_patches, padded_bounding_boxes, landmarks = detect_and_align.align_image(frame, self.pnet, self.rnet, self.onet)

                # if found faces
                    if len(face_patches) > 0:
                        face_patches = np.stack(face_patches)
                        feed_dict = {images_placeholder: face_patches, phase_train_placeholder: False}
       
                        embs = sess.run(embeddings, feed_dict=feed_dict)

                    
                        # Convert box to OpenCV
                        self.shared_variables.landmarks = landmarks

                        face_box = self.convert_tensorflow_box_to_openCV_box(padded_bounding_boxes[0])
                        
                        self.shared_variables.face_box = face_box
                        self.shared_variables.detection_box = face_box
                        

                       # print (face_box) 
                     
                        self.shared_variables.face_found = True
                        self.shared_variables.detection_done = True
        

                    else:
                        # No face
                        self.shared_variables.face_found = False
    

                time.sleep(self.sleep_time) # sleep if wanted   
