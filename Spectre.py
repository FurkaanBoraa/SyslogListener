#This script is for listening to SysLog of Avrestor
#It has a purpose of getting the log and make it understandable
#And then store it on the MariaDB
#Furkan Bora Murat

#IMPORTS
import socket
import sys
import re
import time
import datetime

# TEST SECTION
f = open("logexamples.txt", "a+")


#Global Constants
HOST = '0.0.0.0'
PORT = 514
NUMBERS = re.compile("^<.+>") 

#Functions
def logdecoder(log):                    # Decode logs from bit to str 
    log = log.decode('utf-8')
    return log

def logremovenumbers(log):              # Remove numbers in between angle brackets 
    log = re.sub(NUMBERS, "", log)
    return log

def lowercase(log):                     # Lowercase given log
    return log.lower()

def logtype(log):                       # Classification of logs respect to their type 
    types = ["dhcp", "filter"]
    for type in types:
        if type in log:
            return type    
    return None


def logger(log):                        # Goes through all functions for each log
    log = logdecoder(log)
    log = logremovenumbers(log)
    log = lowercase(log)
    typeoflog = logtype(log)
        # if typeoflog is not None:
        #     print(typeoflog, log)
        # else:
        #     f.write("This log type is not classified!", log)
    if typeoflog is None:
        print("This log type is not classified!", log)   
#Socket Connection
with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:    
    starttime = datetime.datetime.now().strftime("%d/%m/%Y, %H:%M")
    s.bind((HOST, PORT))    
    print(f"{HOST} started listening on port {PORT} at {starttime}")

    while True:
        log = s.recv(512)           #Receive log max size 512
        logger(log)
