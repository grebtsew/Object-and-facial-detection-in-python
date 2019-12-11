import tempfile
import time
import os

def test:
    print(tempfile.tempdir)
    print(os.path.dirname(os.getcwd()) + "\\tmp")
    tempfile.tempdir = os.path.dirname(os.getcwd()) + "\\tmp"
    print(tempfile.tempdir)

    fp = tempfile.NamedTemporaryFile()
    fp.write(b'Hello world!')
    # read data from file
    fp.seek(0)
    print(fp.read())
    # close the file, it will be removed
    time.sleep(1)
    fp.close()

class TempFile():
    """
    A Tempfile is a file that will store temporary data, and will be removed the second the resources are no longer needed.
    In this implementation we will use this with our videos in order to no fill the harddrive during execution.
    We will need to make sure both parties are done before clearing temp files.
    """
    
    def __init__(self):
        temp_dir = os.getcwd() + "\\tmp"
        # if tempdir don't exist, create folder
        try:
            os.stat(directory)
        except:
            os.mkdir(directory)
        # set our tempdir
        tempfile.tempdir = temp_dir

    def create(self):
        pass

    def write(self):
        pass

    def close(self):
        pass
