# This Code uses tensorflow detection and various tracking models to track one person at a time from webcam

#own imports
import detect_and_align
import threading
import time
from tensorflow.python.platform import gfile
import logging_data as LOG
import sys
import os
import numpy as np
import re

# tracker imports
import cv2

# detection import
import tensorflow as tf

tracker = None
face_landmarks_list = None
face_found = False
ticks = 0
DETECTION_SLEEP_TICKS = 0   # Constant
FAST_DETECTION_SLEEP_TICKS = 10   # Constant
SLOW_DETECTION_SLEEP_TICKS = 10   # Constant
cam_cap = None
face_box = None
FaceDetector = None
frame = None

#variables from tensorflow
pnet = None
rnet = None
onet = None
model_path = 'model/20170512-110547.pb'
show_landmarks = True
show_bb = True
show_fps = True
images_placeholder = None
embeddings = None
phase_train_placeholder = None



# Own Implementation Class


# Init
#
# Initiate function variables and functions
#
def init():
    global cam_cap
    cam_cap = cv2.VideoCapture(0) # capture webcam

    # needed for custom tracking
    update_custom_tracker()


    pass

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


# Convert_tensorflow_box_to_OpenCV_box(box)
# @param takes in a dlib box
# @return returns a box for OpenCV
def convert_tensorflow_box_to_openCV_box(box):
    return (box[0], box[1], box[2] - box[0], box[3] - box[1])

# Run
# Running loop of program
def run():
    with tf.Session() as sess:

        LOG.log("Loading modell","SYSTEM")
        #temp test
        global pnet
        global rnet
        global onet
        global images_placeholder
        global embeddings
        global phase_train_placeholder

        pnet, rnet, onet = detect_and_align.create_mtcnn(sess, None)

        model_exp = os.path.expanduser(model_path)
        if (os.path.isfile(model_exp)):
           # print('Model filename: %s' % model_exp)
            with gfile.FastGFile(model_exp, 'rb') as f:
                graph_def = tf.GraphDef()
                graph_def.ParseFromString(f.read())
                tf.import_graph_def(graph_def, name='')

        images_placeholder = tf.get_default_graph().get_tensor_by_name("input:0")
        embeddings = tf.get_default_graph().get_tensor_by_name("embeddings:0")
        phase_train_placeholder = tf.get_default_graph().get_tensor_by_name("phase_train:0")


        # set up tensorflow model
        #load_model(model_path)

        LOG.log("Start system","SYSTEM")
        while True:

            if cam_cap.isOpened():
                start = time.time()
                # Get current frame
                global frame
                ret, frame = cam_cap.read()


                # Count tick
                global ticks
                ticks = ticks + 1

                # Do detection
                global DETECTION_SLEEP_TICKS
                if DETECTION_SLEEP_TICKS <= ticks:

                 #print("Detection")
                    global face_box
                    global face_found

                    global show_id
                    global show_bb
                    global show_landmarks

                    # Do detection
                    face_patches, padded_bounding_boxes, landmarks = detect_and_align.align_image(frame, pnet, rnet, onet)

                    # if found faces
                    if len(face_patches) > 0:
                        face_patches = np.stack(face_patches)
                        feed_dict = {images_placeholder: face_patches, phase_train_placeholder: False}

                        embs = sess.run(embeddings, feed_dict=feed_dict)

                       # print('Matches in frame:')
                        for i in range(len(embs)):
                            bb = padded_bounding_boxes[i]

                            if show_bb:
                                cv2.rectangle(frame, (bb[0], bb[1]), (bb[2], bb[3]), (255, 0, 0), 2)

                            if show_landmarks:
                                for j in range(5):
                                    size = 1
                                    top_left = (int(landmarks[i, j]) - size, int(landmarks[i, j + 5]) - size)
                                    bottom_right = (int(landmarks[i, j]) + size, int(landmarks[i, j + 5]) + size)
                                    cv2.rectangle(frame, top_left, bottom_right, (255, 0, 255), 2)

                        # Convert box to OpenCV

                        face_box = convert_tensorflow_box_to_openCV_box(padded_bounding_boxes[0])
                       # print (face_box)

                        # if running custom tracker this is needed
                        update_custom_tracker()

                        face_found = True
                        #return True


                    else:
                    # No face
                        face_found = False
                    #return False

                    # if face found



                    if face_found:
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
                        object_custom_tracking()

                # print fps
                end = time.time()

                seconds = end - start
                if seconds != 0:
                    fps = round(1 / seconds, 2)

                if show_fps:
                    font = cv2.FONT_HERSHEY_SIMPLEX
                    cv2.putText(frame, str(fps), (0, 100), font, 1, (255, 255, 255), 1, cv2.LINE_AA)


                #Show Cam
                cv2.imshow('Detection GUI', frame)

                #Close Program functionallity
                if cv2.waitKey(25) & 0xFF == ord('q'):
                    cam_cap.release()
                    cv2.destroyAllWindows()
                    break

                time.sleep(0.2) # Sleep

          #  frame_listener.set(frame) # notify all

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
