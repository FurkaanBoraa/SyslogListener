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
f = open("logexample.txt", "a+")

#Global Constants
HOST = '0.0.0.0'
PORT = 514
NUMBERS = re.compile("^<.+>")
LOGTYPES = re.compile("^f.*\[.*]:")

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
    wantedtypes = ["filterdns", "dhcp", "filter"]
    unwantedtypes = ["nginx", "snort"]
    for type in wantedtypes:
        if type in log:
            return type    
    return None

def formatdate(log):                    # Get the date and format it as well
    date = log[:15]
    date_time = datetime.datetime.strptime(date, "%b %d %H:%M:%S")
    date_time = date_time.replace(year=datetime.datetime.now().year)        # Adds Year
    formatteddate = date_time.strftime("%d-%m-%Y %H:%M:%S")
    return formatteddate

def stripdate(log):                     #Strip the date since we already get it in formatdate, may merge them 
    strippedlog = log[16:]
    return strippedlog

def striptype(log):                     # Strip type in log (filterlog[45684], dhcp[6546] etc.) since we get it at first
    striplog = re.sub(LOGTYPES,"", log)
    return striplog

def filterparser(log):
    splitlog = log.split(",")
    meaningfullog = {                   # Every filter log has same start info
        "rulenumber" : splitlog[0],
        # "subrulenumber" : splitlog[1],
        # "anchor" : splitlog[2],
        # "tracker" : splitlog[3],
        "realinterface" : splitlog[4],
        "reason" : splitlog[5],
        "action" : splitlog[6],
        "direction" : splitlog[7],
        }
    if splitlog[8] == "4":
        ipv4 = {                         # If log has IPv4 info
            "iptype" : splitlog[8],
            "tos" : splitlog[9],
            # "ecn" : splitlog[10],
            "ttl" : splitlog[11],
            "id" : splitlog[12],
            "offset" : splitlog[13],
            "flags" : splitlog[14],
            "protocolid" : splitlog[15],
            "protocol" : splitlog[16],
            "length" : splitlog[17],
            "source": splitlog[18],
            "destination" : splitlog[19]
        }
        meaningfullog.update(ipv4)
    elif splitlog[8] == "6":
        ipv6 = {                         # If log has IPv4 info
            "iptype" : splitlog[8],
            "class" : splitlog[9],
            "flow label" : splitlog[10],
            "hop limit" : splitlog[11],
            "protocol text" : splitlog[12],
            "protocol id" : splitlog[13],
            "length" : splitlog[14],
            "source": splitlog[15],
            "destination" : splitlog[16]
        }
        meaningfullog.update(ipv6)
    return meaningfullog

def logger(log):                        # Goes through all functions for each log
    log = logdecoder(log)
    log = logremovenumbers(log)
    log = lowercase(log)
    typeoflog = logtype(log)
    if typeoflog is not None:
        date_time = formatdate(log)
        log = stripdate(log)
        log = striptype(log)
        if typeoflog is "filter":   
            log = filterparser(log)         
            print(f"log type: {typeoflog}, date: {date_time}, log: {log}")
    else:
        f.write(f"{log}\n")

#Socket Connection
with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:    
    starttime = datetime.datetime.now().strftime("%d/%m/%Y, %H:%M")
    s.bind((HOST, PORT))    
    print(f"{HOST} started listening on port {PORT} at {starttime}")

    while True:
        log = s.recv(512)           #Receive log max size 512
        logger(log)
        
