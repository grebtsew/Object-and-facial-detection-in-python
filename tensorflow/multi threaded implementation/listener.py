# This code, is called from getters and setters for variables
# See shared variables for more information

# Add import to function files here
from func import skin_color


# Add thread reference here
skin_color_thread = None

# Add new function call here that need box
def box_notify(frame, box):

    
    
    pass

# Add new function call here that need landmarks
def landmarks_notify(frame, landmarks):
    start_skin_color_thread(frame, landmarks)
    
    pass

# Start skin color thread
# start skin color thread, might want queue and generic function here!
def start_skin_color_thread(frame, landmarks):
    global skin_color_thread

    #Skin Color - see imports
    if skin_color_thread is not None:
        if not skin_color_thread.isAlive():
            skin_color_thread = skin_color.skin_color(name = "Skin Color", frame = frame, landmarks = landmarks)
            skin_color_thread.start()
        else:
            #Skipped a detection value, can create queue here!
            pass
    else:
        skin_color_thread = skin_color.skin_color(name = "Skin Color", frame = frame, landmarks = landmarks)
        skin_color_thread.start()


