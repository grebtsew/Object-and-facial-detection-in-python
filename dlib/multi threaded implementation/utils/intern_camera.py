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
    
    def __init__(self, shared_variables = None):
        threading.Thread.__init__(self)
        self.shared_variables = shared_variables
        
    def run(self):
        while self.shared_variables.detection_running:
            if self.shared_variables.camera_capture.isOpened():
                temp, frame = self.shared_variables.camera_capture.read() 

               

                # flipp if needed
                if self.shared_variables.flipp_test:
                    self.shared_variables.frame = imutils.rotate(frame, self.shared_variables.flipp_test_degree)
                else: 
                    self.shared_variables.frame = frame
                





