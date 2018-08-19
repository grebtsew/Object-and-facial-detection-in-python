# Visualize Camera thread

# imports
import utils.logging_data as LOG
from trackers.camshifttracker import CAMShiftTracker
import shared_variables
import numpy
import cv2
import sys
import threading
import time
import configparser

# Show_camera
# Class that show camera in thread
class Show_Camera(threading.Thread):

    # Change these
    show_detection = True      # Show detection RED
    show_tracking = True       # Show tracking GREEN
    show_landmarks = True       # Show facial features
    showbackprojectedFrame = False
    show_detection_score = False
    grayscale = False

    frame = None
    do_once = True              # initiate backprojektedframe once

    index = 0

    # Initiate function
    # Parameters CameraName, Shared_variables reference, show_mode
    def __init__(self, name=None,  shared_variables = None, index = 0):
        threading.Thread.__init__(self)
        self.name = name
        self.shared_variables = shared_variables
        self.index = index
        self.initiate_variables()

    def initiate_variables(self):
        self.show_detection = self.shared_variables.setting[self.index][shared_variables.SETTINGS.SHOW_DETECTION.value]
        self.show_tracking = self.shared_variables.setting[self.index][shared_variables.SETTINGS.SHOW_TRACKING.value]
        self.show_landmarks =self.shared_variables.setting[self.index][shared_variables.SETTINGS.SHOW_LANDMARKS.value]
        self.showbackprojectedFrame =self.shared_variables.setting[self.index][shared_variables.SETTINGS.SHOW_BACKPROJECTEDIMAGE.value]
        self.show_detection_score = self.shared_variables.setting[self.index][shared_variables.SETTINGS.SHOW_SCORE.value]
        self.grayscale = self.shared_variables.setting[self.index][shared_variables.SETTINGS.SHOW_GRAYSCALE.value]

    #Run
    # Get image, add detections, create and show in window
    def run(self):

        while True:
            if self.shared_variables.system_running:

                self.frame = self.shared_variables.frame[self.index]

                 # Show tracking GREEN
                if self.shared_variables.tracking_box[self.index] is not None:
                    if self.show_tracking:
                        topLeft = (int(self.shared_variables.tracking_box[self.index][0]), int(self.shared_variables.tracking_box[self.index][1]))
                        bottomRight = (int(self.shared_variables.tracking_box[self.index][0] + self.shared_variables.tracking_box[self.index][2]), int(self.shared_variables.face_box[self.index][1] + self.shared_variables.face_box[self.index][3]))
                        cv2.rectangle(self.frame, topLeft,bottomRight, (0,255,0), 2,1 )


                # Some face detected
                if self.shared_variables.face_found[self.index]:

                    #show score in terminal
                    #if self.show_detection_score:
                    #    if self.shared_variables.detection_score[self.index] is not None:
                    #        print(self.shared_variables.detection_score[self.index])

                    # Show detections BLUE
                    if self.shared_variables.detection_box[self.index] is not None:
                        if self.show_detection:
                            topLeft = (int(self.shared_variables.detection_box[self.index][0]), int(self.shared_variables.detection_box[self.index][1]))
                            bottomRight = (int(self.shared_variables.detection_box[self.index][0] + self.shared_variables.detection_box[self.index][2]), int(self.shared_variables.face_box[self.index][1] + self.shared_variables.face_box[self.index][3]))
                            cv2.rectangle(self.frame, topLeft,bottomRight, (255,0,0), 2,1 )

                            #show score in image
                            if self.show_detection_score:
                                if self.shared_variables.detection_score[self.index] is not None:
                                    self.draw_label(self.frame, bottomRight, str(self.shared_variables.detection_score[self.index]))

                            #show age and gender
                            if self.shared_variables.age[self.index] is not None and self.shared_variables.gender[self.index] is not None:
                                self.draw_label(self.frame, topLeft, str(int(self.shared_variables.age[self.index])) + " " + str(self.shared_variables.gender[self.index]))


                    # Show Landmarks RED
                    if self.show_landmarks:
                        # loop over the (x, y)-coordinates for the facial landmarks
                        # and draw them on the image
                        for (x, y) in self.shared_variables.landmarks[self.index]:
                            cv2.circle(self.frame, (x, y), 1, (0, 0, 255), -1)

                # show frame
                if self.frame is not None:

                    if self.grayscale:
                        self.frame = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)

                    cv2.imshow(self.shared_variables.name + "_"+ str(self.index), self.frame)

                # Create and show backproject frames
                if self.showbackprojectedFrame:
                    if self.shared_variables.face_box[self.index] is not None:
                        if self.do_once:
                            camShifTracker = CAMShiftTracker(self.shared_variables.face_box[self.index], self.frame)
                            self.do_once = False

                        cv2.imshow('BackImg %s' % self.shared_variables.name+ "_"+ str(self.index), camShifTracker.getBackProjectedImage(self.frame))

                # close program
                if cv2.waitKey(1) == 27:
                    break  # esc to quit
                if cv2.waitKey(25) & 0xFF == ord('q'):
                    break

        # stop camera
        cv2.destroyAllWindows()


    def draw_label(self, image, point, label, font=cv2.FONT_HERSHEY_SIMPLEX, font_scale=1, thickness=2):
        size = cv2.getTextSize(label, font, font_scale, thickness)[0]
        x, y = point
        cv2.rectangle(image, (x, y - size[1]), (x + size[0], y), (255, 0, 0), cv2.FILLED)
        cv2.putText(image, label, point, font, font_scale, (255, 255, 255), thickness)
