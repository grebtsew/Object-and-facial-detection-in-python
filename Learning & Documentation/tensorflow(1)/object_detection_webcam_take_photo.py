print ("Import libraries...")

import numpy as np
import os
import six.moves.urllib as urllib
import sys
import tarfile
import tensorflow as tf
import zipfile
import time

from collections import defaultdict
from io import StringIO
from matplotlib import pyplot as plt
from PIL import Image

from Own_Code import create_xml as xml

import ctypes

import cv2

print ("Start and capture camera...")

cap = cv2.VideoCapture(0)

# This is needed since the notebook is stored in the object_detection folder.
sys.path.append("..")


# ## Object detection imports
# Here are the imports from the object detection module.

# In[3]:

from utils import label_map_util

from utils import visualization_utils as vis_util


# # Model preparation 

# ## Variables
# 
# Any model exported using the `export_inference_graph.py` tool can be loaded here simply by changing `PATH_TO_CKPT` to point to a new .pb file.  
# 
# By default we use an "SSD with Mobilenet" model here. See the [detection model zoo](https://github.com/tensorflow/models/blob/master/object_detection/g3doc/detection_model_zoo.md) for a list of other models that can be run out-of-the-box with varying speeds and accuracies.

# In[4]:


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

# In[6]:


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


# save image
SAVE_FOLDER = 'test_taken_pictures/'
CREATE_XML_FILE = False


def open_LabelImg():
  result = ctypes.windll.user32.MessageBoxW(None, "Do you want to start LabelImg to manuelly detect?", "No detections found.", 4)
  if result == 6:
    PATH_TO_LABELIMG = "../../../../labelImg-master/labelImg.py"
    print ("Opening LabelImg")
    command = ''.join(['python ', PATH_TO_LABELIMG, ' ',SAVE_FOLDER,filename]) 
    os.system(command)
  elif result == 7:
    print ("No XML file created")
  return


# # Detection and actual loop


with detection_graph.as_default():
  with tf.Session(graph=detection_graph) as sess:
    while True:
      ret, image_np = cap.read()
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


       # Save image file
      if cv2.waitKey(25) & 0xFF == ord('a'):
        # Save picture
         filename = ''.join([time.strftime('%Y-%m-%d-%H-%M-%S'), '.png'])
         print("Created file %s" % (''.join([SAVE_FOLDER, filename])))                        
         cv2.imwrite(''.join([SAVE_FOLDER,filename]),image_np);
         CREATE_XML_FILE = True
        
      
      # Visualization of the results of a detection.
      vis_util.visualize_boxes_and_labels_on_image_array(
          image_np,
          np.squeeze(boxes),
          np.squeeze(classes).astype(np.int32),
          np.squeeze(scores),
          category_index,
          use_normalized_coordinates=True,
          line_thickness=8)

      DETECTION = False

      if CREATE_XML_FILE:
        #Initiate xml struct for training
          detect_box_array = []
          height, width, channels = image_np.shape
     
      # Log detection result
          print (time.strftime('%d/%m/%Y %H:%M:%S'))

         

          if len(range(min(20, np.squeeze(boxes).shape[0]))) == 0:
            # ask question to start ImgLabel
            print("No boxes found")
            open_LabelImg()
            continue;
            
          for i in range(min(20, np.squeeze(boxes).shape[0])):
        
            if int(100*np.squeeze(scores)[i]) >= 50:
              DETECTION = True
              print (" %s : %s "  % (category_index[np.squeeze(classes).astype(np.int32)[i]]['name'], int(100*np.squeeze(scores)[i])) + "%" )
              ymin = boxes[0][i][0]*height
              xmin = boxes[0][i][1]*width
              ymax = boxes[0][i][2]*height
              xmax = boxes[0][i][3]*width

           #   print ("ymin=%s xmin=%s ymax=%s xmax=%s"  % (ymin, xmin, ymax, xmax ))

          # needed for xml creaton
              new_box = xml.detected_object()
              new_box.name = category_index[np.squeeze(classes).astype(np.int32)[i]]['name']
              new_box.pose = "Unspecified"
              new_box.truncated = 0
              new_box.difficult = 0
              new_box.positions = [ymin, xmin, ymax, xmax]
              detect_box_array.append(new_box);

          if DETECTION:
            xml.create_training_xml(SAVE_FOLDER,
                              filename,
                              ''.join([os.getcwd(),'/', SAVE_FOLDER, filename]),
                              'Unknown',
                              width,
                              height,
                              len(boxes.shape),
                              0,
                              detect_box_array,
                              SAVE_FOLDER)

            print("Created file %s" % (''.join([SAVE_FOLDER,'/', filename])))                        
            
          else:
            print("NO DETECTIONS")
            open_LabelImg()
          CREATE_XML_FILE = False;
      

      # Log detection result
      #print (time.strftime('%d/%m/%Y %H:%M:%S'))
      #for i in range(min(20, np.squeeze(boxes).shape[0])):
      #  if int(100*np.squeeze(scores)[i]) >= 50:
      #    print (" %s : %s "  % (category_index[np.squeeze(classes).astype(np.int32)[i]]['name'], int(100*np.squeeze(scores)[i])) + "%" )

     

      cv2.imshow('object detection', cv2.resize(image_np, (1600,900)))
      if cv2.waitKey(25) & 0xFF == ord('q'):
        cv2.destroyAllWindows()
        break

