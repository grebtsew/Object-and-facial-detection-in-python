#This file contains startmethods

#own imports
import utils.logging_data as LOG
import shared_variables
import sys
import threading
import cv2


# Start_instance
# Function that starts an instance of threads for each camera
def start_instance(instance_name,camera_id,camera_mode='NORMAL'):
    
    LOG.log("Capturing Camera %s" % camera_id, instance_name) 
    
    # Capture camera
    _camera_capture = cv2.VideoCapture(camera_id)

    # Wait for camera capture
    #while not _camera_capture.isOpened():
    #   pass 

     # initiate shared variables instance
    _shared_variables = shared_variables.Shared_Variables(instance_name,
                                          _camera_capture)
    # detection Thread  
    _shared_variables.start_detection_thread()

    # tracking Thread
    _shared_variables.start_tracking_thread()
    
    # show camera thread
    _shared_variables.start_camera_thread(camera_mode)

# Functions to calculate available cameras copied from
#https://stackoverflow.com/questions/7322939/how-to-count-cameras-in-opencv-2-3
def clearCapture(capture):
    capture.release()
    cv2.destroyAllWindows()

def countCameras():
    n = 0
    for i in range(10):
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

# Start a system instance for each camera in computer
def start_instances_for_all_cameras():
    # start all cameras
    number_of_cameras =  countCameras()
    
    LOG.log("Found %s cameras" % (number_of_cameras), "SYSTEM")
    for i in range(number_of_cameras):
        start_instance('CAM_%s' % (i), i, 'NORMAL')

        
    
# Main function
def main():
    LOG.log("Starting system", "SYSTEM")
    LOG.log("Start all threads", "SYSTEM")
    LOG.log("Find all cameras", "SYSTEM")

    start_instances_for_all_cameras();

    # example
        # start_instance('cam_0',0)
    
# Starts Program here! 
if __name__ == '__main__':
    main()
