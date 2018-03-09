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
import listener
import imutils

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
    tracking_box = None
    face_found = None
    detection_done = False
    tracking_running = True
    detection_running = True
    flipp_test_degree = 0
    flipp_test = True

    # Debugging threads
    debug = False   # debug mode, doesnt do much right now
    debug_detection = False
    debug_tracking = False
    
    # Listen to these variables
    _landmarks = None
    _detection_box = None

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

       # start camera read thread
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


    # Listen at variables
    # Detection variable
    @property
    def detection_box(self):
        return self._detection_box

    @detection_box.setter
    def detection_box(self, box):
        self._detection_box = box
        
        # Send to listener when variable set
        listener.box_notify(self.detection_frame, box)
        
        # Notify detection
        self.face_found = True
        self.detection_done = True
        
    @detection_box.getter
    def detection_box(self):
        return self._detection_box

    # Landmarks variable
    @property
    def landmarks(self):
        return self._landmarks

    @landmarks.setter
    def landmarks(self, landmark):
        self._landmarks = landmark

        # Send to listener when variable set
        listener.landmarks_notify(self.detection_frame, landmark)

    @landmarks.getter
    def landmarks(self):
        return self._landmarks

# Class Thread that reads camera stream, to make sure system only read camera stream once
class camera_stream(threading.Thread):
    start_time = None
    end_time = None
    
    def __init__(self, shared_variables = None):
        threading.Thread.__init__(self)
        self.shared_variables = shared_variables
        
    def run(self):
        while self.shared_variables.detection_running:
            if self.shared_variables.camera_capture.isOpened():
                temp, frame = self.shared_variables.camera_capture.read() 

                # flipp if needed
                if self.shared_variables.flipp_test:
                    self.shared_variables.frame = imutils.rotate(frame, self.shared_variables.flipp_test_degree)
                else: 
                    self.shared_variables.frame = frame
                
