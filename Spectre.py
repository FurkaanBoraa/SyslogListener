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
    if "filter" in data:          #Filter Logs
        return 'f'                
    elif "dhcp" in data:          #DHCP Logs
        if 'ACK' in data:
            return 'da'
        elif 'REQUEST' in data:
            return 'dr'
        elif 'DISCOVER' in data:
            return 'dd'
        elif 'OFFER' in data:
            return 'do'
        elif 'REQUEST' in data:
            return 'dr'

#Decode bits to str and delete <number>
def logdecoder(data):
    log = data.decode('utf-8')
    log = log.lower()
    numbers = "^<.+>"
    log = re.sub(numbers, "", log)
    return log


##Parses datetime stamps
def logdatetime(data):
    datetime = data[:16]
    return datetime

def logger(data):
    log = logdecoder(data)
    datetime = logdatetime(log)
    

#Socket Connection
with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:    
    s.bind((HOST, PORT))    
    print(f"{HOST} listening on port {PORT}")

    while True:
        data = s.recv(512) #Receive data max size 512
        print(logdecoder(data))