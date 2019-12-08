
# Visualize Camera thread

import numpy
import cv2
import sys
import threading
import time
import numpy as np


# Show_camera
# Class that show camera in thread
class Visualisation(threading.Thread):

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

    def click_event(self, event, x, y, flags, param):
        # grab references to the global variables

        if event == cv2.EVENT_LBUTTONDOWN:
            refPt = [(x, y)]
            print(str(refPt))

        elif event == cv2.EVENT_LBUTTONUP:
            refPt = [(x, y)]
            print(str(refPt))

    # Initiate function
    # Parameters CameraName, Shared_variables reference, show_mode
    def __init__(self, name=None,  shared_variables = None):
        threading.Thread.__init__(self)
        self.name =  "SURVEILLANCE SYSTEM"
        self.shared_variables = shared_variables


    def all_tracking_done(self):
        for t in self.shared_variables.tracking_threads:
            if not t.tracking_done:
                return False
        return True

    #Run
    # Get image, add detections, create and show in window
    def run(self):

        while True:
            if self.shared_variables.frame is not None and self.shared_variables.model_loaded:
                current_boxes = []
                # show frame
                self.frame = self.shared_variables.frame
                for b in self.shared_variables.tracking_threads:
                    box = b.box
                    x = int(box[0])
                    y = int(box[1])
                    w = int(box[2])
                    h = int(box[3])
                    topLeft = (x, y)
                    bottomRight = (x+w, y+h)
                    cv2.rectangle(self.frame, topLeft,bottomRight, (0,0,255), 2,1 )
                    current_boxes.append((topLeft,bottomRight))

                cv2.imshow(self.name, cv2.resize( self.frame, (640, 480)))
                cv2.setMouseCallback(self.name, self.click_event)

                # close program
                if cv2.waitKey(1) == 27:
                    break  # esc to quit
                if cv2.waitKey(25) & 0xFF == ord('q'):
                    break

            else:
                time.sleep(0.1)

        # stop camera
        self.shared_variables.camera_capture.release()
        cv2.destroyAllWindows()
