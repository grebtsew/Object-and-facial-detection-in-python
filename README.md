# Facial-detection-and-functionallity-in-python

This repo contains, training material, dlib implementation and tensorflow implementation.
Too large files (mostly models) is ignored due to Github limitations, the models can be found in github-repos linked in learning folder readme.

# Training Material
See folder learning.
Here I show my learning process of object detection, facial detection and how to work with tensorflow and dlib. Repos used to develop code in this repo is linked in Learning-folder README.

# Dlib
See dlib folder.
Here I share a singel and multi threaded dlib solution for facial detection.
I am using code from several other repos with my code here.

This is how the dlib program look like during execution.
![Screenshot](images/tf_demo.png)

# Tensorflow
See tensorflow folder.
Here I share a singel and multi threaded tensorflow solution for facial detection and some functions like skin_color.
I am using code from several other repos with my code here.

This is how the tf program look like during execution.
![Screenshot](images/tf_demo.png)

# Complete System Implementation
This is my own implementation if a test system with a parse-controller. The system architecture is described by the image below. Here follows a short explaination of the architecture. Start starts the parseController that initiate the system. Shared_Variables is the Shared and centered node class that handle all data shared in the program. First of there is a read thread that reads images from a camera stream. These images are then sent to detection and tracking when renewed. The result is returned to shared_variables. Shared_variables then invoke the on_set_frame listener and execute activated functions on seperate threads. Last the frame is sent to Visualize class that show the image. This is a multithreaded implementation and I recommend to run it on a high preformance computer.

![Screenshot](images/arkitektur.png)


As seen in the arkitektur several extra functions has been added, those are :


* blink frequency - intresting to know if someone is tierd
* age/gender estimation - just for fun
* expressions - intresting to know if someone is struggling
* skincolor - to see if there are any skin color changes in realtime.


If it is hard to understand how to use the parse-controller type help or h for some extra information. Let me know if something is hard to understand.

/Grebtsew
