import os
from threading import Thread

'''
Start Several clients at once to test server traffic ability
Also test how fast Serving can be
Try adding 10000 clients!
'''

# It appears that 100 requests to server at once over wifi = error!

number_of_clients=10

def start_client():
    print("Start client " )
    os.system("python test_client.py")

# Start here!
for i in range(0,number_of_clients):
    client_thread = Thread(target = start_client )
    client_thread.start()
