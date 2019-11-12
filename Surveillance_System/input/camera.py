import cv2
import threading


class camera(threading.Thread):

    def __init__(self, shared_variables, address):
        super(camera, self).__init__()
        self.address = address
        self.shared_variables = shared_variables

    def run(self):
        cap = cv2.VideoCapture(self.address)

        while True:
            ret, frame = cap.read()

            self.shared_variables.frame = frame
