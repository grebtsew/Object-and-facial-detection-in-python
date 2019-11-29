'''
This is Shared variables class. This is the center Node of the system where alot of threads share variables.
'''

import threading

# Core functions
from visualise_gui.visualisation import Visualisation
from input.camera import camera
from object_detection.detection import Object_Detection
from tracking.tracking import Tracking

# On zoom in effects
from face_detection.detection import Face_Detection

# Global shared variables
# an instace of this class share variables between system threads
class Shared_Variables():

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
    detection_box = None
    face_box = None
    tracking_box = None

    name_data = None
    age_data = None
    gender_data = None
    expression_data = None

    # Listen to these variables
    landmarks = None

    # Frames, can be showed in show_camera
    frame = None     # current camera frame

    model_loaded = False
    boxes = []
    '''
    ----- Status Variables -----
    '''
    system_running = True
    detection_lock = False
    tracking_lock = False
    tracking_threads = []

    def __init__(self):
        threading.Thread.__init__(self)

    '''
    ----- CAMERAS -----
    '''

    def start_camera_stream(self, address = 0):
        self.camera = camera(shared_variables = self, address = address )
        self.camera.start()

    '''
    ----- DETECTION -----
    '''

    def start_object_detection_thread(self):
        self.object_detection = Object_Detection( shared_variables = self)
        self.object_detection.start()

    def start_face_detection_thread(self):
        self.face_detection = Face_Detection(shared_variables = self)
        self.face_detection.start()


    '''
    ----- TRACKING -----
    '''

    def start_tracking_thread(self, frame, box):
        self.tracking_thread = Tracking(name = "Tracking", shared_variables = self, frame =frame,box = box)
        self.tracking_thread.start()
        return self.tracking_thread

    '''
    ----- Visualisation -----
    '''

    def start_visualisation_thread(self, ):
        self.visualisation_thread = Visualisation(name = "Show", shared_variables = self)
        self.visualisation_thread.start()

    '''
    ----- FUNCTIONS -----
    '''
    def start_fatigue_thread(self):
        fatigue_thread = Fatigue_Detection(shared_variables = self)
        fatigue_thread.start()

    def start_age_gender_thread(self):
        age_gender_thread = age_gender_estimation.Age_gender_estimation( shared_variables = self)
        age_gender_thread.start()

    def start_expression_thread(self):
        express = expression.Expression( shared_variables = self)
        express.start()

    def start_name_thread(self):
        name_thread = name_thread.Name_detection( shared_variables = self)
        name_thread.start()
