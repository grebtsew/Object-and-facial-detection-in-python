import sys
import threading

def log(data, label):
    print ("%s :  %s " % (label, data)) 
    return
    

# Test number of threads runnning
# print  (threading.enumerate())
