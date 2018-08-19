#This file contains start methods

#own imports
import utils.logging_data as LOG
import shared_variables
import sys
import threading
import cv2
import parser_controller as controller


# Main function
def main():
    LOG.log("Starting system", "SYSTEM")

    controll_thread = controller.parse_controller()
    controll_thread.start()

# Starts Program here!
if __name__ == '__main__':
    main()
