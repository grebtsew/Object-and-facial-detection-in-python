# Camera thread

# imports

# import own

#from trackers.camshifttracker import CAMShiftTracker

import numpy
import cv2
import sys
import threading
import time
import tensorflow as tf


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
    if camera_capture.isOpened():
        start = time.time()

        ret_val, frame = camera_capture.read()
        
        end = time.time()

        seconds = end - start

        print (tf.eye(0))

        
        if seconds != 0:
            fps = round(1 / seconds, 2)

        if show_fps:
            font = cv2.FONT_HERSHEY_SIMPLEX
            cv2.putText(frame, str(fps), (0, 100), font, 1, (255, 255, 255), 1, cv2.LINE_AA)

            # show frame
        if frame is not None:
            cv2.imshow("test", frame)

                    
                # close program
        if cv2.waitKey(1) == 27:
            break  # esc to quit
        if cv2.waitKey(25) & 0xFF == ord('q'):
            break
                    
        # stop camera
camera_capture.release()
cv2.destroyAllWindows()

