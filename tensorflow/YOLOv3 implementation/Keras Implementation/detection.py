
'''
Helpful functions
'''

import sys
import tensorflow as tf
import cv2
import threading

from yolo_v3 import Yolo_v3
from utils import load_images, load_class_names, draw_boxes, draw_frame

'''
Variables
'''
_MODEL_SIZE = (416, 416)
_CLASS_NAMES_FILE = 'coco.names'
_MAX_OUTPUT_SIZE = 20
confidence_threshold = 0.5
iou_threshold = 0.5
model_path = "../../../../model/model.ckpt"

#Detection
# Class that handle detection in own thread
class Detection(threading.Thread):
    # Thread sleep times
    sleep_time = 0.1
    LONG_SLEEP = 2
    SHORT_SLEEP = 0.5

    Loaded_model = False

    # Initiate thread
    # parameters name, and shared_variables reference
    def __init__(self, name=None,  shared_variables = None):
        threading.Thread.__init__(self)
        self.name = name
        self.shared_variables = shared_variables
        self.sleep_time = self.SHORT_SLEEP
        #self.model_path = self.get_model_path()

    def load_model(self):
        self.shared_variables.class_names = load_class_names(_CLASS_NAMES_FILE)
        self.shared_variables.n_classes = len(self.shared_variables.class_names)
        self.shared_variables.model_size = _MODEL_SIZE

        model = Yolo_v3(n_classes=self.shared_variables.n_classes, model_size=_MODEL_SIZE,
                        max_output_size=_MAX_OUTPUT_SIZE,
                        iou_threshold=iou_threshold,
                        confidence_threshold=confidence_threshold)

        self.inputs = tf.placeholder(tf.float32, [1, *_MODEL_SIZE, 3])
        self.detections = model(self.inputs, training=False)
        return tf.train.Saver(tf.global_variables(scope='yolo_v3_model'))

    #Run
    def run(self):

        saver = self.load_model()

        with tf.Session() as sess:
            saver.restore(sess, model_path)



            try:
                while True:
                    if self.shared_variables.frame is not None:

                        resized_frame = cv2.resize(self.shared_variables.frame, dsize=_MODEL_SIZE[::-1],
                                                   interpolation=cv2.INTER_NEAREST)
                        self.shared_variables.detection_result = sess.run(self.detections,
                                                    feed_dict={self.inputs: [resized_frame]})

            finally:
                cv2.destroyAllWindows()
                print('Detections have been saved successfully.')
