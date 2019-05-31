
'''
Helpful functions
'''

import sys
import tensorflow as tf
import cv2
import threading
import numpy as np

import argparse
from yolo import YOLO
from PIL import Image

#Detection
# Class that handle detection in own thread
class Detection(threading.Thread):
    # Thread sleep times
    sleep_time = 0.1
    LONG_SLEEP = 2
    SHORT_SLEEP = 0.5

    Loaded_model = False

    # Initiate thread
    # parameters name, and shared_variables reference
    def __init__(self, name=None,  shared_variables = None):
        threading.Thread.__init__(self)
        self.name = name
        self.shared_variables = shared_variables
        self.sleep_time = self.SHORT_SLEEP
        #self.model_path = self.get_model_path()

    def Cv2ToPil(self,frame):
        #cv2 to image
        cv2_im = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
        pil_im = Image.fromarray(cv2_im)
        return pil_im

    def PilToCv2(self,im):
        #pil to  cv2
        # PIL RGB 'im' to CV2 BGR 'imcv'
    #    imcv = np.asarray(im)[:,:,::-1].copy()
        # Or
        imcv = cv2.cvtColor(np.asarray(im), cv2.COLOR_RGB2BGR)

        # To gray image
    #    imcv = np.asarray(im.convert('L'))
        # Or
    #    imcv = cv2.cvtColor(np.asarray(im), cv2.COLOR_RGB2GRAY)
        return imcv

    def load_model(self):
        return YOLO()

    def run(self):
        yolo = self.load_model()
        try:
            while True:
                if self.shared_variables.frame is not None:
                    r_image = yolo.detect_image_faster(self.Cv2ToPil(self.shared_variables.frame))
                    self.shared_variables.detection_result = self.PilToCv2(r_image)
            yolo.close_session()
        except Exception:
            print("Detection exception!" + "\n" + str(Exception))
