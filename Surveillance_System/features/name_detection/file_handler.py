import os
import cv2
from datetime import datetime
import shutil
from pathlib import Path

def check_program_size():
    '''
    Make sure program doesnt fill memory
    '''
    memory_tresh = 2 # in gb

    size = getFolderSize(os.path.dirname(__file__)+"/Data")
    print( "Size: " + str(size))

    if size > memory_tresh * 1000000:
        print("Program and dataset is bigger then memory_tresh ", memory_tresh,
        " therefore we exit the program.")
        exit(0)

def getFolderSize(folder):
    '''
    Recursive function for getting folder size
    '''
    total_size = os.path.getsize(folder)
    for item in os.listdir(folder):
        itempath = os.path.join(folder, item)
        if os.path.isfile(itempath):
            total_size += os.path.getsize(itempath)
        elif os.path.isdir(itempath):
            total_size += getFolderSize(itempath)
    return total_size


def save_time_data(name):
    '''
    Save last seen data
    '''
    print(name, "Last seen at" , datetime.now().strftime('%Y-%m-%d %H:%M:%S'))


def save_image(name, image):
    '''
    Save image to folder named name
    '''
    height, width, channels = image.shape

    if(height <= 0 and width <= 0):
        return None, None;

    base = os.path.dirname(__file__)
    folder = (base+"/Data/"+name).replace("/","/")

    if not os.path.exists(folder):
        os.makedirs(folder)

    path = os.path.dirname(__file__)+"/Data/"+name+"/"+name+".jpg"
    cv2.imwrite(path,image)
    return path, image

def removedir(path):
    p = Path(path)
    dir_path = path.replace(p.name, "")
    print(dir_path)

    shutil.rmtree(dir_path, ignore_errors=True)
    pass

def save_face(name, image):
    '''
    Save image to folder named name
    '''
    height, width, channels = image.shape

    if(height <= 0 and width <= 0):
        return None, None;

    base = os.path.dirname(__file__)
    folder = (base+"/Data/"+name+"/Face/").replace("/","/")

    if not os.path.exists(folder):
        os.makedirs(folder)

    path = os.path.dirname(__file__)+"/Data/"+name+"/Face/"+name+".jpg"
    cv2.imwrite(path,image)
    return path, image


def get_available_name():
    '''
    Return a default available filename
    '''
    i = 0
    for root, dirs, files in os.walk(os.path.dirname(__file__)+"/Data"):

        while(("Unknown"+str(i)) in dirs):
            i += 1
    return "Unknown"+str(i)

def get_images_paths_and_names():
    '''
    Gets images of all known faces in correct order
    Gets name of all known faces in correct order
    '''
    lis = []
    name_lis = []
    for root, dirs, files in os.walk(os.path.dirname(__file__)+"/Data"):
        for name in dirs: # for each folder
            if "Face" in name :
                continue


            s = name
            temp = ''.join([i for i in s if not i.isdigit()])
            name_lis.append(temp)

            for roots, dirss, filess in os.walk(os.path.dirname(__file__)+"/Data/"+name):
                for file in filess: # for each image
                    if ".jpg" in file or ".png" is file:

                        if os.path.dirname(__file__)+"/Data/"+name+"/"+file not in lis:
                            lis.append(os.path.dirname(__file__)+"/Data/"+name+"/"+file)
                        #break; # we only want one image per person!
    return lis, name_lis



def secure_data_files():
    '''
    Make sure files exist
    Else create new ones
    '''
    base = os.path.dirname(__file__)
    folder = (base+"/Data").replace("\\","/")
    file = (base+"/Data/data.txt").replace("\\","/")

    if not os.path.exists(folder):
        os.makedirs(folder)

    if not os.path.exists(file):
        f = open(file,"w+")
        f.close()
