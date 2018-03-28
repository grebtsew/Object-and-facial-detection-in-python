
import cv2


c = None

if c is not None:
    print("1 true")

c = ["a", "b"]
if c is not None:
    print("2 true")

c = []

if c is not None:
    print("3 true")


stream = cv2.VideoCapture(0)

test, c = stream.read()


if c is not None:
    print("4 true")
