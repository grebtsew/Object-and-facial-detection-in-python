# Visualize Camera thread

import numpy
import cv2
import sys
import threading
import time

from yolo_v3 import Yolo_v3
from utils import load_images, load_class_names, draw_boxes, draw_frame


# Show_camera
# Class that show camera in thread
class Show_Camera(threading.Thread):

    # Change these
    show_combo = True           # Show both detection and tracking as BLUE
    show_detection = False      # Show detection RED
    show_tracking = False       # Show tracking GREEN
    show_landmarks = True       # Show facial features
    showbackprojectedFrame = False
    show_detection_score = False
    grayscale = False


    frame = None
    do_once = True              # initiate backprojektedframe once

    # Initiate function
    # Parameters CameraName, Shared_variables reference, show_mode
    def __init__(self, name=None,  shared_variables = None):
        threading.Thread.__init__(self)

        self.shared_variables = shared_variables

    #Run
    # Get image, add detections, create and show in window
    def run(self):
        while True:
            if self.shared_variables.camera_capture.isOpened():

                # show frame
                if self.shared_variables.detection_result is not None:

                    draw_frame(self.shared_variables.frame, self.shared_variables.frame_size, self.shared_variables.detection_result,
                               self.shared_variables.class_names, self.shared_variables.model_size)


                    cv2.imshow("YOLO3 CPU", self.shared_variables.frame)

                # close program
                if cv2.waitKey(1) == 27:
                    break  # esc to quit
                if cv2.waitKey(25) & 0xFF == ord('q'):
                    break


        # terminate all threads
        self.shared_variables.tracking_running = False
        self.shared_variables.detection_running = False

        # stop camera
        self.shared_variables.camera_capture.release()
        cv2.destroyAllWindows()
