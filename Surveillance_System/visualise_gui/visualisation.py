
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

    selected_box = None
    clicked_pos = []

    def draw_box(self, img, pt1, pt2, color, thickness, r, d):
        x1,y1 = pt1
        x2,y2 = pt2

        # Top left
        cv2.line(img, (x1 + r, y1), (x1 + r + d, y1), color, thickness)
        cv2.line(img, (x1, y1 + r), (x1, y1 + r + d), color, thickness)
        cv2.ellipse(img, (x1 + r, y1 + r), (r, r), 180, 0, 90, color, thickness)

        # Top right
        cv2.line(img, (x2 - r, y1), (x2 - r - d, y1), color, thickness)
        cv2.line(img, (x2, y1 + r), (x2, y1 + r + d), color, thickness)
        cv2.ellipse(img, (x2 - r, y1 + r), (r, r), 270, 0, 90, color, thickness)

        # Bottom left
        cv2.line(img, (x1 + r, y2), (x1 + r + d, y2), color, thickness)
        cv2.line(img, (x1, y2 - r), (x1, y2 - r - d), color, thickness)
        cv2.ellipse(img, (x1 + r, y2 - r), (r, r), 90, 0, 90, color, thickness)

        # Bottom right
        cv2.line(img, (x2 - r, y2), (x2 - r - d, y2), color, thickness)
        cv2.line(img, (x2, y2 - r), (x2, y2 - r - d), color, thickness)
        cv2.ellipse(img, (x2 - r, y2 - r), (r, r), 0, 0, 90, color, thickness)

    def click_event(self, event, x, y, flags, param):
        # grab references to the global variables

        if event == cv2.EVENT_LBUTTONDOWN:
            self.clicked_pos = [x, y]

        elif event == cv2.EVENT_LBUTTONUP:
            # if inside a box
            for b in self.shared_variables.tracking_threads:
                if self.posinsidebox(self.clicked_pos, b.box):
                    self.selected_box = b;


    def posinsidebox(self,pos, box):
        return pos[0] >= box[0] and pos[0] <= box[0]+box[2] and pos[1] >=box[1] and pos[1] <=box[1]+box[3]

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

                    if self.selected_box is not None:
                        if self.selected_box == b:
                            self.draw_box(self.frame, (x, y), (x + w, y + h), (255, 0, 0),3, 20, 10)
                        else:
                            self.draw_box(self.frame, (x, y), (x + w, y + h), (0, 0, 255),3, 20, 10)
                    else:
                        self.draw_box(self.frame, (x, y), (x + w, y + h), (0, 0, 255),3,20,10)

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
