import sys
import threading
import logging

'''
This file handles logging and how to save to data.log
'''

logging.basicConfig(filename='data.log',level=logging.DEBUG)

def debug(data, label):
    logging.debug(log(data,label))


def info(data, label):
    logging.debug(log(data,label))


def warning(data, label):
    logging.debug(log(data,label))


def log(data, label):
    return "%s :  %s " % (label, data)

def clear_log():
    with open('data.log', 'w'):
        pass
