#!/usr/bin/python3
import time
import serial
import logging
import sys
from logging.handlers import TimedRotatingFileHandler

devices = ['/dev/ttyUSB0','/dev/ttyUSB1','/dev/ttyUSB2','/dev/ttyUSB3']

baud = 9600
#baud = 115200

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

logname = "./resetitko.log"
#logname = "./cardos.log"

handler = TimedRotatingFileHandler(logname, when='h', interval=1, utc=True)
#handler = TimedRotatingFileHandler(logname, when='s', interval=20, utc=True)
#handler.setLevel(logging.INFO)
#handler.suffix = "%Y%m%d%H%M"
logger.addHandler(handler)

'''
# reset device
ser.setDTR(False)
time.sleep(0.5)
ser.setDTR(True)
time.sleep(0.5)
ser.setDTR(False)
'''
success = False
for port in devices:
    try:
        print("I am Trying",port)
        ser = serial.Serial(port, baud, timeout=20)
        time.sleep(10)
        reading = ser.readline()
        print(reading)
        if ((str(reading,'utf-8')[0]=='$') or (str(reading,'utf-8')[0]=='#')):
            success = True
            break   
    except:
        pass
        
if (not success):
    sys.exit("I can not find any tty device.")

while True:
     reading = ser.readline()
     if (len(reading) > 0):
         data = str(int(round(time.time(),2))) + ',' + str(reading,'utf-8')
         print(data)
         logger.info(data)

