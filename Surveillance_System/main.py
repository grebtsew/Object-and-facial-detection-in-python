# Run this file to start implementation
from shared_variables import Shared_Variables


# input list can contain:
# Webcameras as Integer
# Ipcameras as rtps
# Youtube videos as http
input_sources = ['https://www.youtube.com/watch?v=Hw8YtsAFDaQ']

def main():
    shared_variables = Shared_Variables()
    for input in input_sources:
        # Start camera
        shared_variables.start_camera_stream(input)
        # Start detection
        shared_variables.start_object_detection_thread()
        # Start gui
        shared_variables.start_visualisation_thread()

if __name__ == '__main__':
    main()
