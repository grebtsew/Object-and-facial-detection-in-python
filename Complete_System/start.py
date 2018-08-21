import utils.logging_data as LOG
import sys
import parser_controller as controller

'''
Start the program by running this file!
'''

# Main function
def main():
    LOG.clear_log()
    LOG.info("Log cleared", "ROOT")
    LOG.info("Starting program", "ROOT")

    controll_thread = controller.parse_controller()
    controll_thread.start()

# Starts Program here!
if __name__ == '__main__':
    main()
