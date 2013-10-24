# Battery Watchdog Data collection events
# filename: watchdogdatacollect.py
# Version 1.3 09/10/13
#
# contains event routines for data collection from the battery watchdog arduino
#
#

import sys
import time
import RPi.GPIO as GPIO

import MySQLdb as mdb

def  watchdogdatacollect(source, delay):

	print("watchdogdatacollect source:%s" % source)

	time.sleep(delay)
	# blink GPIO LED when it's run
        GPIO.setup(22, GPIO.OUT)
        GPIO.output(22, False)
        time.sleep(0.5)
        GPIO.output(22, True)
        time.sleep(0.5)
        GPIO.output(22, False)
        time.sleep(0.5)
        GPIO.output(22, True)
        time.sleep(0.5)
        GPIO.output(22, False)
        time.sleep(0.5)
        GPIO.output(22, True)



	# setup serial port to Arduino

	# signal Arduino to start listening

	# Send the GD (Get Data) Command

	# Read the value

	# stuff the values into variables



		
	"""
	# now we have the data, stuff it in the database

	try:
		print("trying database")
    		con = mdb.connect('localhost', 'root', 'bleh0101', 'ProjectCuracao');

    		cur = con.cursor()
		print "before query"

		query = 'INSERT INTO powersubsystemdata(TimeStamp, PiInputCurrent, PiInputVoltage, BatteryOutputCurrent, BatteryOutputVoltage, SolarOutputCurrent, SolarOutputVoltage, BatteryTemperature, PowerEfficiency) VALUES(UTC_TIMESTAMP(), %.3f, %.3f, %.3f, %.3f, %.3f, %.3f, %.3f,%.3f)' % (current40, voltage40, current41, voltage41, current44, voltage44, batterytemperature, powerEfficiency) 
		print("query=%s" % query)

		cur.execute(query)
	
		con.commit()
		#cur.execute ("SELECT * FROM powersubsystemdata");

		# get the number of rows in the resultset
		
		#numrows = int(cur.rowcount)
		#print "numrows=", numrows

		#for x in range(0,numrows):
    		#	row = cur.fetchone()
    		#	print row[0], "-->", row[1]
		
	except mdb.Error, e:
  
    		print "Error %d: %s" % (e.args[0],e.args[1])
    		con.rollback()
    		#sys.exit(1)
    
	finally:    
       		cur.close() 
        	con.close()

		del cur
		del con
	"""
