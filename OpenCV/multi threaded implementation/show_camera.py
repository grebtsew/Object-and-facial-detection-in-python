# Visualize Camera thread

# imports
import logging_data as LOG
from testing.trackers.camshifttracker import CAMShiftTracker

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
    show_detection = True      # Show detection RED
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


                     # Show tracking GREEN
                    if self.shared_variables.tracking_box is not None:
                        if self.show_tracking:
                            topLeft = (int(self.shared_variables.tracking_box[0]), int(self.shared_variables.tracking_box[1]))
                            bottomRight = (int(self.shared_variables.tracking_box[0] + self.shared_variables.tracking_box[2]), int(self.shared_variables.face_box[1] + self.shared_variables.face_box[3]))
                            cv2.rectangle(self.frame, topLeft,bottomRight, (0,255,0), 2,1 )


                    # Show detections RED
                    if self.shared_variables.detection_box is not None:
                        if self.show_detection:
                            faces = self.shared_variables.detection_box
                            for (x,y,w,h) in faces:
                                cv2.rectangle(self.frame,(x,y),(x+w,y+h),(255,0,0),2)
                                roi_color = self.frame[y:y+h, x:x+w]
                                for (ex,ey,ew,eh) in facials:
                                    cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,100,0),2)

                    # Show Landmarks
                    if self.show_landmarks:
                        if len(self.shared_variables.landmarks) >= 1:
                            facials = self.shared_variables.landmarks
                            for (x,y,w,h) in self.shared_variables.detection_box:
                                roi_color = self.frame[y:y+h, x:x+w]
                                for (ex,ey,ew,eh) in facials:
                                    cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,100,0),2)

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


      # TEST FUNC
    # Return box of eye images
    def cropEyes(self,frame, landmarks):
        nose_pos = [landmarks[0,2], landmarks[0,7]]
        left_eye_pos = [landmarks[0,0], landmarks[0,5]]
       # right_eye_pos = [landmarks[1], landmarks[6]]



        #calculate eye size
        w = abs((nose_pos[0]- left_eye_pos[0])*0.4);
        h = abs((nose_pos[1]- left_eye_pos[1])*0.2);


        x = int(landmarks[0,0] - w/2)
        y = int(landmarks[0,5] - h/2)

        h = 50   #height pixels
        w = 100  #width pixels

        x = int(landmarks[0,1] - w/2)
        y = int(landmarks[0,6] - h/2)

        left_eye_img = frame[y:y+h, x:x+w]

        cv2.imshow('test_eye', left_eye_img)

        pass
