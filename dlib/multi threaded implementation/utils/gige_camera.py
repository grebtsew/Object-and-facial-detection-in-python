import cv2
import requests
import numpy as np
import threading

def get_connected_ip():
    pass

def get_temperature_in_pos(x,y):
    pass


class gige_camera_stream(threading.Thread):
    
    def __init__(self, shared_variables = None):
        threading.Thread.__init__(self)
        self.shared_variables = shared_variables
   
    def run(self):

        pass
