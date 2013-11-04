# Takes a single picture on System 
# filename: takeSinglePicture.py
# Version 1.0  10/31/13
#
# takes a picture using the camera 
#
#

import sys
import time
import RPi.GPIO as GPIO
import serial
import picamera
import subprocess 
import MySQLdb as mdb
sys.path.append('/home/pi/ProjectCuracao/main/hardware')
sys.path.append('/home/pi/ProjectCuracao/main/pclogging')
sys.path.append('/home/pi/ProjectCuracao/main/util')
import pclogging
import util
import hardwareactions

OK = 0
ERROR = 1 
CRITICAL=50
ERROR=40
WARNING=30
INFO=20
DEBUG=10
NOTSET=0




def  sweepShutter(source, delay):

	print("sweepShutter source:%s" % source)
	GPIO.setmode(GPIO.BOARD)
	time.sleep(delay)
	# blink GPIO LED when it's run
        GPIO.setup(22, GPIO.OUT)
        GPIO.output(22, False)
        time.sleep(0.5)
        GPIO.output(22, True)
        time.sleep(0.5)

	hardwareactions.sweepshutter()


	time.sleep(3.0)




	pclogging.log(INFO, __name__, "Sweep Shutter")

def  takePicture(source):
	# take picture
	print "taking picture"
	output = subprocess.check_output ("raspistill -o /home/pi/RasPiConnectServer/static/picameraraw.jpg -t 0",shell=True, stderr=subprocess.STDOUT )
	output = subprocess.check_output("convert '/home/pi/RasPiConnectServer/static/picameraraw.jpg' -pointsize 72 -fill white -gravity SouthWest -annotate +50+100 'ProjectCuracao %[exif:DateTimeOriginal]' '/home/pi/RasPiConnectServer/static/picamera.jpg'", shell=True, stderr=subprocess.STDOUT)

	pclogging.log(INFO, __name__, source )

	print "finished taking picture"
	return

def  takeSinglePicture(source, delay):

	print("takeSinglePicture source:%s" % source)

	GPIO.setmode(GPIO.BOARD)
	time.sleep(delay)
	# blink GPIO LED when it's run
        GPIO.setup(22, GPIO.OUT)
        GPIO.output(22, False)
        time.sleep(0.5)
        GPIO.output(22, True)
        time.sleep(0.5)

	print GPIO.VERSION

	hardwareactions.openshutter()


	time.sleep(3.0)
	takePicture("Single Picture Taken With Shutter")

	hardwareactions.closeshutter()



	return
		
