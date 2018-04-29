# Shared variables between threads
# contains:
# ENUM
# SHARED_VARIABLES
# CAMERA_STREAM

# Imports
import detection_dlib as dlib_detection
import detection_tensorflow as tf_detection
import tracking
import show_camera
import sys
import threading
import cv2
import listener
import imutils

from utils import gige_camera
from utils import intern_camera
from utils import ip_camera
from func.blink_frequency import dlib_blink_frequency as blink_frequency
from func.age_gender_estimation import dlib_age_gender_estimation as age_gender_estimation

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
    flipp_test_degree = 0
    flipp_test = True
    detection_score = None
    detection_running = True

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
    tf_detection_thread = None
    dlib_detection_thread = None
    tracking_thread = None
    camera_thread = None
    camera_stream_thread = None

    # Enum
    Display_enum = Enum(["NORMAL", "DETECTION", "TRACKING_AND_DETECTION"])

    def __init__(self, name=None):
        threading.Thread.__init__(self)
        self.name = name
        self.camera_capture = None

        #start camera read thread
        #self.start_ip_camera_stream()
        #self.start_intern_camera_stream()
        #self.start_gige_camera_stream()
        # start blink function thread
        #self.start_blink_thread()

        # start age gender function thread
        #self.start_age_gender_thread()

    def start_gige_camera_stream(self):
        self.camera_stream_running = True
        self.camera_stream_thread = gige_camera.camera_stream(shared_variables = self)
        self.camera_stream_thread.start()


    def start_ip_camera_stream(self):
        self.camera_stream_running = True
        self.camera_stream_thread = ip_camera.ip_camera_stream(shared_variables = self)
        self.camera_stream_thread.start()

    def start_age_gender_thread(self):
        age_gender_thread = age_gender_estimation.Age_gender_estimation(name = "Age_Gender_Estimation", shared_variables = self)
        age_gender_thread.start()

    def start_blink_thread(self):
        blink_thread = blink_frequency.Blink_frequency(name = "Blink_frequence", shared_variables = self)
        blink_thread.start()

    def start_intern_camera_stream(self, name=0):
        self.camera_capture = cv2.VideoCapture(name)
        self.camera_stream_running = True
        self.camera_stream_thread = intern_camera.camera_stream(shared_variables = self)
        self.camera_stream_thread.start()

    def start_dlib_detection_thread(self, cam_id):
        self.dlib_detection_thread = dlib_detection.Detection(name = "Dlib_Detection", shared_variables = self)
        self.dlib_detection_thread.start()

    def start_tf_detection_thread(self, cam_id):
        self.tf_detection_thread = tf_detection.Detection(name = "TF_Detection", shared_variables = self)
        self.tf_detection_thread.start()

    def start_tracking_thread(self):
        self.tracking_running = True
        self.tracking_thread = tracking.Tracking(name = "Tracking", shared_variables = self)
        self.tracking_thread.start()

    def start_camera_thread(self, mode = Display_enum.NORMAL):
        self.camera_thread = show_camera.Show_Camera(name = "Show_Camera", shared_variables = self, mode = mode)
        self.camera_thread.start()

    # Start_instance
    # Function that starts an instance of threads for each camera
    def start_instance(instance_name,camera_id,camera_mode='NORMAL'):

        LOG.log("Capturing Camera %s" % camera_id, instance_name)

        # Capture camera
        #_camera_capture = cv2.VideoCapture(camera_id)

         # initiate shared variables instance
        #_shared_variables = shared_variables.Shared_Variables(instance_name,
         #                                 _camera_capture)

        # detection Thread
        #_shared_variables.start_detection_thread()

        # tracking Thread
        #_shared_variables.start_tracking_thread()

        # show camera thread
        #_shared_variables.start_camera_thread(camera_mode)




    # Start a system instance for each camera in computer
    def start_instances_for_all_cameras():
    # start all cameras
        number_of_cameras =  i_cam.countCameras()

        LOG.log("Found %s cameras" % (number_of_cameras), "SYSTEM")
        for i in range(number_of_cameras):
            start_instance('CAM_%s' % (i), i, 'NORMAL')



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
        #listener.landmarks_notify(self.detection_frame, landmark)

    @landmarks.getter
    def landmarks(self):
        return self._landmarks
