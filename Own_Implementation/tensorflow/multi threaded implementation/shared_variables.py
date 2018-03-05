# Shared variables between threads
import detection
import tracking
import show_camera

# system
import sys
import threading

# camera
import cv2

class Enum(set):
    def __getattr__(self, name):
        if name in self:
            return name
        raise AttributeError

# global shared variables
class Shared_Variables():
    face_box = None
    detection_box = None
    tracking_box = None
    face_found = None
    detection_done = False
    tracking_running = True
    detection_running = True
    landmarks = None

    # Frames
    frame = None
    detection_frame = None
    tracking_and_detection_frame = None

    # Threads
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

       # start camerea read Thread()
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


# Thread that reads camera stream, to only read stream once
class camera_stream(threading.Thread):
    def __init__(self, shared_variables = None):
        threading.Thread.__init__(self)
        self.shared_variables = shared_variables
       
        
    def run(self):
        while self.shared_variables.detection_running:
            if self.shared_variables.camera_capture.isOpened():
                temp, self.shared_variables.frame = self.shared_variables.camera_capture.read() 
                
