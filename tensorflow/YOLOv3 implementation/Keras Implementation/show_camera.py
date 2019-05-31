# Visualize Camera thread

import numpy
import cv2
import sys
import threading
import time


# Show_camera
# Class that show camera in thread
class Show_Camera(threading.Thread):

    frame = None

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


                    cv2.imshow("YOLO3 KERAS", self.shared_variables.detection_result)

                # close program
                if cv2.waitKey(1) == 27:
                    break  # esc to quit
                if cv2.waitKey(25) & 0xFF == ord('q'):
                    break

        # terminate all threads
        self.shared_variables.detection_running = False

        # stop camera
        self.shared_variables.camera_capture.release()
        cv2.destroyAllWindows()
