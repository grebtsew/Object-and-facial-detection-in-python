import cv2
import dlib
import threading
import numpy as np
from keras.models import load_model
from scipy.spatial import distance as dist
from imutils import face_utils
import sys


# Blink detector
# Class that calcualte blink frequence
#
class Blink_frequency(threading.Thread):
    
    
    # Initiate thread
    # parameters name , shared_variables reference
    #
    def __init__(self, name = None,  shared_variables = None):
        threading.Thread.__init__(self)
        self.name = name
        self.shared_variables = shared_variables

    # make this run at correct time
    def run(self):

        print("loading model")
        model = load_model('model/blinkModel.hdf5')
        print("model loaded")
        print("start detection")

        close_counter = blinks = mem_counter= 0
        state = ''

        #Wait for detection
        while self.shared_variables.detection_frame is None:
            pass

        
        
        while self.shared_variables.detection_frame is not None:

            if self.shared_variables.tracking_running:
                
                frame = self.shared_variables.detection_frame

                eyes = self.cropEyes(frame)
                if eyes is None:
                    continue
                else:
                    left_eye,right_eye = eyes
                    #cv2.imshow('sd',left_eye)
                
                prediction = (model.predict(self.cnnPreprocess(left_eye)) + model.predict(self.cnnPreprocess(right_eye)))/2.0

                if prediction > 0.5 :
                    state = 'open'
                    close_counter = 0
                else:
                    state = 'close'
                    close_counter += 1

                if state == 'open' and mem_counter > 1:
                    blinks += 1

                mem_counter = close_counter 

                #save blinking

                #blinks
                #state
                #print (state)
                #print (blinks)
           

        pass

    # make the image to have the same format as at training 
    def cnnPreprocess(self,img):
        img = img.astype('float32')
        img /= 255
        img = np.expand_dims(img, axis=2)
        img = np.expand_dims(img, axis=0)
        return img
    

    def cropEyes(self,frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        shape = self.shared_variables.landmarks

        (rStart, rEnd) = face_utils.FACIAL_LANDMARKS_IDXS["left_eye"]
        (lStart, lEnd) = face_utils.FACIAL_LANDMARKS_IDXS["right_eye"]
        
        leftEye = shape[lStart:lEnd]
        rightEye = shape[rStart:rEnd]

        l_uppery = min(leftEye[1:3,1])
        l_lowy = max(leftEye[4:,1])
        l_dify = abs(l_uppery - l_lowy)

        lw = (leftEye[3][0] - leftEye[0][0])

        minxl = (leftEye[0][0] - ((34-lw)/2))
        maxxl = (leftEye[3][0] + ((34-lw)/2))
        minyl = (l_uppery - ((26-l_dify)/2))
        maxyl = (l_lowy + ((26-l_dify)/2))

        left_eye_rect = np.rint([minxl, minyl, maxxl, maxyl])
        left_eye_rect = left_eye_rect.astype(int)
        left_eye_image = gray[(left_eye_rect[1]):left_eye_rect[3], (left_eye_rect[0]):left_eye_rect[2]]

        r_uppery = min(rightEye[1:3,1])
        r_lowy = max(rightEye[4:,1])
        r_dify = abs(r_uppery - r_lowy)
        rw = (rightEye[3][0] - rightEye[0][0])
        minxr = (rightEye[0][0]-((34-rw)/2))
        maxxr = (rightEye[3][0] + ((34-rw)/2))
        minyr = (r_uppery - ((26-r_dify)/2))
        maxyr = (r_lowy + ((26-r_dify)/2))
        right_eye_rect = np.rint([minxr, minyr, maxxr, maxyr])
        right_eye_rect = right_eye_rect.astype(int)
        right_eye_image = gray[right_eye_rect[1]:right_eye_rect[3], right_eye_rect[0]:right_eye_rect[2]]

        if 0 in left_eye_image.shape or 0 in right_eye_image.shape:
            return None

        left_eye_image = cv2.resize(left_eye_image, (34, 26))
        right_eye_image = cv2.resize(right_eye_image, (34, 26))
        right_eye_image = cv2.flip(right_eye_image, 1)
        return left_eye_image, right_eye_image 

    

