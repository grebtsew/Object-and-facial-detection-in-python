# This Code uses dlib detection and various tracking models to track one person at a time from webcam

#own imports
import frame_listener as FL
import logging_data as LOG

import threading
import time
import sys

# tracker imports
import cv2
from trackers.camshifttracker import CAMShiftTracker


# detection import
import face_recognition
import dlib

tracker = None
face_landmarks_list = None
face_found = False
ticks = 0
DETECTION_SLEEP_TICKS = 0   # Constant
FAST_DETECTION_SLEEP_TICKS = 50   # Constant
SLOW_DETECTION_SLEEP_TICKS = 10   # Constant
cam_cap = None
face_box = None
FaceDetector = None
frame = None
frame_listener = FL.Frame_Listener()

# For camShift tracking
camShifTracker = None
rotatedWindow = None
#bkprojectImage = None
x = None
y = None
w = None
h = None


# Own Implementation Class


# Init
#
# Initiate function variables and functions
#
def init():
    global cam_cap
    cam_cap = cv2.VideoCapture(0) # capture webcam

    global FaceDetector
    FaceDetector = dlib.get_frontal_face_detector()

    # needed for custom tracking
    update_custom_tracker()

    pass


# Object_CamShift_tracking
#
# This function uses CamShiftTracking with OpenCV
# I will probably not use this tracking due to scaling fixes
#
def object_CamShift_tracking():
    #print("Tracking")
    global frame

    # Send box to tracker
    global face_box
    global camShifTracker

    if face_box is None or frame is None:
        return

    camShifTracker = CAMShiftTracker(face_box, frame)

    # Calculate
    camShifTracker.computeNewWindow(frame)

    global x
    global y
    global w
    global h
    x,y, w, h = camShifTracker.getCurWindow()

    # update face_box
    face_box = (x,y,w,h)

    #global bkprojectImage
    #bkprojectImage = camShifTracker.getBackProjectedImage(frame)

    # display the current window
    cv2.rectangle(frame, (x,y), (x+w, y+h), (255, 0, 0), 2, cv2.LINE_AA)

    global rotatedWindow
    rotatedWindow = camShifTracker.getRotatedWindow()

    #display rotated window

    cv2.polylines(frame, [rotatedWindow], True, (0,255,0), 2, cv2.LINE_AA)

# Update_custom_tracker
#
# Set and reset custom tracker
#
def update_custom_tracker():
    global tracker
    tracker = cv2.TrackerBoosting_create()
    #tracker = cv2.TrackerMIL_create()
    #tracker = cv2.TrackerKCF_create()
    #tracker = cv2.TrackerTLD_create()
    #tracker = cv2.TrackerMedianFlow_create()


# Object_Custom_tracking
#
# This function uses the OpenCV tracking form uncommented in update_custom_tracking
#
def object_custom_tracking():
    #print("Tracking")
    global frame

    # Send box to tracker
    global face_box
    global tracker
    tracker_test = tracker.init( frame,face_box)

    # Calculate
    tracker_test, face_box = tracker.update(frame)

    # Display tracker box
    if tracker_test:
        # Tracking success
        topLeft = (int(face_box[0]), int(face_box[1]))
        bottomRight = (int(face_box[0] + face_box[2]), int(face_box[1] + face_box[3]))
        cv2.rectangle(frame, topLeft,bottomRight, (255,0,0), 2,1 )


# Detect_facial_features
#
# Detects and shows some facial features
#
#
def detect_facial_features():
    global frame

     #Add facial landmarks
    global face_landmarks_list
    face_landmarks_list = face_recognition.face_landmarks(frame)

    #Show some landmarks
    for face_landmarks in face_landmarks_list:
        cv2.line(frame, face_landmarks['left_eyebrow'][0], face_landmarks['left_eyebrow'][4],(68, 54, 39), 5)
        cv2.line(frame, face_landmarks['right_eyebrow'][0], face_landmarks['right_eyebrow'][4],(68, 54, 39), 5)
        cv2.line(frame, face_landmarks['top_lip'][0], face_landmarks['top_lip'][4],(68, 54, 39), 5)
        cv2.line(frame, face_landmarks['bottom_lip'][0], face_landmarks['bottom_lip'][4],(68, 54, 39), 5)
        cv2.line(frame, face_landmarks['left_eye'][0], face_landmarks['left_eye'][4],(68, 54, 39), 5)
        cv2.line(frame, face_landmarks['right_eye'][0], face_landmarks['right_eye'][4],(68, 54, 39), 5)

# Object_detection
# @ returns True if detections successful
# @ returns False if no face found
#
# This function uses dlib to make a face detection.
# Then transform the result to OpenCV
#
def object_detection():
    #print("Detection")
    global face_box
    global FaceDetector
    global frame
    global face_found

    # Detect and show facial_features
    detect_facial_features()

    # Ordinary Detection
    box_arr = FaceDetector(frame, 0)

    # No face
    if(not len(box_arr) ):
        face_found = False
        return False

    # Convert box to OpenCV
    face_box = convert_dlib_box_to_openCV_box(box_arr[0])

    print(face_box)

    # if running custom tracker this is needed
    update_custom_tracker()

    face_found = True
    return True

# Convert_dlib_box_to_OpenCV_box(box)
# @param takes in a dlib box
# @return returns a box for OpenCV
def convert_dlib_box_to_openCV_box(box):
    return (int(box.left()), int(box.top()), int(box.right() - box.left()),
                         int(box.bottom() - box.top()) )

# Run
# Running loop of program
def run():
    while True:
        if cam_cap.isOpened():

            # Get current frame
            global frame
            ret, frame = cam_cap.read()


            # Count tick
            global ticks
            ticks = ticks + 1

            # Do detection
            global DETECTION_SLEEP_TICKS
            if DETECTION_SLEEP_TICKS <= ticks:

                # if face found
                if object_detection():
                    ticks = 0
                    global FAST_DETECTION_SLEEP_TICKS
                    DETECTION_SLEEP_TICKS = FAST_DETECTION_SLEEP_TICKS
                else:
                    # Make less detections if not
                    ticks = 0
                    global SLOW_DETECTION_SLEEP_TICKS
                    DETECTION_SLEEP_TICKS = SLOW_DETECTION_SLEEP_TICKS
            else:
                # Do tracking
                if face_found:
                    #object_CamShift_tracking()
                    object_custom_tracking()

            #Show Cam
            cv2.imshow('Detection GUI', frame)

            #Close Program functionallity
            if cv2.waitKey(25) & 0xFF == ord('q'):
                cam_cap.release()
                cv2.destroyAllWindows()
                break

            time.sleep(0.2) # Sleep

            frame_listener.set(frame) # notify all



          #  LOG.log(threading.enumerate(), "SYSTEM")

# End Class

# Main function
def main():
    LOG.log("Starting system", "SYSTEM")
    LOG.log("Setting up system", "SYSTEM")
    init()  # Set up init

    LOG.log("System is running", "SYSTEM")
    run()   # run loop



# Starts Program here!
if __name__ == '__main__':
    main()

if cam_cap != None:
    cam_cap.release()
    cv2.destroyAllWindows()
