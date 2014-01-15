# select solar on Arduino 
# filename: selectSolar.py
# Version 1.0 01/11/14 
#
# contains select solar power for pi on arduino 
#
#

import sys
import time
import RPi.GPIO as GPIO
import serial

sys.path.append('./util')
sys.path.append('./state')
sys.path.append('./actions')
sys.path.append('./pclogging')
import pclogging
import util
import globalvars

sys.path.append('/home/pi/ProjectCuracao/main/config')

# if conflocal.py is not found, import default conf.py

# Check for user imports
try:
	import conflocal as conf
except ImportError:
	import conf


def returnNameFromInterrupt(interrupt):
	
	if (interrupt == 0):
		return "NOINTERRUPT"
		
	if (interrupt == 1):
		return "NOREASON"
		
	if (interrupt == 2):
		return "SHUTDOWN"
		
	if (interrupt == 3):
		return "GETLOG"
		
	if (interrupt == 4):
		return "ALARM1"
		
	if (interrupt == 5):
		return "ALARM2"
		
	if (interrupt == 6):
		return "ALARM3"

	if (interrupt == 7):
		return "REBOOT"

	return "UNKNOWNINTERRUPT"
		

def  selectSolar(source, delay):

	print("recieveInterruptFromBW source:%s" % source)

	time.sleep(delay)
	# blink GPIO LED when it's run
	GPIO.setmode(GPIO.BOARD)
        GPIO.setup(22, GPIO.OUT)
        GPIO.output(22, False)
        time.sleep(0.1)
        GPIO.output(22, True)
        time.sleep(0.1)
        GPIO.output(22, False)
        time.sleep(0.1)
        GPIO.output(22, True)
        time.sleep(0.1)
        GPIO.output(22, False)
        time.sleep(0.1)
        GPIO.output(22, True)



	# setup serial port to Arduino

	# interrupt Arduino to start listening

	GPIO.setmode(GPIO.BOARD)
    	GPIO.setup(7, GPIO.OUT, pull_up_down=GPIO.PUD_DOWN)	
	GPIO.output(7, False)
	GPIO.output(7, True)
	GPIO.output(7, False)
	

	# Send the WA (Get Data) Command
	ser = serial.Serial('/dev/ttyAMA0', 9600, timeout=1)
	ser.open()
	time.sleep(7.0)

	# send the first "are you there? command - RD - return from Arduino OK"
		
        response = util.sendCommandAndRecieve(ser, "RD")
	print("response=", response);
	
	if (response == "OK\n"):
		print "Good RD Response"
	else:
		print "bad response from RD"
		pclogging.log(pclogging.ERROR, __name__, "RD failed from Pi to BatteryWatchDog")
                ser.close()

		return globalvars.FAILED
	# Read the value

        response = util.sendCommandAndRecieve(ser, "SS")
	print("response=", response);
	

	if (len(response) > 0):
		pclogging.log(pclogging.INFO, __name__, "sent selectSolar command to Battery Watchdog " )
	else:
		# system setup

		pclogging.log(pclogging.ERROR, __name__, "SS failed from Pi to BatteryWatchDog")

		# say goodby  
        	response = util.sendCommandAndRecieve(ser, "GB")
		print("response=", response);
		ser.close()
		return globalvars.FAILED
	

        response = util.sendCommandAndRecieve(ser, "GB")
	print("response=", response);

	ser.close()
		
	# now we have the data, dostuff with it


	return True; 
