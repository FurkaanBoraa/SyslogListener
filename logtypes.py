#This script is for testing the structure of logs except filterlogs
#It will be active for a 1 day to get examples of logs
#Furkan Bora Murat

#IMPORTS
import socket

#Global Constants
HOST = '0.0.0.0'
PORT = 514

#Functions
def logtype(data):
    data = str(data)
    if "filter" not in data:
        print(data)

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:    #Socket Connection
    s.bind((HOST, PORT))    
    print(f"{HOST} listening on port {PORT}")
    
    while True:
        data = s.recv(512)
        logtype(data)