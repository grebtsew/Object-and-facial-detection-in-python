# Visualize Camera thread

# imports
import utils.logging_data as LOG
from trackers.camshifttracker import CAMShiftTracker

import numpy
import cv2
import sys
import threading
import time

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
    def __init__(self, name=None,  shared_variables = None, mode = 'NORMAL'):
        threading.Thread.__init__(self)
        self.name = name
        self.shared_variables = shared_variables
        self.mode = mode

    #Run
    # Get image, add detections, create and show in window
    def run(self):
        while True:
            if self.shared_variables.camera_capture.isOpened():

                # Display mode
                if self.mode == self.shared_variables.Display_enum.NORMAL:
                   # ret_val, self.frame = self.shared_variables.camera_capture.read()
                    self.frame = self.shared_variables.frame
                elif self.mode == self.shared_variables.Display_enum.DETECTION:
                    self.frame = self.shared_variables.detection_frame
                elif self.mode == self.shared_variables.Display_enum.TRACKING_AND_DETECTION:
                    self.frame = self.shared_variables.tracking_and_detection_frame

                # Some face detected
                if self.shared_variables.face_found:

                    #show score in terminal
                    if self.show_detection_score:
                        if self.shared_variables.detection_score is not None:
                            print(self.shared_variables.detection_score)
                        

                    # Show combination of tracking and detection, BLUE
                    if self.shared_variables.face_box is not None:


                                            
                        if self.show_combo:
                            topLeft = (int(self.shared_variables.face_box[0]), int(self.shared_variables.face_box[1]))
                            bottomRight = (int(self.shared_variables.face_box[0] + self.shared_variables.face_box[2]), int(self.shared_variables.face_box[1] + self.shared_variables.face_box[3]))
                            cv2.rectangle(self.frame, topLeft,bottomRight, (255,0,0), 2,1 )

                     # Show tracking GREEN
                    if self.shared_variables.tracking_box is not None:
                        if self.show_tracking:
                            topLeft = (int(self.shared_variables.tracking_box[0]), int(self.shared_variables.tracking_box[1]))
                            bottomRight = (int(self.shared_variables.tracking_box[0] + self.shared_variables.tracking_box[2]), int(self.shared_variables.face_box[1] + self.shared_variables.face_box[3]))
                            cv2.rectangle(self.frame, topLeft,bottomRight, (0,255,0), 2,1 )

  
                    # Show detections RED
                    if self.shared_variables.detection_box is not None:
                        if self.show_detection:
                            topLeft = (int(self.shared_variables.detection_box[0]), int(self.shared_variables.detection_box[1]))
                            bottomRight = (int(self.shared_variables.detection_box[0] + self.shared_variables.detection_box[2]), int(self.shared_variables.face_box[1] + self.shared_variables.face_box[3]))
                            cv2.rectangle(self.frame, topLeft,bottomRight, (0,0,255), 2,1 )

                    # Show Landmarks
                    if self.show_landmarks:
                        # loop over the (x, y)-coordinates for the facial landmarks
                        # and draw them on the image
                        for (x, y) in self.shared_variables.landmarks:
                            cv2.circle(self.frame, (x, y), 1, (0, 0, 255), -1)
                
                
                # show frame
                if self.frame is not None:
                    
                    if self.grayscale:
                        self.frame = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)

                    cv2.imshow(self.shared_variables.name, self.frame)

                # Create and show backproject frames
                if self.showbackprojectedFrame:
                    if self.shared_variables.face_box is not None:
                        if self.do_once:
                            camShifTracker = CAMShiftTracker(self.shared_variables.face_box, self.frame)
                            self.do_once = False
                            
                        cv2.imshow('BackImg %s' % self.shared_variables.name, camShifTracker.getBackProjectedImage(self.frame))
               

                    
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


     

