import sys
import logging_data as LOG
import threading

frame = None


def init(_frame):
    global frame
    frame = _frame
    run()
   


def run():
    while True:
        # Make calculations
    
        break

    result = (0,0,0)
    
    LOG.log(result, 'HUD_COLOR_RGB')

    task_done()

def task_done():
    pass
    

