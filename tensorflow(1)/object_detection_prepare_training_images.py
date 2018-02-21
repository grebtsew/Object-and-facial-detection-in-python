print ("Import libraries...")

import numpy as np
import os, os.path
import six.moves.urllib as urllib
import sys
import tarfile
import tensorflow as tf
import zipfile
import time
from shutil import copyfile

from collections import defaultdict
from io import StringIO
from matplotlib import pyplot as plt
from PIL import Image

import cv2

# This is needed since the notebook is stored in the object_detection folder.
sys.path.append("..")

# ## Object detection imports
# Here are the imports from the object detection module.

from utils import label_map_util

from utils import visualization_utils as vis_util

from Own_Code import create_xml as xml


# # Model preparation 

# ## Variables
# 
# Any model exported using the `export_inference_graph.py` tool can be loaded here simply by changing `PATH_TO_CKPT` to point to a new .pb file.  
# 
# By default we use an "SSD with Mobilenet" model here. See the [detection model zoo](https://github.com/tensorflow/models/blob/master/object_detection/g3doc/detection_model_zoo.md) for a list of other models that can be run out-of-the-box with varying speeds and accuracies.

class file_path:
    def __init__(self):
        self.path = ""
        self.name = ""
       

# What model to download.
MODEL_NAME = 'ssd_mobilenet_v1_coco_11_06_2017'
MODEL_FILE = MODEL_NAME + '.tar.gz'
DOWNLOAD_BASE = 'http://download.tensorflow.org/models/object_detection/'

# Path to frozen detection graph. This is the actual model that is used for the object detection.
PATH_TO_CKPT = MODEL_NAME + '/frozen_inference_graph.pb'

# List of the strings that is used to add correct label for each box.
PATH_TO_LABELS = os.path.join('data', 'mscoco_label_map.pbtxt')

NUM_CLASSES = 90

# ## Load a (frozen) Tensorflow model into memory.

print ("Loading Modell...")
 
detection_graph = tf.Graph()
with detection_graph.as_default():
  od_graph_def = tf.GraphDef()
  with tf.gfile.GFile(PATH_TO_CKPT, 'rb') as fid:
    serialized_graph = fid.read()
    od_graph_def.ParseFromString(serialized_graph)
    tf.import_graph_def(od_graph_def, name='')


# ## Loading label map
# Label maps map indices to category names, so that when our convolution network predicts `5`, we know that this corresponds to `airplane`.  Here we use internal utility functions, but anything that returns a dictionary mapping integers to appropriate string labels would be fine

print ("Loading label map...")


label_map = label_map_util.load_labelmap(PATH_TO_LABELS)
categories = label_map_util.convert_label_map_to_categories(label_map, max_num_classes=NUM_CLASSES, use_display_name=True)
category_index = label_map_util.create_category_index(categories)


print ("Get files...")

# For the sake of simplicity we will use only 2 images:
# If you want to test the code with your images, just add path to the images to the TEST_IMAGE_PATHS.
PATH_TO_TEST_IMAGES_DIR = 'test_images'
TEST_IMAGE_PATHS = []

valid_images = [".jpg",".gif",".png",".tga"]

for files in os.listdir(PATH_TO_TEST_IMAGES_DIR):
  ext = os.path.splitext(files)[1]
  if ext.lower() not in valid_images:
    continue
  temp = file_path()
  temp.name = files
  temp.path = os.path.join(PATH_TO_TEST_IMAGES_DIR,files)
  TEST_IMAGE_PATHS.append(temp)
                              

# # Detection and actual loop

print("Detecting...")

with detection_graph.as_default():
  with tf.Session(graph=detection_graph) as sess:
   for image_path in TEST_IMAGE_PATHS:
    
      #print(image_path.path)
      image_np = cv2.imread(image_path.path)
      height, width, channels = image_np.shape
      
      
      # Expand dimensions since the model expects images to have shape: [1, None, None, 3]
      image_np_expanded = np.expand_dims(image_np, axis=0)
      image_tensor = detection_graph.get_tensor_by_name('image_tensor:0')
      # Each box represents a part of the image where a particular object was detected.
      boxes = detection_graph.get_tensor_by_name('detection_boxes:0')
      # Each score represent how level of confidence for each of the objects.
      # Score is shown on the result image, together with the class label.
      scores = detection_graph.get_tensor_by_name('detection_scores:0')
      classes = detection_graph.get_tensor_by_name('detection_classes:0')
      num_detections = detection_graph.get_tensor_by_name('num_detections:0')

      
      # Actual detection.
      (boxes, scores, classes, num_detections) = sess.run(
          [boxes, scores, classes, num_detections],
          feed_dict={image_tensor: image_np_expanded})

      
      # Visualization of the results of a detection.
      vis_util.visualize_boxes_and_labels_on_image_array(
          image_np,
          np.squeeze(boxes),
          np.squeeze(classes).astype(np.int32),
          np.squeeze(scores),
          category_index,
          use_normalized_coordinates=True,
          line_thickness=8)

      #Initiate xml struct for training
      detect_box_array = []
     
      # Log detection result
      print (time.strftime('%d/%m/%Y %H:%M:%S'))

       
      for i in range(min(20, np.squeeze(boxes).shape[0])):
        
        if int(100*np.squeeze(scores)[i]) >= 50:
          print (" %s : %s "  % (category_index[np.squeeze(classes).astype(np.int32)[i]]['name'], int(100*np.squeeze(scores)[i])) + "%" )
          ymin = boxes[0][i][0]*height
          xmin = boxes[0][i][1]*width
          ymax = boxes[0][i][2]*height
          xmax = boxes[0][i][3]*width

          print ("ymin=%s xmin=%s ymax=%s xmax=%s"  % (ymin, xmin, ymax, xmax ))

          # needed for xml creaton
          new_box = xml.detected_object()
          new_box.name = category_index[np.squeeze(classes).astype(np.int32)[i]]['name']
          new_box.pose = "Unspecified"
          new_box.truncated = 0
          new_box.difficult = 0
          new_box.positions = [ymin, xmin, ymax, xmax]
          detect_box_array.append(new_box);

      #print(os.path.abspath(image_path.path))
      #print(len(boxes.shape))
      #print(detect_box_array)

      #create training xml
      xml.create_training_xml('test_images',
                              image_path.name,
                              os.path.abspath(image_path.path),
                              'Unknown',
                              width,
                              height,
                              len(boxes.shape),
                              0,
                              detect_box_array,
                              'test_result')

      print("Created file %s" % (''.join(['test_result','/', image_path.name])))                        

      copyfile(image_path.path, ''.join(['test_result/',image_path.name]))
      print("Copied image to same directory for training.")
      
      cv2.imshow('object detection', image_np)
      cv2.waitKey()
