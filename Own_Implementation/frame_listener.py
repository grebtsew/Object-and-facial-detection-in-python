import calculate_face_color as face_color
import threading


# _notify(in_data)
#
# function that starts new thread for each notify
#
def _notify(in_data, i):
    if i == 0:
        t = threading.Thread(target=face_color.init(in_data))
        t.start()
    elif i == 1:
        pass

# Frame_Listener
#
# frame_listener interface
#
class Frame_Listener:
    frame = 0;
    
    def __init__(self):
#        self.v=v
        self.command=None
    def set(self, frame):
        self.frame=frame
        _notify(frame, 0)
        if self.command!=None:
            self.command()
    def get(self):
        return self.frame
    def trace(self, command):
        self.command=command
    def notify(self):
        _notify(self.frame, 0);



# Testing
#frame = Frame_Listener()
#frame.set(2)
