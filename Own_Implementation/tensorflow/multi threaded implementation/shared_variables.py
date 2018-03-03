# system
import sys
import threading

# camera
import cv2

# global shared variables
class Shared_Variables():
    face_box = None
    detection_box = None
    tracking_box = None
    face_found = None
    detection_done = False
    running = True
    landmarks = None

    def __init__(self, name=None, camera_capture = None):
        threading.Thread.__init__(self)
        self.name = name
        self.camera_capture = camera_capture
