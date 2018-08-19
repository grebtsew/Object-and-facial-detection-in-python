# Object-and-facial-detection-in-python
I have tried a couple of models for object and facial detection i python. Here i share some knowledge and links.

In this repo I share some of the problems and solutions I had during my learning process.
Only code in Own_Implementation can solo-run, but other code can also be intresting to look at or copy into finished tutorials descibed below.
Make sure to read though all repo-readme files in the linked repos below and star repos you like.

# This is my process of learning how to work with Tensorflow and later Dlib

# First tutorial
I found this beginner-friendly tutorial to be great, propably the best tutorial out there!
https://pythonprogramming.net/introduction-use-tensorflow-object-detection-api-tutorial/

Here you will learn how to: (video or text format tutorial)
* Install tensorflow, and what it is.
* Run object detection in images
* Run object detection realtime in webcam
* Train own modells

This tutorial assume around this code: (1)
https://github.com/tensorflow/models

After this tutorial you will have a fair idea about how to work with tensorflow.

# Further Testing and Facial detection, good practice
Now you know the basics of object detection.

I wanted to look closer at facial recognition in tensorflow and found this: (2)
https://github.com/habrman/FaceRecognition

Repo (2) is a modell for facial detection and uses landmarks to find a couple of spots on the face.
The modell from this repo can be used in the first tutorial too.

With this starting knowledge of how to detect faces and some attributes I wanted to take it to the next level.
And found this tutorial:
https://medium.com/@ageitgey/machine-learning-is-fun-part-4-modern-face-recognition-with-deep-learning-c3cffc121d78

And from there found out about dlib. And this repo: (3)
https://github.com/ageitgey/face_recognition

Here they use face_recognition import.

Another modell i tried is openFace, with both dlib and tensorflow. Found here:
https://github.com/ColeMurray/medium-facenet-tutorial

# Object Tracking and reaching higher preformance

To achive a object detection with much greater preformance we can look at object tracking and detection. (4)
https://github.com/inayatkh/tracking-python3
This is a repo using OpenCV for tracking and face recognition with great examples. Note that one example runs
object detection at really high speed. Find out how, here:
https://www.learnopencv.com/object-tracking-using-opencv-cpp-python/
In this article they explain how object tracking works.

From here on you probably have a great overall competence of object and facial detection
You are ready to create your own content.

# Speeding up your models
The preformance of detections can also be greatly increased by teaching your model or implementing the right kind of architecture for your situation. Here you will have to make a compromise between speed, memory and precision of detections. Some great models i would recommend are:

* Yolo (You Only Look Once) - This is probably the fastest one, here is an implementation in tensorflow:
https://github.com/xiaochus/YOLOv3
https://github.com/qqwweee/keras-yolo3

* SSD (Single Shot Detection) - A fast mobile designed model with low precision.

* Mask-RCNN - A model that also masks detections:
https://github.com/matterport/Mask_RCNN

# Why different models?
As mentioned above it can be a preformance boost. Another great advantage of selecting your model carefully is the variants of usage. In some neural networks we dont want to classify objects, or detect faces and sometimes we want to detect facial details like with the MTCNN model liked above. I would recommend reading some papers on the matter before deciding what to use.

# Dlib or Tensorflow or something else?
A great amount of different machine learning projects exist today some of the more common would be caffe, Dlib, tensorflow, opencv, darknet and so on. Each project have its own advantages and disadvantages. Tensorflow is often ranked the best because of its scalability and huge application scope. Tensorflow also support machine learning and training of own models. My favorite advantage of tensorflow would be the production capability that tensorflow serving model server supports. Dlib is more strict to preinstalled models just like opencv and not as easy to implement in huge scales. My opinion is therefore that Tensorflow at current stage is the most complete ai project, but this can change rapidly.

# Other functions
I have looked closer at some extra functions used with facial detections, here are some great repos:
* Blink detector : https://github.com/iparaskev/simple-blink-detector
* Expression detector : https://github.com/JostineHo/mememoji
* age/gender estimation : https://github.com/yu4u/age-gender-estimation

# Own implementation
In folders "tensorflow"/"dlib" (in root folder) I have combinated some code from the repos linked above to create a customable python script using face-detection, face-recognition and object-tracking. The result is realtime facial features detection with OpenCV tracking to boost preformance. One solution for Tensorflow detection and one solution for dlib detection. The tracking models can be easily changed.
