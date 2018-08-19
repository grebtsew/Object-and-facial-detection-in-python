import cv2
import threading
import imutils

# Functions to calculate available cameras copied from
#https://stackoverflow.com/questions/7322939/how-to-count-cameras-in-opencv-2-3
def clearCapture(capture):
    capture.release()
    cv2.destroyAllWindows()

def countCameras():
    n = 0
    for i in range(10): # max 10 cams
        try:
            cap = cv2.VideoCapture(i)
            ret, frame = cap.read()
            cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            clearCapture(cap)
            n += 1
        except:
            clearCapture(cap)
            break
    return n


# Class Thread that reads camera stream, to make sure system only read camera stream once
class camera_stream(threading.Thread):
    start_time = None
    end_time = None
    grayscale = False
    capture = None

    def __init__(self, shared_variables = None, id = 0, index = 0):
        threading.Thread.__init__(self)
        self.id = id
        self.index = index
        self.shared_variables = shared_variables

    def capture(self):
        try:

            self.capture = cv2.VideoCapture(self.id)

        except Exception as e:
            print('Failed to capture camera')

    def run(self):

        self.capture()

        while self.shared_variables.system_running:
            if self.capture.isOpened():
                temp, frame = self.capture.read()

                # flipp if needed
                if self.shared_variables.flipp_test[self.index]:
                    self.shared_variables.frame[self.index] = imutils.rotate(frame, self.shared_variables.flipp_test_degree[self.index])
                else:
                    self.shared_variables.frame[self.index] = frame
