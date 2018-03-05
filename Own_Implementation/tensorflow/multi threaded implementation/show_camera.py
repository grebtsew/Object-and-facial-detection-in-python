# Camera thread

# imports

# import own
import utils.logging_data as LOG
from testing.trackers.camshifttracker import CAMShiftTracker

import numpy
import cv2
import sys
import threading
import time

# Show_camera
# Class that show camera in thread
class Show_Camera(threading.Thread):

    show_fps = True
    show_combo = True
    show_detection = False
    show_tracking = False
    show_landmarks = True
    frame = None
    stream_reader_thread = None
    showbackprojectedFrame = True
    do_once = True
    fps = 0
    
    def __init__(self, name=None,  shared_variables = None, mode = 'NORMAL'):
        threading.Thread.__init__(self)
        self.name = name
        self.shared_variables = shared_variables
        self.mode = mode

    def run(self):
        while True:
            if self.shared_variables.camera_capture.isOpened():

               # start = time.time()

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

                    # Show combination of tracking and detection, BLUE
                    if self.shared_variables.face_box:

                        
                        if self.show_combo:
                            topLeft = (int(self.shared_variables.face_box[0]), int(self.shared_variables.face_box[1]))
                            bottomRight = (int(self.shared_variables.face_box[0] + self.shared_variables.face_box[2]), int(self.shared_variables.face_box[1] + self.shared_variables.face_box[3]))
                            cv2.rectangle(self.frame, topLeft,bottomRight, (255,0,0), 2,1 )

                     # Show tracking GREEN
                    if self.shared_variables.tracking_box:
                        if self.show_tracking:
                            topLeft = (int(self.shared_variables.tracking_box[0]), int(self.shared_variables.tracking_box[1]))
                            bottomRight = (int(self.shared_variables.tracking_box[0] + self.shared_variables.tracking_box[2]), int(self.shared_variables.face_box[1] + self.shared_variables.face_box[3]))
                            cv2.rectangle(self.frame, topLeft,bottomRight, (0,255,0), 2,1 )

                    # Show detections RED
                    if self.shared_variables.detection_box:
                        if self.show_detection:
                            topLeft = (int(self.shared_variables.detection_box[0]), int(self.shared_variables.detection_box[1]))
                            bottomRight = (int(self.shared_variables.detection_box[0] + self.shared_variables.detection_box[2]), int(self.shared_variables.face_box[1] + self.shared_variables.face_box[3]))
                            cv2.rectangle(self.frame, topLeft,bottomRight, (0,0,255), 2,1 )

                    # Show Landmarks
                    if self.show_landmarks:
                            for j in range(5):
                                size = 1
                                top_left = (int(self.shared_variables.landmarks[0, j]) - size, int(self.shared_variables.landmarks[0, j + 5]) - size)
                                bottom_right = (int(self.shared_variables.landmarks[0, j]) + size, int(self.shared_variables.landmarks[0, j + 5]) + size)
                                cv2.rectangle(self.frame, top_left, bottom_right, (255, 0, 255), 2)
                
                
                # print fps
                #end = time.time()

                #seconds = end - start
                #if seconds != 0:
                #    self.fps = round(1 / seconds, 2)
        
                
                #if self.show_fps:
                #    font = cv2.FONT_HERSHEY_SIMPLEX
                #    cv2.putText(self.frame, str(self.fps), (0, 100), font, 1, (255, 255, 255), 1, cv2.LINE_AA)

                
                # show frame
                if self.frame is not None:
                    cv2.imshow(self.shared_variables.name, self.frame)

                if self.showbackprojectedFrame:
                    if self.shared_variables.face_box is not None:
                    # Create and show backproject frames
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

