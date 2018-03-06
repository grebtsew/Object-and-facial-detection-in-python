# Shared variables between threads
# contains:
# ENUM
# SHARED_VARIABLES
# CAMERA_STREAM

# Imports
import detection
import tracking
import show_camera
import sys
import threading
import cv2

# Create Enums with this class
class Enum(set):
    def __getattr__(self, name):
        if name in self:
            return name
        raise AttributeError


# Global shared variables
# an instace of this class share variables between system threads
class Shared_Variables():
    face_box = None
    detection_box = None
    tracking_box = None
    face_found = None
    detection_done = False
    tracking_running = True
    detection_running = True
    landmarks = None

    # Frames, can be showed in show_camera
    frame = None                        # current camera frame
    detection_frame = None              # latest detection frame
    tracking_and_detection_frame = None # latest tracking or detection frame

    # Threads reference
    detection_thread = None
    tracking_thread = None
    camera_thread = None
    camera_stream_thread = None
    
    # Enum
    Display_enum = Enum(["NORMAL", "DETECTION", "TRACKING_AND_DETECTION"])

    def __init__(self, name=None, camera_capture = None):
        threading.Thread.__init__(self)
        self.name = name
        self.camera_capture = camera_capture

       # start camera read Thread()
        self.camera_stream_running = True
        self.camera_stream_thread = camera_stream(shared_variables = self)
        self.camera_stream_thread.start()

   
    def start_detection_thread(self):
        self.detection_running = True
        self.detection_thread = detection.Detection(name = "Detection", shared_variables = self)
        self.detection_thread.start()
        
    def start_tracking_thread(self):
        self.tracking_running = True
        self.tracking_thread = tracking.Tracking(name = "Tracking", shared_variables = self)
        self.tracking_thread.start()
        
    def start_camera_thread(self, mode = Display_enum.NORMAL):
        self.camera_thread = show_camera.Show_Camera(name = "Show_Camera", shared_variables = self, mode = mode)
        self.camera_thread.start()


# Class Thread that reads camera stream, to make sure system only read camera stream once
class camera_stream(threading.Thread):
    def __init__(self, shared_variables = None):
        threading.Thread.__init__(self)
        self.shared_variables = shared_variables
        
    def run(self):
        while self.shared_variables.detection_running:
            if self.shared_variables.camera_capture.isOpened():
                temp, self.shared_variables.frame = self.shared_variables.camera_capture.read() 
                
