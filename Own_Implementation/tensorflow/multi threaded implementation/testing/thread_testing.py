import threading
import sys
import time

while True:
    print("Current running threads : ")
    print(threading.enumerate())
    time.sleep(3)
