import tempfile
import time
import os
import cv2
from threading import Thread

"""
lets ignore the tempfile implementation for now.
"""

def simple_test():
    print(tempfile.tempdir)
    print(os.path.dirname(os.getcwd()) + "\\tmp")
    tempfile.tempdir = os.path.dirname(os.getcwd()) + "\\tmp"
    print(tempfile.tempdir)

    fp = tempfile.NamedTemporaryFile()
    fp.write(b'Hello world!')
    # read data from file
    fp.seek(0)
    print(fp.read())
    # close the file, it will be removed
    time.sleep(1)
    fp.close()

def read_and_save_webcam_image_in_temp():
    cap = cv2.VideoCapture(0)
    tmp = None
    while True:
        ret,frame = cap.read()
        if tmp is None:
            tmp = TempFile()
            tmp.create("video_test")
        tmp.write(frame)


def video_test():
    thread = Thread(target = read_and_save_webcam_image_in_temp)
    thread.start()

    tmp = None
    while True:
        if tmp is None:
            try:
                cap = cv2.VideoCapture('../tmp/video_test.avi')
            except Exception as e:
                pass

        else:
            ret, frame = cap.read()
            if ret == True:
                # Display the resulting frame
                cv2.imshow('Frame',frame)

                # Press Q on keyboard to  exit
                if cv2.waitKey(25) & 0xFF == ord('q'):
                  break


class TempFile(Thread):
    """
    A Tempfile is a file that will store temporary data, and will be removed the second the resources are no longer needed.
    In this implementation we will use this with our videos in order to no fill the harddrive during execution.
    We will need to make sure both parties are done before clearing temp files.
    """
    file = None
    path = None
    name = None
    frame = None
    def __init__(self):
        super(TempFile, self).__init__()
        temp_dir = os.path.dirname(os.getcwd()) + "\\tmp"
        # if tempdir don't exist, create folder
        try:
            os.stat(temp_dir)
        except:
            os.mkdir(temp_dir)
        # set our tempdir
        tempfile.tempdir = temp_dir
        self.path = temp_dir

    def create(self, name):
        self.file = cv2.VideoWriter(self.path+"\\"+name+'.avi',cv2.VideoWriter_fourcc('M','J','P','G'), 10, (640,480))
        self.name = name

    def write(self, frame):
        self.file.write(frame)     # save frame as JPEG file

        # Will write frame to video file
        #self.frame = frame

    def close(self):
        if self.file is not None:
            self.file.close()
            os.remove(self.path)

simple_test()
video_test()
