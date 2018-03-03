
#own imports
import detection
import tracking
import show_camera
import utils.logging_data as LOG
import shared_variables

# system
import sys
import threading

# camera
import cv2
    


# Main function
def main():
    LOG.log("Starting system", "SYSTEM")
    LOG.log("Start detection thread", "SYSTEM")
   # t = threading.Thread(target=detection.Detection(), args=("hej",))
   # t = detection.Detection();

    _camera_capture = cv2.VideoCapture(0)

    # wait for camera capture here
    #while not _camera_capture.isOpened():
    #   pass

    # initiate shared variables instance
    _shared_variables = shared_variables.Shared_Variables('variable_names',
                                          _camera_capture)

    # detection Thread  
    thread_detection = detection.Detection(name = "Detection",
                            shared_variables = _shared_variables)
    thread_detection.start()

    # tracking Thread
    thread_tracking = tracking.Tracking(name = "Tracking",
                            shared_variables = _shared_variables)
    thread_tracking.start()

    # show camera
    thread_show_camera = show_camera.Show_Camera(name = "Show_Camera",
                            shared_variables = _shared_variables)
    thread_show_camera.start()

    
    
# Starts Program here! 
if __name__ == '__main__':
    main()
