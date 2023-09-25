#This script is for listening to SysLog of Avrestor
#It has a purpose of getting the log and make it understandable
#And then store it on the MariaDB
#Furkan Bora Murat

#IMPORTS
import socket
import sys

#Global Constants
HOST = '0.0.0.0'
PORT = 514



#Functions
def logtype(data):
    data = str(data)
    if "filter" in data:
        return "Filter Log"
    elif "dhcp" in data:
        return "DHCP Log"


def logparser(data):
    data = str(data).split(",")
    return data


with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:    #Socket Connection
    s.bind((HOST, PORT))    
    print(f"{HOST} listening on port {PORT}")



    while True:
        data = s.recv(512) #Receive data max size 512
        logtype(data)