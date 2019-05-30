import sys
import argparse
from yolo import YOLO, detect_video
from PIL import Image

import numpy as np

import cv2

def Cv2ToPil(frame):
    #cv2 to image
    cv2_im = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
    pil_im = Image.fromarray(cv2_im)
    return pil_im

def PilToCv2(im):
    #pil to  cv2
    # PIL RGB 'im' to CV2 BGR 'imcv'
#    imcv = np.asarray(im)[:,:,::-1].copy()
    # Or
    imcv = cv2.cvtColor(np.asarray(im), cv2.COLOR_RGB2BGR)

    # To gray image
#    imcv = np.asarray(im.convert('L'))
    # Or
#    imcv = cv2.cvtColor(np.asarray(im), cv2.COLOR_RGB2GRAY)
    return imcv

def detect_img(yolo):
    cap = cv2.VideoCapture(0)
    while True:
        try:
            ret, image = cap.read()

        except:
            print('Open Error! Try again!')
            continue
        else:
            r_image = yolo.detect_image(Cv2ToPil(image))
            cv2.imshow("test", PilToCv2(r_image))
            cv2.waitKey(1)
            #r_image.show()
    yolo.close_session()

FLAGS = None

if __name__ == '__main__':

    detect_img(YOLO())
