#!/bin/sh

# alarm system

# main circle

while true;
do 

  /usr/bin/python3 /usr/sbin/get-bolid.py
  /usr/bin/python3 /usr/sbin/get-temp.py


done
