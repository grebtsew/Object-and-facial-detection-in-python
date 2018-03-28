# Camera thread

# imports

# import own

from trackers.camshifttracker import CAMShiftTracker

import numpy
import cv2
import sys
import threading
import time

import dlib


show_fps = True
show_combo = True
show_detection = False
show_tracking = False
show_landmarks = True
frame = None
stream_reader_thread = None
showbackprojectedFrame = True
fps = 0

camera_capture = cv2.VideoCapture(0)

while True:
    
    ret_val, frame = camera_capture.read()
    frontFaceDetector = dlib.get_frontal_face_detector()
    faceRect = frontFaceDetector(frame, 0)        
    bbox = faceRect[0]    
    curWindow = (int(bbox.left()), int(bbox.top()), int(bbox.right() - bbox.left()),
                         int(bbox.bottom() - bbox.top()) )
    camShifTracker = CAMShiftTracker(curWindow, frame)
    break

while True:
    if camera_capture.isOpened():
        start = time.time()

        ret_val, frame = camera_capture.read()
        
        end = time.time()

        seconds = end - start
        
        if seconds != 0:
            fps = round(1 / seconds, 2)

        if show_fps:
            font = cv2.FONT_HERSHEY_SIMPLEX
            cv2.putText(frame, str(fps), (0, 100), font, 1, (255, 255, 255), 1, cv2.LINE_AA)

            # show frame
        bkprojectImage = camShifTracker.getBackProjectedImage(frame)
        cv2.imshow("CAMShift Face in Back Project Image", bkprojectImage)
        

                    
                # close program
        if cv2.waitKey(1) == 27:
            break  # esc to quit
        if cv2.waitKey(25) & 0xFF == ord('q'):
            break
                    
        # stop camera
camera_capture.release()
cv2.destroyAllWindows()

