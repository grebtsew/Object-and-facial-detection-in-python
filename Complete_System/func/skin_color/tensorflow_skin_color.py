# This function will calculate the skin color of person and logg rgb value


from numpy import median
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

        color_array = []

        # take color of each landmark
        for (x, y) in self.landmarks:
            color_array.append(self.get_color(x,y))

        # calculate median rgb
        mean_RGB = self.calculate_medium(color_array)

    #    LOG.info( "Face RGB: " + str(mean_RGB), "SKIN_COLOR: ")
        print( "Face RGB: " + str(mean_RGB), "SKIN_COLOR: ")

    # Calculates mean color of several pointlists and transform bgr to rgb
    def calculate_medium_color(self, arr):
        list_of_bgr = []

        # get all bgr in a list
        for points in arr:
            for point in points:
                list_of_bgr.append(self.get_color(point[0], point[1]))

        r = []
        b = []
        g = []
        for color in list_of_bgr:
            r.append(color[2])
            g.append(color[1])
            b.append(color[0])

        return (median(r), median(g), median(b))

    def calculate_medium(self, arr):
        r = []
        b = []
        g = []
        for color in arr:
            r.append(color[2])
            g.append(color[1])
            b.append(color[0])

        return (median(r), median(g), median(b))

    def get_color(self, x, y):
        return self.frame[x][y]

    # Get Facial
    # return coordinates of facial
    # x x
    #  x
    # x x
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
    # i1 = first point
    # i2 = second point
    # y multi
    # x multi
    # add or remove
    def get_more_facial(self, i1 = 0, i2 = 1, y_multi = 1, x_multi = 1, positive = True):

        x1 = int(self.landmarks[0, i1])
        y1 = int(self.landmarks[0, i1 + 5])
        x2 = int(self.landmarks[0, i2])
        y2 = int(self.landmarks[0, i2 + 5])

        # calculate pos
        if positive:
            x = x_multi*abs(x1 - x2) + x1
            y = y_multi*abs(y1 - y2) + y1
        else:
            x = x1 - x_multi*abs(x1 - x2)
            y = y1 - y_multi*abs(y1 - y2)


        return x,y



    # get approx positions
    # takes a position, returns an array of closeby points
    # params, x, y, from, to
    def get_approx_positions(self, x, y, f, t):
        result = []
        for i in range(f,t):
            result.append([i + x,i + y])
        return result
