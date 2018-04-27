import sys
import os
import clr
import cv2
import numpy as np
import time
import threading

# import Ebus sdk files
#clr.AddReference(r'PvGUIDotNet')
#from PvGUIDotNet import *

#clr.AddReference(r'PvDotNet')
#from PvDotNet import *


#clr.AddReference(r'ClassLibrary2')
#from PvStreamSample import FLIR


class camera_stream(threading.Thread):
    
    ipaddress = '192.168.0.30'
    cam_inst = None
    

    def __init__(self, shared_variables = None): #shared_variables = None):
        threading.Thread.__init__(self)
        self.shared_variables = shared_variables

