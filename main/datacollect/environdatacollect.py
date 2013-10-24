# environmental data collection events
# filename: environdatacollect.py
# Version 1.3 09/10/13
#
# contains event routines for data collection
#
#

import sys
import time

import RPi.GPIO as GPIO
import re
import math
import subprocess

from luxmeter import Luxmeter
from Adafruit_BMP085 import *

import MySQLdb as mdb

def  environdatacollect(source, delay):

	print("environdatacollect source:%s" % source)

	# delay to not "everything happen at once"
	time.sleep(delay)
	# blink GPIO LED when it's run
	# double blink
        GPIO.setup(22, GPIO.OUT)
        GPIO.output(22, False)
        time.sleep(0.5)
        GPIO.output(22, True)
        time.sleep(0.5)
        GPIO.output(22, False)
        time.sleep(0.5)
        GPIO.output(22, True)

	# now read in all the required data
	# Inside Temperature
	# Barometric Pressure

        # Initialise the BMP085 and use STANDARD mode (default value)
        # bmp = BMP085(0x77, debug=True)
        # bmp = BMP085(0x77)

        # To specify a different operating mode, uncomment one of the following:
        # bmp = BMP085(0x77, 0)  # ULTRALOWPOWER Mode
        # bmp = BMP085(0x77, 1)  # STANDARD Mode
        # bmp = BMP085(0x77, 2)  # HIRES Mode
        bmp = BMP085(0x77, 3)  # ULTRAHIRES Mode



	pressure = -1000.0 # bad data
	insidetemperature =-1000.0
        try:
               pressure = bmp.readPressure()/100.0
               insidetemperature = bmp.readTemperature()

        except IOError as e:
               print "I/O error({0}): {1}".format(e.errno, e.strerror)
        except:
               print "Unexpected error:", sys.exc_info()[0]
               raise


	# Inside Humidity

        insidehumidity = -1000.0 # bad data
        try:
                maxCount = 20
                count = 0
                while (count < maxCount):
                    output = subprocess.check_output(["/home/pi/ProjectCuracao/main/hardware/Adafruit_DHT_MOD", "22", "23"]);
                    print "count=", count
                    print output
                    # search for humidity printout
                    matches = re.search("Hum =\s+([0-9.]+)", output)

                    if (not matches):
                          count = count + 1
                          time.sleep(3.0)
                          continue
                    insidehumidity = float(matches.group(1))
                    count = maxCount



        except IOError as e:
                 print "I/O error({0}): {1}".format(e.errno, e.strerror)
        except:
                 print "Unexpected error:", sys.exc_info()[0]
                 raise




	# Outside Temperature

	# these are NOT implemented yet.  Comes from Arduino
	outsidetemperature = insidetemperature
	# Outside Humidity
	# these are NOT implemented yet.  Comes from Arduino
	outsidehumidity = insidehumidity

	# Luminosity
	luminosity = -1000.0 # bad data
        try:
              oLuxmeter=Luxmeter()

              luminosity = oLuxmeter.getLux()
        except IOError as e:
              print "I/O error({0}): {1}".format(e.errno, e.strerror)
        except:
              print "Unexpected error:", sys.exc_info()[0]
              raise

	# Fan State
	
	# read from fan state file
        try:
		f = open("./state/fanstate.txt", "r")
		tempString = f.read()
        	f.close()
        	fanstate = int(tempString)
	except IOError as e:
		fanstate = 0

	print "fanstate=", fanstate

	# now we have the data, stuff it in the database

	try:
		print("trying database")
    		con = mdb.connect('localhost', 'root', 'bleh0101', 'ProjectCuracao');

    		cur = con.cursor()
		print "before query"

		query = 'INSERT INTO environmentaldata(TimeStamp, InsideTemperature, InsideHumidity, OutsideTemperature, OutsideHumidity, BarometricPressure, Luminosity, FanState) VALUES(UTC_TIMESTAMP(), %.3f, %.3f, %.3f, %.3f, %.3f, %.3f, %i)' % (insidetemperature, insidehumidity, outsidetemperature, outsidehumidity, pressure, luminosity, fanstate) 
		print("query=%s" % query)

		cur.execute(query)
	
		con.commit()
		
	except mdb.Error, e:
  
    		print "Error %d: %s" % (e.args[0],e.args[1])
    		con.rollback()
    		#sys.exit(1)
    
	finally:    
       		cur.close() 
        	con.close()

		del cur
		del con

