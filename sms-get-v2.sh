#!/bin/bash

WORKDIR='/var/spool/gammu/inbox'
VALID_SENDER="+79126021816"

DATAFILE='/tmp/ramdisk/SensorState.txt'
DATAFILE2='/tmp/ramdisk/SensorState.txt'

SEND_SMS_REPORT()
{

D1=$(cat $DATAFILE | awk '{split($0,s,","); print s[6]}')
D2=$(cat $DATAFILE | awk '{split($0,s,","); print s[8]}')
D3=$(cat $DATAFILE | awk '{split($0,s,","); print s[9]}')
D4=$(cat $DATAFILE | awk '{split($0,s,","); print s[10]}')
D5=$(cat $DATAFILE | awk '{split($0,s,","); print s[11]}')

MESS="PR=$D1 GasB=$D2 SmokB=$D3 Smok1=$D4 Smok2=$D5"

echo $MESS

/usr/bin/gammu-smsd-inject TEXT 89126021816 -text  "$MESS" &

}




while true;
do

for file in $WORKDIR/*
do
  # file name
  echo $file

  SMS_SENDER=$(echo $file | awk '{split($0,s,"_"); print s[4]}')

  echo $SMS_SENDER

  SMS_TEXT=$(cat $file | tr -d '[:space:]')

  echo $SMS_TEXT


   if [ "$SMS_SENDER" = "+79126021816" ];
   then
     echo "Valid sender!"

     if [ "$SMS_TEXT" = "report" ] || [ "$SMS_TEXT" = "Report" ] ;
     then
       echo "Valid SMS command"
         if [ -f "/tmp/ramdisk/ArmedStateFile"];
         then
           DATAFILE='/tmp/ramdisk/SensorState.txt';
           SEND_SMS_REPORT;
         fi
           DATAFILE='/tmp/ramdisk/SensResData.txt';
           SEND_SMS_REPORT;

       rm $file
     fi


   fi

   echo

done

sleep 5

done
