#This file contains start methods

#own imports
import utils.logging_data as LOG
import shared_variables
import sys
import threading
import cv2
import parser_controller as controller

import utils.intern_camera as i_cam

# Main function
def main():
    LOG.log("Starting system", "SYSTEM")
   
    shared_var = shared_variables.Shared_Variables(name="shared_version")
 

    controll_thread = controller.parse_controller(shared_var)
    controll_thread.start()
    
   

    
# Starts Program here! 
if __name__ == '__main__':
    main()
