'''
A simple object detection implementation
'''

import math

from math import hypot
import tensorflow as tf
from object_detection.utils import label_map_util
import time
import numpy as np
from threading import Thread
import os

class Object_Detection(Thread):

    MODEL_NAME = 'ssd_mobilenet_v1_coco_11_06_2017'
    # Path to frozen detection graph. This is the actual model that is used for the object detection.
    PATH_TO_CKPT = 'object_detection/models/' + MODEL_NAME + '/frozen_inference_graph.pb'
    # List of the strings that is used to add correct label for each box.
    CWD_PATH = os.getcwd()
    PATH_TO_LABELS = os.path.join(CWD_PATH,'object_detection/object_detection', 'data', 'mscoco_label_map.pbtxt')
    NUM_CLASSES = 90
    boxes = None

    def __init__(self, model = 'ssd_mobilenet_v1_coco_11_06_2017/frozen_inference_graph.pb', name=None, shared_variables = None ):
        super(Object_Detection, self).__init__()
        self.name = name
        self.shared_variables = shared_variables
        self.id = id
        self.detection_graph = self.load_modell()
        self.label_map = label_map_util.load_labelmap(self.PATH_TO_LABELS)
        self.categories = label_map_util.convert_label_map_to_categories(self.label_map, max_num_classes=self.NUM_CLASSES, use_display_name=True)
        self.category_index = label_map_util.create_category_index(self.categories)
        self.shared_variables.categorylist = self.categories
        self.shared_variables.category_max = self.NUM_CLASSES
        self.shared_variables.category_index = self.category_index

        self.sess = tf.Session(graph=self.detection_graph)

        self.shared_variables.model_loaded = True # activate rest of the program
        print("Model Loaded successfully!")
        print("Detections Started!")


    def distance_between_boxes(self, box1, box2):
        return int(abs(math.hypot(box2[0]-box1[0], box2[1]-box1[1])))

    def box_exist(self, tracking_list, box):
        # if inside, replace!
        
        for t in tracking_list:
            if t is not None:
                if len(t.box) > 0:
                    if(self.distance_between_boxes(t.box, box)) < 100:
                        return True
        return False


    def load_modell(self):
        # Load modell
        print("Loading model")
        detection_graph = tf.Graph()
        with detection_graph.as_default():
            od_graph_def = tf.GraphDef()
            with tf.gfile.GFile(self.PATH_TO_CKPT, 'rb') as fid:
                serialized_graph = fid.read()
                od_graph_def.ParseFromString(serialized_graph)
                tf.import_graph_def(od_graph_def, name='')
        return detection_graph


    def run(self):
        while True:
            if self.shared_variables.frame is not None:
                if self.shared_variables.detection_lock:
                    frame = self.shared_variables.frame

                    if( frame is not None):
                        image_np = frame
                        # Expand dimensions since the model expects images to have shape: [1, None, None, 3]
                        image_np_expanded = np.expand_dims(image_np, axis=0)
                        image_tensor = self.detection_graph.get_tensor_by_name('image_tensor:0')
                        # Each box represents a part of the image where a particular object was detected.
                        boxes = self.detection_graph.get_tensor_by_name('detection_boxes:0')

                        # Each score represent how level of confidence for each of the objects.
                        # Score is shown on the result image, together with the class label.
                        scores = self.detection_graph.get_tensor_by_name('detection_scores:0')
                        classes = self.detection_graph.get_tensor_by_name('detection_classes:0')

                        num_detections = self.detection_graph.get_tensor_by_name('num_detections:0')

                        # Actual detection.
                        self.shared_variables.detection_box = self.sess.run(
                          [boxes, scores, classes, num_detections],
                          feed_dict={image_tensor: image_np_expanded})

                        detection_list = []
                        if self.shared_variables.detection_box is not None:
                            boxes = np.squeeze(self.shared_variables.detection_box[0])
                            scores = np.squeeze(self.shared_variables.detection_box[1])
                            classification = np.squeeze(self.shared_variables.detection_box[2])

                            # loop through all detections
                            detection_list = []
                            for i in range(0,len(np.squeeze(self.shared_variables.detection_box[0]))):
                                x = int((self.shared_variables.WIDTH)*boxes[i][1])
                                y = int((self.shared_variables.HEIGHT)*boxes[i][0])
                                w = int((self.shared_variables.WIDTH)*(boxes[i][3]-boxes[i][1]))
                                h = int((self.shared_variables.HEIGHT)*(boxes[i][2]-boxes[i][0]))
                                c = ""

                                # Check category in bounds
                                if len(self.shared_variables.categorylist) >= classification[i]:
                                    c = str(self.shared_variables.categorylist[int(classification[i]-1)]['name'])

                                if not c == "person":
                                    continue

                                if w*h > 10000000:
                                    continue

                                if scores[i] > 0.6:
                                    #detection_list.append(((x,y,w,h), c, scores[i]))
                                    if len(self.shared_variables.tracking_threads) > 0:
                                        if not self.box_exist(self.shared_variables.tracking_threads,(x,y,w,h)):

                                            self.shared_variables.tracking_threads.append(self.shared_variables.start_tracking_thread(frame, (x,y,w,h)))
                                    else:
                                        self.shared_variables.tracking_threads.append(self.shared_variables.start_tracking_thread(frame, (x,y,w,h)))
                                    #print("Found detection")

                        self.shared_variables.detection_lock = False

                else:
                    time.sleep(0.1)
