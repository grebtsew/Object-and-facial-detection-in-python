import cv2
import requests
import numpy as np
import threading

ip_adress_list = ['http://192.168.0.200:8080/video2.mjpg',
                  'http://192.168.1.242:8080/video']


def get_number_connected_cameras():
    global ip_adress_list
    c = 0

    for ip in ip_adress_list:
        try:
            r = requests.get(ip, auth=('admin', ''), stream=True)
            if(r.status_code == 200):
                c = c + 1
        except:
            pass

    return c

def get_connected_cameras():
    global ip_adress_list
    c = []

    for ip in ip_adress_list:
        try:
            r = requests.get(ip, auth=('admin', ''), stream=True)
            if(r.status_code == 200):
                c.append(ip)
        except:
            pass

    return c

class ip_camera_stream(threading.Thread):

    capture = None

    def __init__(self, shared_variables = None, address = "", index = 0):
        threading.Thread.__init__(self)
        self.shared_variables = shared_variables


    '''
    ----- RTSP solution -----
    '''
    def run(self):
        try:
            self.capture = cv2.VideoCapture("rtsp://admin:admin@192.168.0.10:554/live.sdp")
        except Exception as e:
            print("Could not open ip camera")
            return


        while self.shared_variables.system_running:
            if self.capture.isOpened():
                temp, frame = self.capture.read()

                # flipp if needed
                if self.shared_variables.flipp_test[self.index]:
                    self.shared_variables.frame[self.index] = imutils.rotate(frame, self.shared_variables.flipp_test_degree[self.index])
                else:
                    self.shared_variables.frame[self.index] = frame


    '''
    ----- HTTP solution -----
    '''

    def run_http(self):

        # get ip adress

        #r = requests.get('http://192.168.0.200:8080/video2.mjpg', auth=('admin', ''), stream=True)
        r = requests.get('http://192.168.0.3:8080/video', auth=('admin', ''), stream=True)

        #bytes = bytes()

        if(r.status_code == 200):
            byte = bytes()
            for chunk in r.iter_content(chunk_size=1024):
                byte += chunk
                a = byte.find(b'\xff\xd8')
                b = byte.find(b'\xff\xd9')
                if a != -1 and b != -1:
                    jpg = byte[a:b+2]
                    byte = byte[b+2:]
                    i = cv2.imdecode(np.fromstring(jpg, dtype=np.uint8), cv2.IMREAD_COLOR)
                    self.shared_variables.frame[index] = i

        else:
            print("Received unexpected status code {}".format(r.status_code))
