import tkinter as tk
import random

import tkinter as tk

class Example(tk.Frame):
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)
        self.l1 = tk.Label(self, text="Hover over me")
        self.l2 = tk.Label(self, text="", width=40)
        self.l1.pack(side="top")
        self.l2.pack(side="top", fill="x")

        self.l1.bind("<Enter>", self.on_enter)
        self.l1.bind("<Leave>", self.on_leave)

    def on_enter(self, event):
        self.l2.configure(text="Hello world")

    def on_leave(self, enter):
        self.l2.configure(text="")

if __name__ == "__main__":
    root = tk.Tk()
    Example(root).pack(side="top", fill="both", expand="true")
    root.mainloop()

"""
root = tk.Tk()
root.geometry("900x600")

treeview_frame = tk.Frame(root, background="#FFF0C1", bd=1, relief="sunken")
graph_frame = tk.Frame(root, background="#D2E2FB", bd=1, relief="sunken")
text_frame = tk.Frame(root, background="#CCE4CA", bd=1, relief="sunken")
button_frame = tk.Frame(root, background="#F5C2C1", bd=1, relief="sunken")

treeview_frame.grid(row=0, column=0, sticky="nsew", padx=2, pady=2)
graph_frame.grid(row=1, column=0, sticky="nsew", padx=2, pady=2)
text_frame.grid(row=0, column=1, rowspan=2, sticky="nsew", padx=2, pady=2)
button_frame.grid(row=0, column=2, rowspan=2, sticky="nsew", padx=2, pady=2)

root.grid_rowconfigure(0, weight=3)
root.grid_rowconfigure(1, weight=2)

root.grid_columnconfigure(0, weight=3)
root.grid_columnconfigure(1, weight=2)
root.grid_columnconfigure(2, weight=2)

#tree = tk.Treeview(treeview_frame)
#sb = tk.Scrollbar(treeview_frame)
#sb.pack(side="right", fill="y")
#tree.pack(side="left", fill="both", expand=True)

root.mainloop()
"""
"""
root = tk.Tk()
# width x height + x_offset + y_offset:
root.geometry("170x200+30+30")

languages = ['Python','Perl','C++','Java','Tcl/Tk']
labels = range(5)
for i in range(5):
   ct = [random.randrange(256) for x in range(3)]
   brightness = int(round(0.299*ct[0] + 0.587*ct[1] + 0.114*ct[2]))
   ct_hex = "%02x%02x%02x" % tuple(ct)
   bg_colour = '#' + "".join(ct_hex)
   l = tk.Label(root,
                text=languages[i],
                fg='White' if brightness < 120 else 'Black',
                bg=bg_colour)
   l.place(x = 20, y = 30 + i*30, width=120, height=25)

root.mainloop()
"""
"""
import tkinter
import cv2
import PIL.Image, PIL.ImageTk
import time

class App:
    def __init__(self, window, window_title, video_source=0):
        self.window = window
        self.window.title(window_title)
        self.video_source = video_source

        # open video source (by default this will try to open the computer webcam)
        self.vid = MyVideoCapture(self.video_source)

        # Create a canvas that can fit the above video source size
        self.canvas = tkinter.Canvas(window, width = self.vid.width, height = self.vid.height)
        self.canvas.pack()

        # Button that lets the user take a snapshot
        self.btn_snapshot=tkinter.Button(window, text="Snapshot", width=50, command=self.snapshot)
        self.btn_snapshot.pack(anchor=tkinter.CENTER, expand=True)

        # After it is called once, the update method will be automatically called every delay milliseconds
        self.delay = 15
        self.update()

        self.window.mainloop()

    def snapshot(self):
        # Get a frame from the video source
        ret, frame = self.vid.get_frame()

        if ret:
            cv2.imwrite("frame-" + time.strftime("%d-%m-%Y-%H-%M-%S") + ".jpg", cv2.cvtColor(frame, cv2.COLOR_RGB2BGR))

    def update(self):
        # Get a frame from the video source
        ret, frame = self.vid.get_frame()
        if ret:
            self.photo = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(frame))
            self.canvas.create_image(0, 0, image = self.photo, anchor = tkinter.NW)
        self.window.after(self.delay, self.update)

class MyVideoCapture:
    def __init__(self, video_source=0):
        # Open the video source
        self.vid = cv2.VideoCapture(video_source)
        if not self.vid.isOpened():
            raise ValueError("Unable to open video source", video_source)

        # Get video source width and height
        self.width = self.vid.get(cv2.CAP_PROP_FRAME_WIDTH)
        self.height = self.vid.get(cv2.CAP_PROP_FRAME_HEIGHT)

    def get_frame(self):
        if self.vid.isOpened():
            ret, frame = self.vid.read()
            if ret:
                # Return a boolean success flag and the current frame converted to BGR
                return (ret, cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            else:
                return (ret, None)
        else:
            return (ret, None)

    # Release the video source when the object is destroyed
    def __del__(self):
        if self.vid.isOpened():
            self.vid.release()
# Create a window and pass it to the Application object
App(tkinter.Tk(), "Tkinter and OpenCV")
"""
