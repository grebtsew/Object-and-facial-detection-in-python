# This function will calculate the skin color of person and logg rgb value

import threading
import sys

sys.path.append('../')

from utils import logging_data as LOG


class skin_color(threading.Thread):
 
    def __init__(self, name, frame, landmarks):
        threading.Thread.__init__(self)
        self.name = name
        self.frame = frame
        self.landmarks = landmarks
        

    def run(self):

        x, y = self.get_facial(2)
        
        LOG.log( "Nose BGR: " + str(self.get_color(x,y)), "SKIN_COLOR: ")

        # for later:
        # get 3 good positions in face
        # take x approx positions
        # create array of color values
        # calculate medium value
        # log medium value

        

    def get_color(self, x, y):
        return self.frame[y][x]

    # Get Facial
    # return coordinates of facial
    # 0 = left eye
    # 1 = right eye
    # 2 = nose
    # 3 = left mouth
    # 4 = right mouth
    def get_facial(self, i = 0):
        x = int(self.landmarks[0, i])
        y = int(self.landmarks[0, i + 5])
        return x, y        

    # Get more facial
    # uses nose position to add more positions
    # send in 2 will return nose
    # param:
    #i = compare pos, gets distance from nose to i, see get facial for i
    #y_multi = multiply y change
    #x_multi = multiply x change
    #positive = up or down pos
    def get_more_facial(self, i = 0, y_multi = 1, x_multi = 1, positive = True):
        x = int(self.landmarks[0, i])
        y = int(self.landmarks[0, i + 5])
        center_x = int(self.landmarks[0, 2])
        center_y = int(self.landmarks[0, 2 + 5])

        if i == 2:
            return x,y

        # calculate pos
        if positive:
            x = x_multi*abs(x - center_x) + x
            y = y_multi*abs(y - center_y) + y
        else:
            x = x - x_multi*abs(x - center_x) 
            y = y - y_multi*abs(y - center_y) 
        return x,y


    # get approx positions
    # takes a position, returns an array of closeby points
    def get_approx_positions(self, x, y):
        pass
 
