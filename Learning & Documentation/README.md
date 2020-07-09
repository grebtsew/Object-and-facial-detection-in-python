# Learning & Documentation
During my learning process of Object detection and AI I read a lot of articles and followed a few tutorials while also doing a couple of university courses on general AI usages. One reason I decided to create this repository was to help with the learning process for future generations. I have tried a couple of models for object and facial detection in python3. In this repo I share some of the problems and solutions I had during my learning process with some of my comments on the subject.Code in this folder cannot solo run but can be interesting to look at or copy into finished tutorials described below.
Make sure to read through all repo-readme files in the linked repos below and star repos you like.

In folder `Create Models in Tensorflow` I have also added a short tutorial on how to create your own models and neural networks ready to be served by `Tensorflow Serving`.

# This is my process of learning how to work with Tensorflow and later Dlib

## First tutorial
I found this beginner-friendly tutorial to be great, probably the best tutorial out there!
https://pythonprogramming.net/introduction-use-tensorflow-object-detection-api-tutorial/

Here you will learn how to: (video or text format tutorial)
* Install tensorflow, and what it is.
* Run object detection in images
* Run object detection realtime in webcam
* Train own models

This tutorial assume around this code: (1)

https://github.com/tensorflow/models

Which is the actual tensorflow opensource project!

After this tutorial you will have a fair idea about how to work with tensorflow. I recommend going through the entire tutorial.

## Further Testing and Facial detection, good practice
Now you know the basics of object detection.

At this time I wanted to look closer at `facial recognition` in `tensorflow` and found this: (2)

https://github.com/habrman/FaceRecognition

Repo (2) is a project using a model for facial detection and uses landmarks to find several features on the face.
The model from this repo can be used in the first tutorial too.

With this starting knowledge of how to detect faces and some attributes I wanted to take it to the next level.

And found this tutorial:
https://medium.com/@ageitgey/machine-learning-is-fun-part-4-modern-face-recognition-with-deep-learning-c3cffc121d78

And from there found out about `dlib`. And this repo: (3)
https://github.com/ageitgey/face_recognition

Here they use `face_recognition` import.

Another model i tried is openFace, with both dlib and tensorflow. Found here:
https://github.com/ColeMurray/medium-facenet-tutorial

You can also look at `OpenCV` object detection about now. Just Google and you will find suitable examples. The reason you should wait with this implementation is that `OpenCV` has abstracted and made the process more automatic which makes it easier to create but harder to understand!

# Object Tracking and reaching higher performance

To achive a object detection with much greater performance we can look at object tracking and detection. (4)

https://github.com/inayatkh/tracking-python3

This is a repo using `OpenCV` for `tracking and face recognition` with great examples. Note that one example runs
object detection at really high speed. Find out how, here:

https://www.learnopencv.com/object-tracking-using-opencv-cpp-python/

In this article they explain how object tracking works.

From here on you probably have a great overall competence of object and facial detection
You are ready to create your own content.

# Motion Detection to boost detection precision

By adding motion detection algorithms we can find fast moving objects that might be impossible for the object detection to detect on an image.

Opencv contains several functions for handling motion detection.
Motion detection has been added to some of my example programs.

Some useful links to understand what motion detection is:
* [https://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_video/py_bg_subtraction/py_bg_subtraction.html](https://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_video/py_bg_subtraction/py_bg_subtraction.html)
* [https://www.pyimagesearch.com/2015/05/25/basic-motion-detection-and-tracking-with-python-and-opencv/](https://www.pyimagesearch.com/2015/05/25/basic-motion-detection-and-tracking-with-python-and-opencv/)

# Speed up execution with multithreading

By multithreading a solution we can achive a better result. The program will not lock while detecting and the user will have a better experience.
Some examples of multithreading can be found in my example programs.

# Boost result smoothness with Kalman-filters

The results can also be influenced by adding filters and thresholds. One of the prefered filters to use are the Kalman filter. This filter will need some initiation values for boxes and will make the boxes move smooth over fast transactions.
Examples of kalman filters are added to my example programs.

# Speeding up your models
The performance of detections can also be greatly increased by teaching your model or implementing the right kind of architecture for your situation. Here you will have to make a compromise between speed, memory and precision of detections. Some great models I would recommend are:

* `Yolo` (You Only Look Once) 1,2,3 and so on - This is probably the fastest one, here is an implementation in tensorflow:

https://github.com/xiaochus/YOLOv3
https://github.com/qqwweee/keras-yolo3

* `SSD` (Single Shot Detection) - A fast mobile designed model with low precision.

* `Mask-RCNN` - A model that also masks detections:

https://github.com/matterport/Mask_RCNN

# Why different models?
As mentioned above it can be a performance boost. Another great advantage of selecting your model carefully is the variants of usage. In some neural networks we don't want to classify objects, or detect faces. Sometimes we want to detect facial details like with the MTCNN model above. I would recommend reading some papers on the matter before deciding which model to use.

# Dlib or Tensorflow or something else?
A great amount of different machine learning projects exist today some of the more common would be caffe, Dlib, tensorflow, opencv, darknet and so on. Each project have its own advantages and disadvantages. Tensorflow is often ranked the best because of its scalability and huge application scope. Tensorflow also support machine learning and training of own models. My favorite advantage of tensorflow would be the production capability that tensorflow serving model server supports. Dlib is more strict to preinstalled models just like opencv and not as easy to implement in huge scales. My opinion is therefore that Tensorflow at current stage is the most complete ai project, but this can change rapidly.

# Other functions
I have looked closer at some extra functions used with facial detections, here are some great repos:
* `Blink detector` : https://github.com/iparaskev/simple-blink-detector
* `Expression detector` : https://github.com/JostineHo/mememoji
* `age/gender estimation` : https://github.com/yu4u/age-gender-estimation

# Own implementation
In folders `../"tensorflow"/"dlib"/"OpenCV"` (in root folder) I have combined some code from the repos linked above to create a customable python script using `face-detection`, `face-recognition` and `object-tracking`. The result is realtime facial features detection with `OpenCV` tracking to boost performance. One solution for `tensorflow` detection, one solution for `dlib` detection and one solution for `OpenCV` detection. The tracking models can be easily changed.
