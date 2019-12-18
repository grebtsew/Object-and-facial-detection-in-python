import tkinter as tk
import tkinter

import random
import cv2
import PIL.Image, PIL.ImageTk
import time

class App:
    def __init__(self, window, window_title, video_source=0):
        self.window = window
        self.window.title(window_title)
        self.video_source = video_source

        window.geometry("900x600")

        treeview_frame = tk.Frame(self.window, background="#FFF0C1", bd=1, relief="sunken")
        graph_frame = tk.Frame(self.window, background="#D2E2FB", bd=1, relief="sunken")
        text_frame = tk.Frame(self.window, background="#CCE4CA", bd=1, relief="sunken")
        button_frame = tk.Frame(self.window, background="#F5C2C1", bd=1, relief="sunken")

        treeview_frame.grid(row=0, column=0, sticky="nsew", padx=2, pady=2)
        graph_frame.grid(row=1, column=0, sticky="nsew", padx=2, pady=2)
        text_frame.grid(row=0, column=1, rowspan=2, sticky="nsew", padx=2, pady=2)
        button_frame.grid(row=0, column=2, rowspan=2, sticky="nsew", padx=2, pady=2)

        self.window.grid_rowconfigure(0, weight=3)
        self.window.grid_rowconfigure(1, weight=2)

        self.window.grid_columnconfigure(0, weight=3)
        self.window.grid_columnconfigure(1, weight=2)
        self.window.grid_columnconfigure(2, weight=2)

        # create grid over these cards
        self.card = Card(self.window).grid(row=0, column=0,sticky="nsew", padx=2, pady=2)#.pack(side="top", fill="both", expand="true")

        # open video source (by default this will try to open the computer webcam)
        self.vid = MyVideoCapture(self.video_source)

        # Create a canvas that can fit the above video source size
        self.canvas = tkinter.Canvas(window, width = self.vid.width, height = self.vid.height)
        self.canvas.grid(row=0, column=0, sticky="nsew", padx=2, pady=2)
        #self.canvas.pack()

        # Button that lets the user take a snapshot
        self.btn_snapshot=tkinter.Button(window, text="Snapshot", width=50, command=self.snapshot)
        #self.btn_snapshot.pack(anchor=tkinter.CENTER, expand=True)

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


class Card(tk.Frame):
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)
        self.l1 = tk.Label(self, text="Hover over me")
        self.l2 = tk.Label(self, text="", width=40)
        #self.l1.pack(side="top")
        #self.l2.pack(side="top", fill="x")

        self.l1.bind("<Enter>", self.on_enter)
        self.l1.bind("<Leave>", self.on_leave)

    def on_enter(self, event):
        self.l2.configure(text="Hello world")

    def on_leave(self, enter):
        self.l2.configure(text="")

if __name__ == "__main__":
    # Create a window and pass it to the Application object
    App(tkinter.Tk(), "Tkinter and OpenCV")
