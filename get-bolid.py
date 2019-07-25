# alarm system
# v2 

from __future__ import division

import minimalmodbus

import time
import codecs
import sys
import serial
from time import sleep
import re
from subprocess import call

#minimalmodbus.CLOSE_PORT_AFTER_EACH_CALL = True


CRC = [0,94,188,226,97,63,221,131,194,156,126,32,163,253,31,65,
157,195,33,127,252,162,64,30,95,1,227,189,62,96,130,220,
35,125,159,193,66,28,254,160,225,191,93,3,128,222,60,98,
190,224,2,92,223,129,99,61,124,34,192,158,29,67,161,255,
70,24,250,164,39,121,155,197,132,218,56,102,229,187,89,7,
219,133,103,57,186,228,6,88,25,71,165,251,120,38,196,154,
101,59,217,135,4,90,184,230,167,249,27,69,198,152,122,36,
248,166,68,26,153,199,37,123,58,100,134,216,91,5,231,185,
140,210,48,110,237,179,81,15,78,16,242,172,47,113,147,205,
17,79,173,243,112,46,204,146,211,141,111,49,178,236,14,80,
175,241,19,77,206,144,114,44,109,51,209,143,12,82,176,238,
50,108,142,208,83,13,239,177,240,174,76,18,145,207,45,115,
202,148,118,40,171,245,23,73,8,86,180,234,105,55,213,139,
87,9,235,181,54,104,138,212,149,203,41,119,244,170,72,22,
233,183,85,11,136,214,52,106,43,117,151,201,74,20,246,168,
116,42,200,150,21,75,169,247,182,232,10,84,215,137,107,53]



# func
def GetPortState(PortNum):

 try:
    #ser = serial.Serial(port='/dev/ttyUSB0', baudrate=9600, timeout=1, bytesize=8, parity='N', stopbits=1, xonxoff=1, rtscts=1)

    #if ser.is_open:
    #    a = 1
        # print(ser.name)  # check which port was really used
    #else:
    #    exit(1)

    data = [0 for i in range(9)]

    data[0]=0x7F
    data[1]=0x08
    data[2]=0x00
    data[3]=0x57
    data[4]=0x02
    data[5]=0x00
    data[6]=0x00
    data[7]=PortNum
    data[8]=0x00

    for i in range(0,8):
        data[8]=CRC[data[8] ^ data[i]]

    #print(hex(data[8]))
    #print(bytes(data))
    ser.write(bytes(data))

    ##sleep(0.05)

    #line = ser.readline()
    line = ser.read(9)

    text = codecs.encode(line, 'hex')

    #print ('Response')

    #print (codecs.encode(line, 'hex'))

    # str = str(line)

    # for i in range(len(str)):
    #    print (i, '=', str[i])

    #print (len(line))

    #print (line[7]

    #ser.close()  # close port
    
    return (line[7])

 except (KeyboardInterrupt, SystemExit):
   raise

 except:
   return (555)
#

# func
def GetPortResistance(PortNum):
 
 try:
    #ser = serial.Serial(port='/dev/ttyUSB0', baudrate=9600, timeout=1, bytesize=8, parity='N', stopbits=1, xonxoff=1, rtscts=1) 

    #if ser.is_open:
    #    a=1
        #print(ser.name)  # check which port was really used
    #else:
    #    exit(1)

    #ser.flushInput()
    #ser.flushOutput()

    data = [0 for i in range(9)]

    data[0]=0x7F
    data[1]=0x08
    data[2]=0x00
    data[3]=0x57
    data[4]=0x04
    data[5]=0x05
    data[6]=0x06
    data[7]=PortNum
    data[8]=0x00

    for i in range(0,8):
        data[8]=CRC[data[8] ^ data[i]]

    #print(hex(data[8]))
    #print(bytes(data))

    ser.write(bytes(data))

    ##sleep(0.05)

    #line = ser.readline()
    line = ser.read(20)

    #text = codecs.encode(line, 'hex')

    #print ('Response')

    #print (codecs.encode(line, 'hex'))

    #ser.send_break()

    RawStr = str(line)

    #for i in range(30, 38):
    #   print (i, '=', RawStr[i])

    S=re.findall("\d+\.\d+", RawStr)

    #print (line)
    Resistance = float(str(S[0]))

    #ser.flush()

    #print (Resistance)
    #ser.close()  # close port
    #return (0)
    return (Resistance)

 except:
  return (555)
#

###

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


###

def GetPortState2(PortNum):
    TryCount=0
    while (TryCount<10):
        S=GetPortState(PortNum)
        if S == 555:
            TryCount=TryCount+1
        else:
            TryCount=100
    return (S)
##

def GetPortResistance2(PortNum):
    TryCount=0
    while (TryCount<10):
        R=GetPortResistance(PortNum)
        if R == 555:
            TryCount=TryCount+1
        else:
            TryCount=100
    return (R)

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
import re

ArmedStateFile="/tmp/ramdisk/ArmedStateFile"
SensorStateFile="/tmp/ramdisk/SensorState.txt"
SensorResStateFile="/tmp/ramdisk/Resistance.txt"
SensResStateFile="/tmp/ramdisk/Resistance.txt"

SensResDataFile="/tmp/ramdisk/SensResData.txt"

SensorState=[0]*11
SensorStateOld=[0]*11
SensorResState=[0]*11
SensorResStateOld=[0]*11


SensResDataOld=[0]*11
SensResDataNew=[0]*11
SensResStateOld=[0]*11
SensResStateNew=[0]*11


SensorName=['sens0','alarm\ entrance','alarm\ 1\ floor\ room','alarm\ 1\ floor','alarm\ 2\ floor','power','alarm\ boiler','gas\ boiler','smoke\ boiler','smoke\ 1\ floor','smoke\ 2\ flor']

SensorAlwaysControl=[0,0,0,0,0,1,0,1,1,1,1]


ArmedState=0;
ArmedStateOld=0;


if (os.path.exists(ArmedStateFile)):
#  print("find armed file")
  ArmedStateOld=1
else:
#  print("not find armed file")
  ArmedStateOld=0


#while 2>1:
for i in range(1,2):
  print ("start")

  ser = serial.Serial(port='/dev/ttyUSB0',baudrate=9600,timeout=0.05, bytesize=8, parity='N', stopbits=1, xonxoff=0, rtscts=0) # open serial port

  if ser.is_open:
    #print(ser.name)         # check which port was really used
    N=1
  else:
    exit(1)


  for i in range(1,11):
      SensorState[i]=GetPortState2(i)
      if (SensorState[i]==23):
          SensorState[i]=24

  for i in range(1,11):
      print("S=",SensorState[i])


  Counter=0
  for i in range(1,11):
      if (SensorState[i]==109):
          Counter=Counter+1

  if (Counter==10):
      ArmedState=0
      if (ArmedStateOld==1):
          os.remove(ArmedStateFile)
          ArmedStateOld=0
          if (os.path.exists(SensorStateFile)):
               os.remove(SensorStateFile)
          print ("ArmedState change from 1 to 0")
          SendMessageWhatsApp("Alarm\ system\ OFF")
          SendMessageSms("Alarm\ system\ OFF")
  
  if (Counter==0):
      ArmedState=1
      if (ArmedStateOld==0):
          os.mknod(ArmedStateFile)
          ArmedStateOld=1
          if (os.path.exists(SensResStateFile)):
              os.remove(SensResStateFile)
          print ("ArmedState change from 0 to 1")
          SendMessageWhatsApp("Alarm\ system\ ON")
          SendMessageSms("Alarm\ system\ ON")

  if (Counter>0 and Counter<10):
      ArmedState=2
  

#  print ("Counter=",Counter)

  print ("ArmedState=", ArmedState)



  if (ArmedState==1):

      if (os.path.exists(SensorStateFile)):
        with open(SensorStateFile,'r') as filehandle:
          SensorStateOld=json.load(filehandle)

        for i in range(1,11):
            if (SensorState[i]!=SensorStateOld[i]):
                if (SensorState[i]==24):
                    S="Norm"
                if (SensorState[i]==118):
                    S="Entrance"
                if (SensorState[i]==37):
                    S="Smoke\ alarm"
                if (SensorState[i]==3):
                    S="Secur\ alarm"
                if (SensorState[i]==17):
                    S="Fail"
                if (SensorState[i]==45):
                    S="Fail"
                if (SensorState[i]==214):
                    S="Fail"
                if (SensorState[i]==555):
                    S="Fail"

                print ("Change state sensor=",i," Name=", SensorName[i]," State=",S)
                SendMessageWhatsApp(SensorName[i]+'\ '+S)
                if (SensorStateOld[i]!=555):
                  if (SensorState[i]!=555):
                    SendMessageSms(SensorName[i]+'\ '+S)
            SensorStateOld[i]=SensorState[i] 


      else:
        for i in range(1,11):
          SensorStateOld[i]=24

      with open(SensorStateFile,'w') as filehandle:
            json.dump(SensorStateOld, filehandle)


  if (ArmedState==0):

   for i in range (1,11):
    if (SensorAlwaysControl[i]==1): 
      R=GetPortResistance(i)
      #print(i,"=",R)
      if (R>2 and R<10):
      #norm
        SensResDataNew[i]=0
      else:
       #alarm
       if (R==555):
        SensResDataNew[i]=555
       else:
        SensResDataNew[i]=1
    else:
        SensorResState[i]=0


  if (os.path.exists(SensResDataFile)):
    with open(SensResDataFile,'r') as filehandle:
      SensResDataOld=json.load(filehandle)
      print ("Find SensResDataFile")
  else:
      SensResDataOld=SensResDataNew


  with open(SensResDataFile,'w') as filehandle:
    json.dump(SensResDataNew, filehandle)


  if (os.path.exists(SensResStateFile)):
      with open(SensResStateFile,'r') as filehandle:
          SensResStateOld=json.load(filehandle)
          print ("Find SensResStateFile")
  else:
      SensResStateOld=SensResStateNew

  for i in range (1,11):
    if (SensResDataOld[i]==SensResDataNew[i]):
        SensResStateNew[i]=SensResDataNew[i]
    else:
        SensResStateNew[i]=SensResStateOld[i]
        #print ("change ",i)

  for i in range (1,11):
    if (SensResStateOld[i]!=SensResStateNew[i]):
        print ("Change state i=",i)

        if (SensResStateNew[i]==0):
          S="Norm"
        if (SensResStateNew[i]==1):
          S="Alarm"
        if (SensResStateNew[i]==555):
          S="Error"
        print ("Change state sensor=",i," Name=", SensorName[i]," State=",S)
        SendMessageWhatsApp(SensorName[i]+'\ '+S)
        SendMessageSms(SensorName[i]+'\ '+S)



  with open(SensResStateFile,'w') as filehandle:
      json.dump(SensResStateNew, filehandle)



  ser.close()             # close port


  #print(GetTemp())



exit(0)


