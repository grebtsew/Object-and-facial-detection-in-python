'''
This is Shared variables class. This is the center Node of the system where alot of threads share variables.
'''

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

from utils import web_camera
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

    '''
    ----- Setting Variables -----
    '''
    flipp_test_degree = []
    flipp_test = []
    # Debugging threads
    debug = False   # debug mode, doesnt do much right now
    debug_detection = False
    debug_tracking = False

    '''
    ----- Shared Variables -----
    These variables are shared between threads fast
    '''
    # score and boxes
    detection_score = []
    face_box = []
    tracking_box = []

    # Listen to these variables
    _landmarks = []
    _detection_box = []

    # Frames, can be showed in show_camera
    frame = []                        # current camera frame
    detection_frame = []              # latest detection frame
    tracking_and_detection_frame = [] # latest tracking or detection frame

    # booleans
    face_found = []
    tracking_running = []

    '''
    ----- Status Variables -----
    '''
    system_running = True


    '''
    ----- ENUMS -----
    '''

    # Enum
    Display_enum = Enum(["NORMAL", "DETECTION", "TRACKING_AND_DETECTION"])

    def __init__(self, name=None):
        threading.Thread.__init__(self)
        self.name = name

    def add_camera(self):
        '''
        Instantiate a new slot for a new camera (allocation!)
        '''
        self.frame.append(None)
        self.detection_frame.append(None)
        self.tracking_and_detection_frame.append(None)
        self.face_box.append(None)
        self.tracking_box.append(None)
        self._landmarks.append(None)
        self._detection_box.append(None)
        self.detection_score.append(None)

        # Sets
        self.face_found.append(False)
        self.flipp_test.append(True)
        self.flipp_test_degree.append(0)
        self.tracking_running.append(False)

    '''
    ----- CAMERAS -----
    '''

    def start_ip_camera_stream(self, address = "", index = 0):
        self.add_camera()
        self.camera_stream_thread = ip_camera.ip_camera_stream(shared_variables = self, address = address , index = index)
        self.camera_stream_thread.start()


    def start_webcamera_stream(self, cam_id=0, index = 0):
        self.add_camera()
        self.camera_stream_thread = web_camera.camera_stream(shared_variables = self, id = cam_id, index = index)
        self.camera_stream_thread.start()

    '''
    ----- DETECTION -----
    '''

    def start_dlib_detection_thread(self, cam_id):
        self.dlib_detection_thread = dlib_detection.Detection(name = cam_id, shared_variables = self)
        self.dlib_detection_thread.start()

    def start_tf_detection_thread(self, cam_id):
        self.tf_detection_thread = tf_detection.Detection(name = cam_id, shared_variables = self)
        self.tf_detection_thread.start()


    '''
    ----- TRACKING -----
    '''

    def start_tracking_thread(self, index = 0):
        self.tracking_running = True
        self.tracking_thread = tracking.Tracking(name = "Tracking", shared_variables = self, index = index)
        self.tracking_thread.start()

    '''
    ----- SHOW CAMERA -----
    '''

    def start_show_camera(self, mode = Display_enum.NORMAL, index = 0):
        self.camera_thread = show_camera.Show_Camera(name = "Show_Camera", shared_variables = self, mode = mode, index = index)
        self.camera_thread.start()


    '''
    ----- FUNCTIONS -----
    '''

    def start_age_gender_thread(self, index = 0):
        age_gender_thread = age_gender_estimation.Age_gender_estimation(name = "Age_Gender_Estimation", shared_variables = self, index = 0)
        age_gender_thread.start()


    def start_expression_thread(self, index = 0):
        pass

    def start_skin_color(self, index = 0):
        pass

    def start_blink_thread(self, index = 0):
        blink_thread = blink_frequency.Blink_frequency(name = "Blink_frequence", shared_variables = self, index = 0)
        blink_thread.start()


    '''
    ----- Overides of getters and setters -----
    '''

    # Listen at variables
    # Detection variable
    @property
    def detection_box(self):
        return self._detection_box

    @detection_box.setter
    def detection_box(self, box):
        self._detection_box = box

        # Send to listener when variable set
        #listener.box_notify(self.detection_frame, box)

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


    '''
    ----- OLD CODE -----
    '''

    # Start a system instance for each camera in computer
    def start_instances_for_all_cameras():
    # restcode
    # start all cameras
        number_of_cameras =  i_cam.countCameras()

        LOG.log("Found %s cameras" % (number_of_cameras), "SYSTEM")
        for i in range(number_of_cameras):
            start_instance('CAM_%s' % (i), i, 'NORMAL')
