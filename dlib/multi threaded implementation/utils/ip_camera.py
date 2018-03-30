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
    
    def __init__(self, shared_variables = None):
        threading.Thread.__init__(self)
        self.shared_variables = shared_variables
   
    def run(self):

        # get ip adress
    
        #r = requests.get('http://192.168.0.200:8080/video2.mjpg', auth=('admin', ''), stream=True)
        r = requests.get('http://192.168.1.242:8080/video', auth=('admin', ''), stream=True)

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
                    self.shared_variables.frame = i

        else:
            print("Received unexpected status code {}".format(r.status_code))

