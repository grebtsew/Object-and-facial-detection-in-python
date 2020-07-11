from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import tensorflow as tf
from tensorflow.python.platform import gfile
import numpy as np
import sys
import os
import detect_and_align
#import id_data
from scipy import misc
import re
import cv2
import argparse
import time
import tensorflow.compat.v1 as tf
tf.disable_v2_behavior()



def main():
   # with tf.Graph().as_default():
        with tf.Session() as sess:
            
            pnet, rnet, onet = detect_and_align.create_mtcnn(sess, None)

            #load_model('model/20170512-110547.pb')
            #Load model
            model_exp = os.path.expanduser('model/20170512-110547.pb')
            if (os.path.isfile(model_exp)):
                print('Model filename: %s' % model_exp)
                with gfile.FastGFile(model_exp, 'rb') as f:
                    graph_def = tf.GraphDef()
                    graph_def.ParseFromString(f.read())
                    tf.import_graph_def(graph_def, name='')
            # done loading
            
            images_placeholder = tf.get_default_graph().get_tensor_by_name("input:0")
            embeddings = tf.get_default_graph().get_tensor_by_name("embeddings:0")
            phase_train_placeholder = tf.get_default_graph().get_tensor_by_name("phase_train:0")            

            cap = cv2.VideoCapture(0)
            frame_height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)

            show_landmarks = True
            show_bb = True
            show_id = False
            show_fps = True
            
            while(True):
                start = time.time()
                _, frame = cap.read()

                face_patches, padded_bounding_boxes, landmarks = detect_and_align.align_image(frame, pnet, rnet, onet)

                if len(face_patches) > 0:
                    face_patches = np.stack(face_patches)
                    feed_dict = {images_placeholder: face_patches, phase_train_placeholder: False}
                    embs = sess.run(embeddings, feed_dict=feed_dict)

                    print('Matches in frame:')
                    for i in range(len(embs)):
                        bb = padded_bounding_boxes[i]

                       
                        if show_id:
                            font = cv2.FONT_HERSHEY_SIMPLEX
                            cv2.putText(frame, matching_id, (bb[0], bb[3]), font, 1, (255, 255, 255), 1, cv2.LINE_AA)

                        if show_bb:
                            cv2.rectangle(frame, (bb[0], bb[1]), (bb[2], bb[3]), (255, 0, 0), 2)

                        if show_landmarks:
                            for j in range(5):
                                size = 1
                                top_left = (int(landmarks[i, j]) - size, int(landmarks[i, j + 5]) - size)
                                bottom_right = (int(landmarks[i, j]) + size, int(landmarks[i, j + 5]) + size)
                                cv2.rectangle(frame, top_left, bottom_right, (255, 0, 255), 2)
                else:
                    print('Couldn\'t find a face')

                end = time.time()

                seconds = end - start
                fps = round(1 / seconds, 2)

                if show_fps:
                    font = cv2.FONT_HERSHEY_SIMPLEX
                    cv2.putText(frame, str(fps), (0, int(frame_height) - 5), font, 1, (255, 255, 255), 1, cv2.LINE_AA)

                cv2.imshow('frame', frame)

                key = cv2.waitKey(1)
                if key == ord('q'):
                    break
            
            cap.release()
            cv2.destroyAllWindows()



if __name__ == '__main__':
    main()
