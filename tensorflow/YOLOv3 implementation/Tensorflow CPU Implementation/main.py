import shared_variables
import sys
import threading
import cv2

# Start_instance
# Function that starts an instance of threads for each camera
def start_instance():

    # Capture camera
    _camera_capture = cv2.VideoCapture(0)

     # initiate shared variables instance
    _shared_variables = shared_variables.Shared_Variables(_camera_capture)

    # detection Thread
    _shared_variables.start_detection_thread()

    # show camera thread
    _shared_variables.start_camera_thread()

# Functions to calculate available cameras copied from
#https://stackoverflow.com/questions/7322939/how-to-count-cameras-in-opencv-2-3
def clearCapture(capture):
    capture.release()
    cv2.destroyAllWindows()


# Main function
def main():
    start_instance()

# Starts Program here!
if __name__ == '__main__':
    main()
