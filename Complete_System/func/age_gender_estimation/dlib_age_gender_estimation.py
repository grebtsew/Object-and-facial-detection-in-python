import os
import cv2
import dlib
import numpy as np
import argparse
import threading

from contextlib import contextmanager
from func.age_gender_estimation.wide_resnet import WideResNet
from keras.utils.data_utils import get_file

# Age Gender Estimation
# Class that calcualte Age and gender
#
class Age_gender_estimation(threading.Thread):

    pretrained_model_path = "model/weights.18-4.06.hdf5"
    
    # Initiate thread
    # parameters name , shared_variables reference
    #
    def __init__(self, name = None,  shared_variables = None):
        threading.Thread.__init__(self)
        self.name = name
        self.shared_variables = shared_variables
        

    def run(self):
        
        print("Load models")
        # load model and weights
        img_size = 64
        model = WideResNet(img_size, depth=16, k=8)()
        model.load_weights(self.pretrained_model_path)
        print("Models loaded")

        #wait for detection
        while self.shared_variables.detection_frame is None:
            pass

        img_size = 64

        while True:
            if self.shared_variables.tracking_running:
                input_img = cv2.cvtColor(self.shared_variables.detection_frame, cv2.COLOR_BGR2RGB)
                img_h, img_w, _ = np.shape(input_img)

                faces = np.empty((len([self.shared_variables.face_box]), img_size, img_size, 3))

        #print(self.face_box)

                w = self.shared_variables.face_box[0]
                h = self.shared_variables.face_box[1]
                x1 = self.shared_variables.face_box[2]
                y1 = self.shared_variables.face_box[3]
                x2 = w + x1
                y2 = h + y1
        
                xw1 = max(int(x1 - 0.4 * w), 0)
                yw1 = max(int(y1 - 0.4 * h), 0)
                xw2 = min(int(x2 + 0.4 * w), img_w - 1)
                yw2 = min(int(y2 + 0.4 * h), img_h - 1)

                faces[0, :, :, :] = cv2.resize(self.shared_variables.frame[yw1:yw2 + 1, xw1:xw2 + 1, :], (img_size, img_size))

        

        # predict ages and genders of the detected faces
                results = model.predict(faces)
                predicted_genders = results[0]
                ages = np.arange(0, 101).reshape(101, 1)
                predicted_ages = results[1].dot(ages).flatten()


        # Show

                print("Predicted age: " + str(predicted_ages[0]))

                if predicted_genders[0][0] > 0.5:
            
                    print("Predicted gender: " + "Female")
                else:
                    print("Predicted gender: " + "Male")

        
        #Short version
        
                label = "{}, {}".format(int(predicted_ages[0]),
                                        "F" if predicted_genders[0][0] > 0.5 else "M")
                print(label)

            
