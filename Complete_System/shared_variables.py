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
from enum import Enum

from utils import web_camera
from utils import ip_camera
from func.blink_frequency import dlib_blink_frequency as blink_frequency
from func.age_gender_estimation import dlib_age_gender_estimation as age_gender_estimation

# Create Enums with this class
#class Enum(set):
#    def __getattr__(self, name):
#        if name in self:
#            return name
#        raise AttributeError

class SETTINGS(Enum):
    SKIN_COLOR = 0
    EXPRESSION = 1
    BLINK_FREQUENCY = 2
    AGE_GENDER_ESTIMATION = 3
    TENSORFLOW_DETECTION = 4
    DLIB_DETECTION = 5
    TRACKING = 6
    SHOW_DETECTION = 7
    SHOW_TRACKING = 8
    SHOW_LANDMARKS = 9
    SHOW_BACKPROJECTEDIMAGE = 10
    SHOW_SCORE = 11
    SHOW_GRAYSCALE = 12
    LOG_DATA = 13
    DEBUG = 14

# Global shared variables
# an instace of this class share variables between system threads
class Shared_Variables():
# Enum


    '''
    ----- Setting Variables -----
    '''

    # Debugging threads
    debug = False   # debug mode, doesnt do much right now

    '''
    ----- Shared Variables -----
    These variables are shared between threads fast
    '''
    # score and boxes
    detection_score = []
    face_box = []
    tracking_box = []

    # Flipp test
    flipp_test_degree = []
    flipp_test = []

    # Listen to these variables
    landmarks = []
    detection_box = []

    # Frames, can be showed in show_camera
    frame = []                        # current camera frame

    # booleans
    face_found = []
    tracking_running = []
    setting = []

    '''
    ----- Status Variables -----
    '''
    system_running = True
    config = None

    def __init__(self, name=None, config=None):
        threading.Thread.__init__(self)
        self.name = name

        self.config = config
        if config is None:
            self.initiate_configfile()


    def initiate_configfile(self):
        try:
            self.config = configparser.ConfigParser()
            self.config.read("config.ini")
        except Exception as e:
            print("No config file found!")


    def set_init_settings(self):
        return [self.config.getboolean('DEFAULT', 'SKIN_COLOR'),
                self.config.getboolean('DEFAULT', 'EXPRESSION'),
                self.config.getboolean('DEFAULT', 'BLINK_FREQUENCY'),
                self.config.getboolean('DEFAULT', 'AGE_GENDER_ESTIMATION'),
                self.config.getboolean('DEFAULT', 'TENSORFLOW_DETECTION'),
                self.config.getboolean('DEFAULT', 'DLIB_DETECTION'),
                self.config.getboolean('DEFAULT', 'TRACKING'),
                 self.config.getboolean('SHOW', 'DETECTION'),
                 self.config.getboolean('SHOW', 'TRACKING'),
                 self.config.getboolean('SHOW', 'LANDMARKS'),
                 self.config.getboolean('SHOW', 'BACKPROJECTEDIMAGE'),
                 self.config.getboolean('SHOW', 'SCORE'),
                 self.config.getboolean('SHOW', 'GRAYSCALE'),
                 self.config.getboolean('LOG', 'LOG_DATA'),
                 self.config.getboolean('DEBUG', 'DEBUG')
            ]

    def add_camera(self):
        '''
        Instantiate a new slot for a new camera (allocation!)
        '''
        self.frame.append(None)
        self.face_box.append(None)
        self.tracking_box.append(None)
        self.landmarks.append(None)
        self.detection_box.append(None)
        self.detection_score.append(None)

        self.setting.append(self.set_init_settings())
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
        self.tracking_thread = tracking.Tracking(name = "Tracking", shared_variables = self, index = index)
        self.tracking_thread.start()

    '''
    ----- SHOW CAMERA -----
    '''

    def start_show_camera(self, index = 0):
        self.camera_thread = show_camera.Show_Camera(name = "Show_Camera", shared_variables = self, index = index)
        self.camera_thread.start()


    '''
    ----- FUNCTIONS -----
    '''

    def start_age_gender_thread(self, index = 0):
        age_gender_thread = age_gender_estimation.Age_gender_estimation(name = "Age_Gender_Estimation", shared_variables = self, index = 0)
        age_gender_thread.start()

    def start_expression_thread(self, index = 0):
        pass

    def start_blink_thread(self, index = 0):
        blink_thread = blink_frequency.Blink_frequency(name = "Blink_frequence", shared_variables = self, index = 0)
        blink_thread.start()


    '''
    ----- Listener -----
    '''

    def set_detection_box(self, box, index):
        self.detection_box[index] = box

        # Send to listener when variable set
        listener.box_notify(self.frame[index], self.setting[index], box)

        # Notify detection
        self.face_found[index] = True

    def set_landmarks(self, landmark, index):
        self.landmarks[index] = landmark

        # Send to listener when variable set
        listener.landmarks_notify(self.frame[index], self.setting[index], landmark)

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
