import numpy as np
import cv2
from func.expression import model
import os
import tensorflow as tf
import threading

import utils.logging_data as LOG

'''
Expression calculate expression on face.
This program currently takes some minutes to start!
Make sure models are reachable!
Assumes from:
https://github.com/barkdong123/face_expression_detector
'''

class Expression(threading.Thread):

    index = 0
    # Initiate thread
    # parameters name , shared_variables reference

    def __init__(self, name = None,  shared_variables = None, index = 0 ):
        threading.Thread.__init__(self)
        self.name = name
        self.shared_variables = shared_variables
        self.index = index


    def get_emotion_by_index(self,index):
        # 0=Angry, 1=Disgust, 2=Fear, 3=Happy, 4=Sad, 5=Surprise, 6=Neutral
        if index ==0:
            return "Angry"
        elif index ==1:
            return "Disgust"
        elif index ==2:
            return "Fear"
        elif index ==3:
            return "Happy"
        elif index ==4:
            return "Sad"
        elif index ==5:
            return "Surprise"
        elif index ==6:
            return "Neutral"
        else:
            return "Unregistered emotion"

    # make this run at correct time
    def run(self):
        LOG.info("Start expression "+str(self.index),"SYSTEM-"+self.shared_variables.name)

        face_cascade = cv2.CascadeClassifier('../../model/haarcascade_frontalface_default.xml')
        eye_cascade = cv2.CascadeClassifier('../../model/haarcascade_eye.xml')

        sess = tf.Session()

        face_expression_detector = model.Model()
        checkpoint_save_dir = os.path.join("../../model/checkpoint")
        face_expression_detector.load_graph(sess,checkpoint_save_dir)


        preferred_w,preferred_h = 800,600
        sentiment_argmax = 0
        res = np.array([[0]])

        sentiment_arr =[]

        while True:
            #ret,frame = cap.read()
            frame = self.shared_variables.frame[self.index]
            frame_height, frame_width = frame.shape[:2]

            frame = cv2.resize(frame,None,fx=preferred_w/ frame_width,fy=preferred_h/frame_height,interpolation=cv2.INTER_CUBIC)
            frame_height, frame_width = frame.shape[:2]

            grayed = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(grayed,1.3,5)
            for x,y,w,h in faces:
                cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),2)
                roi_gray = grayed[y:y+h,x:x+w]
                roi_color = frame[y:y+h,x:x+w]

                desired_h, desired_w = 48, 48
                resized_ratio_h, resized_ratio_w = desired_h / h, desired_w / w
                res = cv2.resize(roi_gray, None, fx=resized_ratio_w, fy=resized_ratio_h, interpolation=cv2.INTER_CUBIC)

                res = np.reshape(res,(-1,2304))

                feed_dict = {face_expression_detector.X:res,face_expression_detector.keep_prob:1}
                sentiment_arr = np.array(sess.run(face_expression_detector.softmax_logits, feed_dict=feed_dict))
                sentiment_arr = sentiment_arr[0]
                sentiment_argmax = np.argmax(sentiment_arr,axis=0)
                res = np.reshape(res,(48,48))


            self.shared_variables.expression_result[self.index] = sentiment_arr
            self.shared_variables.face_image[self.index] = res
        sess.close()
        LOG.info("Close expression " + str(self.index), "SYSTEM-"+self.shared_variables.name)
