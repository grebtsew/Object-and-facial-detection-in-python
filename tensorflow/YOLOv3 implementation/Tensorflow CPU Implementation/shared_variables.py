import detection
import show_camera
import sys
import threading
import cv2
import imutils


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
    detection_score = None

    detection_result = None
    class_names = None
    n_classes = None
    model_size = None
    frame_size = None
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


    def __init__(self, camera_capture = None):
        threading.Thread.__init__(self)
        self.camera_capture = camera_capture

       # start camera read thread
        self.camera_stream_running = True
        self.camera_stream_thread = camera_stream(shared_variables = self)
        self.camera_stream_thread.start()

    def start_detection_thread(self):
        self.detection_running = True
        self.detection_thread = detection.Detection(name = "Detection", shared_variables = self)
        self.detection_thread.start()

    def start_camera_thread(self, ):
        self.camera_thread = show_camera.Show_Camera(name = "Show_Camera", shared_variables = self)
        self.camera_thread.start()


# Class Thread that reads camera stream, to make sure system only read camera stream once
class camera_stream(threading.Thread):
    start_time = None
    end_time = None
    grayscale = False

    def __init__(self, shared_variables = None):
        threading.Thread.__init__(self)
        self.shared_variables = shared_variables

    def run(self):
        temp, frame = self.shared_variables.camera_capture.read()
        height, width, channel = frame.shape

        self.shared_variables.frame_size = (width, height)

        while self.shared_variables.detection_running:
            if self.shared_variables.camera_capture.isOpened():
                temp, frame = self.shared_variables.camera_capture.read()



                # flipp if needed
                if self.shared_variables.flipp_test:
                    self.shared_variables.frame = imutils.rotate(frame, self.shared_variables.flipp_test_degree)
                else:
                    self.shared_variables.frame = frame
