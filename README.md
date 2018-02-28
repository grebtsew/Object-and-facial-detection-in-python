# Object-and-facial-detection-in-python
I have tried a couple of modells for object and facial detection i python. Here i share some knowledge and links.

In this repo I share some of the problems and solutions I had during my learning process.
Nothing in this repo can solo-run, but is intresting to look at or copy into finished tutorials descibed below. 
Make sure to read though all repo-readme files in the linked repos below.


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

# Own implementation
In folder "Own implementation" I have combinated some code from the repos linked above to create a customable python script using face-detection, face-recognition and object-tracking. The result is realtime facial features detection with OpenCV tracking to boost preformance. One solution for Tensorflow detection and one solution for dlib detection. The tracking models can be easily changed. 
