import sys
import os
import threading
import time
import shared_variables
import types
from subprocess import call
import configparser
import utils.logging_data as LOG

'''
This is our parse controller
This class controlls the program from the terminal
See commands and usage below
'''

class parse_controller(threading.Thread):

    config = None
    parser = None
    shared_variables_index = 0
    shared_variables = None
    system_reference_array = []
    func_info = (('help, h', 'show how to use all commands'),
                 ('helpsh', 'open python help shell'),
                 ('start  -sys/sysid -func -camid', 'start instance in system or system. Ex: start -SYS , start 000 -SKIN_COLOR 0 (anything func, cam or thread) '),
                 ('autostart', 'starts system with default values from config file. Edit config.ini.'),
                 ('imshow -sysid -camid', 'start imshow thread in system, and camid'),
                 ('show -sysid -camid -func true/false', 'show function of camera. Ex, show 000 0 LANDMARKS True, then start new imshow instance!'),
                 ('status', 'show system status'),
                 ('kill -sysid', 'Stop running system with threads'),
                 ('killall', 'Stop all running system with threads'),
                 ('log', 'Show log, make sure to activate logging in config to see anything'),
                 ('debug -sysid','debug toggle printing.'),
                 ('clear', 'clear terminal'),
                ('exit', 'exit program and all threads.'))

    def __init__(self):
        threading.Thread.__init__(self)

        # Get config file
        self.initiate_configfile()

        # Autostart
        if(self.config.getboolean("DEFAULT","AUTOSTART")):
            self.call_autostart()

    def initiate_configfile(self):
        try:
            self.config = configparser.ConfigParser()
            self.config.read("config.ini")
        except Exception as e:
            print("No config file found!")
            self.create_config_file()

    def create_config_file(self):
        print("Creating new Config file : config.ini")

        # create file
        cfgfile = open("config.ini",'w')

        # write to file
        temp_Config.add_section('DEFAULT')
        temp_Config.set('DEFAULT','WEBCAMERA', 0)
        temp_Config.set('DEFAULT','IPCAMERA', "192.168.0.200")
        temp_Config.set('DEFAULT','AUTOSTART', True)
        temp_Config.set('DEFAULT','START_WEBCAMERA', True)
        temp_Config.set('DEFAULT','START_IPCAMERA', False)
        temp_Config.set('DEFAULT','TENSORFLOW_DETECTION', False)
        temp_Config.set('DEFAULT','DLIB_DETECTION', True)
        temp_Config.set('DEFAULT','OPENCV_DETECTION', False)
        temp_Config.set('DEFAULT','TRACKING', True)
        temp_Config.set('DEFAULT','AGE_GENDER_ESTIMATION', False)
        temp_Config.set('DEFAULT','EXPRESSION', False)
        temp_Config.set('DEFAULT','SKIN_COLOR', False)
        temp_Config.set('DEFAULT','BLINK_FREQUENCY', False)
        temp_Config.add_section('SHOW')
        temp_Config.set('SHOW','LANDMARKS', True)
        temp_Config.set('SHOW','DETECTION', True)
        temp_Config.set('SHOW','TRACKING', True)
        temp_Config.set('SHOW','BACKPROJECTEDIMAGE', False)
        temp_Config.set('SHOW','SCORE', False)
        temp_Config.set('SHOW','GRAYSCALE', False)
        temp_Config.set('SHOW','EYES', False)
        temp_Config.set('SHOW','FACE', False)
        temp_Config.add_section('LOG')
        temp_Config.set('LOG','LOG_DATA', True)
        temp_Config.add_section('DEBUG')
        temp_Config.set('DEBUG','DEBUG', True)
        temp_Config.write(cfgfile)
        cfgfile.close()

        #Reread config file
        self.initiate_configfile()

    def create_new_system_instance(self):
        # Generate system id and add new system instance
        instance_name =  str(threading.get_ident())
        self.system_reference_array.append(shared_variables.Shared_Variables(name=instance_name, config=self.config))
        LOG.info("Created system with id " + str(instance_name), "SYSTEM-" + str(instance_name))
        print("Created system with id " + str(instance_name))

    def run(self):
        args = None
        input_str = "";
        print ("----- Program -----")
        print (" type help or h to see functions")
        while True:
            input_str = input('Program>')
            LOG.info("Run command "+input_str, "ROOT")
            input_str_array = input_str.split(' ')
            if self.get_first_arg(input_str_array) is not None:
                if self.run_command(input_str_array):
                    pass
                else:
                    print("No command : " + input_str + " (for help type h)")

    def get_first_arg(self,arr):
        for s in arr:
            if len(s) > 0:
                return s
        return None


    def get_all_arg(self,arr):

        res = list()
        for s in arr:
            if len(s) > 0 :
                res.append(s)
        return res

    def run_command(self,arr):
        arg_arr = self.get_all_arg(arr);
        s = arg_arr[0]
        s = s.lower()

        if s == "help" or s == "h":
            self.call_help()
            return True
        elif s == "helpsh":
            help()
            pass
        elif s == "clear":
            self.call_clear()
            return True
        elif s == "log":
            self.call_log()
            return True
        elif s == "status":
            self.call_status()
            return True
        elif s == "start":
            self.call_start(arg_arr)
            return True
        elif s == "autostart":
            self.call_autostart()
            return True
        elif s == "imshow":
            self.call_imshow(arg_arr)
            return True
        elif s == "show":
            self.call_show(arg_arr)
            return True
        elif s == "kill":
            self.call_kill(arg_arr)
            return True
        elif s == "killall":
            self.call_killall()
            return True
        elif s == "exit":
            self.call_exit()
            return True
        elif s == "debug":
            self.call_debug()
            return True
        else:
            return False

#
# --------- CALL FUNCTION DOWN HERE -----------
#

    def call_autostart(self):
        # New Shared_Variables
        self.create_new_system_instance()

        # Set reference current
        self.shared_variables_index = len(self.system_reference_array)-1

        # set reference
        self.shared_variables = self.system_reference_array[self.shared_variables_index]

        camera_amount = 0;
        # Start default cameras
        if(self.config.getboolean('DEFAULT','START_WEBCAMERA')):
            camera = self.config.getint('DEFAULT', 'WEBCAMERA')
            self.shared_variables.start_webcamera_stream(camera)
            camera_amount += 1

        time.sleep(1) # sleep between captures!

        if(self.config.getboolean('DEFAULT','START_IPCAMERA')):
            camera = self.config.get('DEFAULT', 'IPCAMERA')
            self.shared_variables.start_ip_camera_stream(camera)
            camera_amount += 1

        # For each camera
        for i in range(0, camera_amount):

            # Show cameras
            self.shared_variables.start_show_camera(index = i)

            # Start default detection
            if(self.config.getboolean('DEFAULT','DLIB_DETECTION')):
                self.shared_variables.start_dlib_detection_thread(i)
            if(self.config.getboolean('DEFAULT','TENSORFLOW_DETECTION')):
                self.shared_variables.start_tf_detection_thread(i)
            if(self.config.getboolean('DEFAULT','OPENCV_DETECTION')):
                self.shared_variables.start_opencv_detection_thread(i)

            # Start default functions
            if(self.config.getboolean('DEFAULT','AGE_GENDER_ESTIMATION')):
                self.shared_variables.start_age_gender_thread(i)

            if(self.config.getboolean('DEFAULT','BLINK_FREQUENCY')):
                self.shared_variables.start_blink_thread(i)

            if(self.config.getboolean('DEFAULT','EXPRESSION')):
                self.shared_variables.start_expression_thread(i)

            # Tracking
            if(self.config.getboolean('DEFAULT','TRACKING')):
                self.shared_variables.start_tracking_thread(i)

    def get_system_index(self, name):
        res = 0
        for sys in self.system_reference_array:
            if(sys.name ==  name):
                return res
            res += 1

        return None

    def call_start(self, args = None):
        if args is not None :
            if args[1] == "-SYS":
                # start new system
                self.create_new_system_instance()
                return

            system_index = self.get_system_index(args[1])
            if system_index is not None:
                # Functions 3 args
                if len(args) >= 3:
                    if args[2] == "-DLIB_DETECTION":
                        self.system_reference_array[system_index].start_dlib_detection_thread(int(args[3]))
                    elif args[2] == "-TENSORFLOW_DETECTION":
                        self.system_reference_array[system_index].start_tf_detection_thread(int(args[3]))
                    elif args[2] == "-OPENCV_DETECTION":
                        self.system_reference_array[system_index].start_opencv_detection_thread(int(args[3]))
                    elif args[2] == "-TRACKING":
                        self.system_reference_array[system_index].start_tracking_thread(int(args[3]))
                    elif args[2] == "-AGE_GENDER_ESTIMATION":
                        self.system_reference_array[system_index].start_age_gender_thread(int(args[3]))
                    elif args[2] == "-EXPRESSION":
                        self.system_reference_array[system_index].start_expression_thread(int(args[3]))
                    elif args[2] == "-SKIN_COLOR":
                        self.system_reference_array[system_index].setting[shared_variables.SETTINGS.SKIN_COLOR] = True
                    elif args[2] == "-BLINK_FREQUENCY":
                        self.system_reference_array[system_index].start_blink_thread(int(args[3]))
                    elif args[2] == "-WEBCAMERA":
                        self.system_reference_array[system_index].start_webcamera_stream(int(args[3]))
                    elif args[2] == "-IPCAMERA":
                        self.system_reference_array[system_index].start_ip_camera_stream(args[3])
                    elif args[2] == "-IMSHOW":
                        self.system_reference_array[system_index].start_show_camera(int(args[3]))
                    else:
                        print("Command " + args + " is invalid,")
                else:
                    print("Not enought parameters in start call. Ex start -SYS or start -11111 -SKIN_COLOR -0")

    def call_exit(self):
        os._exit(1)

    def call_help(self):
        print()
        print("This is program, see functions below. ")
        print()
        print("Help: ")
        for s in self.func_info:
            print( s[0]   + "\t\t" + s[1])
        print()

    def call_clear(self):
        os.system('cls' if os.name=='nt' else 'clear')

    def call_status(self):
        print()
        print("----- Show Systems and info below -----")
        print()

        if(len(self.system_reference_array) > 0 ):
            for sys in self.system_reference_array:
                print ("----------------------------------------")
                print(" ----- System id: " + str(sys.name) + " ----- ")
                print("Amount of camera sources: " + str(sys.reference_length))
                for cam in range(0,sys.reference_length):
                    print(" ----- Camera id : " + str(cam) +" -----")
                    settings = sys.setting[cam]
                    print("Active functions: ")
                    temp = 0
                    for b in settings:
                        if b == True:
                            print(shared_variables.SETTINGS(temp).name)

                        temp += 1

                print("----------------------------------------")
        else:
            print("No running systems")

    def call_kill(self,args):
        if(len(args) >= 1):
            system_index = self.get_system_index(args[1])
            if system_index is not None:
                self.system_reference_array[system_index].system_running = False
                del self.system_reference_array[system_index]
            else:
                print("Invalid arguments in system call kill.")
        else:
            print("Invalid arguments in system call kill.")

    def call_killall(self):
        for system in self.system_reference_array:
            system.system_running = False
        self.system_reference_array = []
        print("Removed all Systems!")

    def call_imshow(self, args):
        if(len(args) >= 2):
            system_index = self.get_system_index(args[1])
            if(system_index is not None):
                self.system_reference_array[system_index].start_show_camera(args[2])
            else:
                print("Invalid arguments in system call imshow.")

    def str2bool(v):
        return v.lower() in ("yes", "true", "t", "1")

    def call_show(self, args):
        if(len(args) >= 4):
            system_index = self.get_system_index(args[1])
            if(system_index is not None):
                if(args[3] == "EYES"):
                    self.system_reference_array[system_index].setting[args[2]][shared_variables.SETTINGS.SHOW_EYES.value] = str2bool(args[4])
                elif (args[3] == "FACE"):
                    self.system_reference_array[system_index].setting[args[2]][shared_variables.SETTINGS.SHOW_FACE.value] = str2bool(args[4])
                elif (args[3] == "SCORE"):
                    self.system_reference_array[system_index].setting[args[2]][shared_variables.SETTINGS.SHOW_SCORE.value] = str2bool(args[4])
                elif (args[3] == "TRACKING"):
                    self.system_reference_array[system_index].setting[args[2]][shared_variables.SETTINGS.SHOW_TRACKING.value] = str2bool(args[4])
                elif (args[3] == "DETECTION"):
                    self.system_reference_array[system_index].setting[args[2]][shared_variables.SETTINGS.SHOW_DETECTION.value] = str2bool(args[4])
                elif (args[3] == "GRAYSCALE"):
                    self.system_reference_array[system_index].setting[args[2]][shared_variables.SETTINGS.SHOW_GRAYSCALE.value] = str2bool(args[4])
                elif (args[3] == "LANDMARKS"):
                    self.system_reference_array[system_index].setting[args[2]][shared_variables.SETTINGS.SHOW_LANDMARKS.value] = str2bool(args[4])
                elif (args[3] == "BACKPROJECTEDIMAGE"):
                    self.system_reference_array[system_index].setting[args[2]][shared_variables.SETTINGS.SHOW_BACKPROJECTEDIMAGE.value] = str2bool(args[4])
            else:
                print("Invalid arguments in system call imshow.")

    def call_debug(self, args):
        if(len(args) >= 1):
            system_index = self.get_system_index(args[1])
            if(system_index is not None):
                if self.system_reference_array.debug :
                    self.system_reference_array.debug = False
                    self.system_reference_array[system_index].setting[args[1]][shared_variables.SETTINGS.DEBUG.value] = False
                else:
                    self.system_reference_array.debug = True
                    self.system_reference_array[system_index].setting[args[1]][shared_variables.SETTINGS.DEBUG.value] = True

    def call_log(self):
        with open("data.log", 'r') as fin:
            print (fin.read())
