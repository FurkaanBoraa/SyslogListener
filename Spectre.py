#This script is for listening to SysLog of Avrestor
#It has a purpose of getting the log and make it understandable
#And then store it on the MariaDB
#Furkan Bora Murat

#IMPORTS
import socket
import sys
import re

#Global Constants
HOST = '0.0.0.0'
PORT = 514



#Functions
def logtype(data):
    data = str(data)
    if "filter" in data:
        return 0                #Filter Logs
    elif "dhcp" in data:
        return 1                #DHCP Logs

#Decode bits to str and delete <number>
def logdecoder(data):
    log = data.decode('utf-8')
    numbers = "^<.+>"
    log = re.sub(numbers, "", log)
    return logdate(log)

def logdate(data):
    month = data[:16]

    return month


#Socket Connection
with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:    
    s.bind((HOST, PORT))    
    print(f"{HOST} listening on port {PORT}")

    while True:
        data = s.recv(512) #Receive data max size 512
        print(logdecoder(data))