#!/usr/bin/python
# hardwareactions.py
# routines for setting hardware for ProjectCuracao

import sys
import time
import RPi.GPIO as GPIO


def setfan(value):

	#return TRUE if successful (can't tell with Fan - I suppose we could by looking at current)

	if (value == True):
 	      GPIO.setup(18, GPIO.OUT)
              GPIO.output(18, True)
              f = open("/home/pi/ProjectCuracao/main/state/fanstate.txt", "w")
              f.write("1")
              f.close()
              return True

        if (value == False):
              GPIO.setup(18, GPIO.OUT)
              GPIO.output(18, False)
              f = open("/home/pi/ProjectCuracao/main/state/fanstate.txt", "w")
              f.write("0")
              f.close()
              return True

        return True


