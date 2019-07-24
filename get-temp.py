# alarm system

from __future__ import division

import minimalmodbus

import time
import codecs
import sys
import serial
from time import sleep
import re


TermAlarmFile="/tmp/ramdisk/TermAlarmFile"
TermErrFile="/tmp/ramdisk/TermErrFile"

#minimalmodbus.CLOSE_PORT_AFTER_EACH_CALL = True


def GetTemp():
  T=0.0

  
  try:
   m = minimalmodbus.Instrument('/dev/ttyUSB0', 1) # port name, slave address (in decimal)
   m.serial.baudrate = 9600
   m.serial.bytesize = 8
   m.serial.stopbits = 1
   m.serial.parity   = serial.PARITY_NONE
   m.serial.timeout = 1

   data=m.read_register(0, 0) # Registernumber, number of decimals

   #print("data=",data)

   if data==65535:
      T=65535
   elif data<10000:
      T=data/10
   else:
      T=-(data-10000)/10

   #print('%d' % T)
   #print('TEMPERATURE=%d' % T)
   return (T)

  except:
   print("Modbus error!")
   ser = serial.Serial(port='/dev/ttyUSB0',baudrate=9600,timeout=0.05, bytesize=8, parity='N', stopbits=1, xonxoff=0, rtscts=0) # open serial port
   #ser.is_open()
   #ser.reset()
   ser.close()
   return (555)

###


def SendMessageWhatsApp(Mess):
    Command='/usr/local/bin/yowsup-cli demos --config /home/pi/yowsup/config --send 79126021816 '+ Mess +'\ &'
    os.system(Command)

    return(1)

def SendMessageSms(Mess):

    Command='/usr/bin/gammu-smsd-inject TEXT 89126021816 -text  '+ Mess +'\ &'
    os.system(Command)

    return(1)

# main body

import os
import os.path
import json

TT=15
T=555

T=GetTemp()
print(GetTemp())

if (T < TT):
    if (not os.path.exists(TermAlarmFile)):
        os.mknod(TermAlarmFile)
        print ("Temp low! T=",T)
        SendMessageWhatsApp('Temp\ low!\ T='+str(T))
        SendMessageSms('Temp\ low!\ T='+str(T))

if (T > TT and T!=555):
    if (os.path.exists(TermAlarmFile)):
        os.remove(TermAlarmFile)
        print ("Temp norm! T=",T)
        SendMessageWhatsApp('Temp\ norm!\ T='+str(T))
        SendMessageSms('Temp\ norm!\ T='+str(T))

if (T==555):
    if (not os.path.exists(TermErrFile)):
        os.mknod(TermErrFile)
        print ("Temp sensor error!")
        SendMessageWhatsApp('Temp\ sensor\ error!')
        #SendMessageSms('Temp\ sensor\ error!')
else:
    if (os.path.exists(TermErrFile)):
        os.remove(TermErrFile)
        print ("Temp sensor norm!")
        SendMessageWhatsApp('Temp\ sensor\ norm!')
        #SendMessageSms('Temp\ sensor\ norm!')


exit(0)


