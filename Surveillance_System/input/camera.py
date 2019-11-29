import pafy
import threading
import time
import cv2

class camera(threading.Thread):


    def __init__(self, shared_variables, address):
        super(camera, self).__init__()
        self.address = address
        self.shared_variables = shared_variables

    def run(self):
        if str(self.address).__contains__("https"):
            vPafy = pafy.new(self.address)
            play = vPafy.getbest(preftype="webm")
            #start the video
            cap = cv2.VideoCapture(play.url)

        elif isinstance(self.address, int()) or str(self.address).__contains__("rtsp"):
            cap = cv2.VideoCapture(self.address)
            fps = cam.get(cv2.CAP_PROP_FPS)
            print("FPS", fps)

        doonce = False
        frame_counter = 0
        while True:

            if self.shared_variables.model_loaded:

                if not self.shared_variables.detection_lock :
                    ret, frame = cap.read()
                    frame_counter += 1

                    if not doonce:
                        doonce = True
                        h,w,c = frame.shape
                        self.shared_variables.WIDTH = w
                        self.shared_variables.HEIGHT = h
                        #print(h,w)

                    self.shared_variables.frame = frame #cv2.resize(frame, (640,640))

                    if frame_counter % 10 == 0:
                        self.shared_variables.detection_lock = True

            else:
                time.sleep(0.1)
