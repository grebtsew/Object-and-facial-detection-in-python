import sys
import os
import threading
import time
import cv2
import shared_variables
import types
from subprocess import call
import configparser

class parse_controller(threading.Thread):

    config = None
    parser = None
    shared_variables_index = 0
    shared_variables = None
    system_reference_array = []
    status_array = list() # list threads
    func_info = (('help, h', 'show how to use all commands'),
                 ('helpsh', 'open python help shell'),
                 ('start -sys/sysid -camid', 'start instance in system or system. Ex: start -sys , start -000 -0 -SKIN_COLOR (anything func, cam or thread)'),
                 ('stop -sys/sysid -camid', 'stop instance in system or system. Ex: stop -sys , stop -000 -0 -SKIN_COLOR -WEBCAM'),
                 ('autostart', 'starts system with default values from config file.'),
                 ('imshow -sysid', 'start imshow thread in system'),
                 ('status', 'show system status'),
                 ('kill -sysid', 'Stop running system with threads'),
                 ('killall', 'Stop all running system with threads'),
                 ('log', 'Show log, make sure to activate logging in config to see anything'),
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
        instance_name =  "System_" + str(threading.get_ident())
        self.system_reference_array.append(shared_variables.Shared_Variables(name=instance_name, config=self.config))

    def run(self):
        args = None
        input_str = "";
        print ("----- Program -----")
        print (" type help or h to see functions")
        while True:

            input_str = input('Program>')
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
            self.call_show(arg_arr)
            return True
        elif s == "stop":
            self.call_stop(arg_arr)
            return True
        elif s == "kill":
            self.call_kill(arg_arr)
            return True
        elif s == "killall":
            self.call_killall(arg_arr)
            return True
        elif s == "exit":
            self.call_exit()
            return True
        else:
            return False

#
# --------- CALL FUNCTION DOWN HERE -----------
#

    def call_log(self):
        pass

    def call_kill(self,args = None):
        pass

    def call_killall(self,args = None):
        pass

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
            self.shared_variables.start_webcamera_stream(camera, index = camera_amount)
            camera_amount += 1

        time.sleep(1) # sleep between captures!

        if(self.config.getboolean('DEFAULT','START_IPCAMERA')):
            camera = self.config.getint('DEFAULT', 'IPCAMERA')
            self.shared_variables.start_ip_camera_stream(index = camera_amount)
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

    def call_start(self, args = None):

        if args is not None :
            if len(args) >= 3:

                if args[1] == "-read":
                    if args[2] == "-web":
                        self.status_array.append(["web", args[3]])
                        #self.shared_variables.start_intern_camera_stream(int(args[3]))
                    elif args[2] == "-gige":
                        self.status_array.append(list("gige", args[3]))
                        #self.shared_variables.start_intern_camera_stream(int(args[2]))
                    elif args[2] == "-ip":
                        self.status_array.append(list("ip", args[3]))
                        #self.shared_variables.start_intern_camera_stream(int(args[2]))

                elif args[1] == "-detect":
                    if args[2] == "-dlib":
                        self.shared_variables.start_dlib_detection_thread(0)
                        pass
                    elif args[2] == "-tf":
                        self.shared_variables.start_tf_detection_thread(0)
                        pass

                else:
                    print("No such parameter")


        else:
            print("No parameters!")

        pass

    def call_stop(self, args):
         if args is not None:
            if len(args) > 2:

                if args[1] == "-web":

                    self.status_array.remove()
                    self.shared_variables.start_camera_thread()
                    #self.shared_variables.start_intern_camera_stream(int(args[2]))
                elif args[1] == "-gige":
                    self.status_array.append(list("show gige", args[2]))
                    #self.shared_variables.start_intern_camera_stream(int(args[2]))
                elif args[1] == "-ip":
                    self.status_array.append(list("show ip", args[2]))
                    #self.shared_variables.start_intern_camera_stream(int(args[2]))

                else:
                    print("No such parameter")
         else:
            print("No parameters!")


    def call_show(self, args):
         if args is not None:
            if len(args) >= 2:

                if args[1] == "-web":

                    self.status_array.append(["show web", args[2]])
                    print("gere")
                    self.shared_variables.start_camera_thread()
                    #self.shared_variables.start_intern_camera_stream(int(args[2]))
                elif args[1] == "-gige":
                    self.status_array.append(list("show gige", args[2]))
                    #self.shared_variables.start_intern_camera_stream(int(args[2]))
                elif args[1] == "-ip":
                    self.status_array.append(list("show ip", args[2]))
                    #self.shared_variables.start_intern_camera_stream(int(args[2]))

                else:
                    print("No such parameter")
         else:
            print("No parameters!")

    def call_kill(self):

        pass

    def call_exit(self):
        os._exit(1)

    def call_status(self):

        print()
        print("Running threads:")
        print()

        for s in self.status_array:
            string = ""
            for i in s:
                string += i + " "

            print(string)

        pass


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
        pass
