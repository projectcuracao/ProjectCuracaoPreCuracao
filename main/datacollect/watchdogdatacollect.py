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
import serial

import MySQLdb as mdb
sys.path.append('./pclogging')
sys.path.append('./util')
import pclogging
import util

OK = 0
ERROR = 1 
CRITICAL=50
ERROR=40
WARNING=30
INFO=20
DEBUG=10
NOTSET=0




def  watchdogdatacollect(source, delay):

	print("watchdogdatacollect source:%s" % source)

	time.sleep(delay)
	# blink GPIO LED when it's run
	GPIO.setmode(GPIO.BOARD)
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

	# interrupt Arduino to start listening

	GPIO.setmode(GPIO.BOARD)
    	GPIO.setup(7, GPIO.OUT, pull_up_down=GPIO.PUD_DOWN)	
	GPIO.output(7, False)
	GPIO.output(7, True)
	GPIO.output(7, False)
	

	# Send the GD (Get Data) Command
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
		pclogging.log(ERROR, __name__, "RD failed from Pi to BatteryWatchDog")
                ser.close()
		return
	# Read the value

        response = util.sendCommandAndRecieve(ser, "GD")
	print("response=", response);
	


	# stuff the values into variables
	splitList = response.split(',')
	print(splitList)	

	if (len(splitList) == 11):
		ArInputVoltage = float(splitList[0])
        	ArInputCurrent = float(splitList[1])
		SolarCellVoltage = float(splitList[2])
		SolarCellCurrent = float(splitList[3])
		BatteryVoltage = float(splitList[4])
		BatteryCurrent = float(splitList[5])
		OutsideHumidity = float(splitList[6])
		OutsideTemperature = float(splitList[7])
		LastReboot = splitList[8]
		BatteryTemperature = float(splitList[9])
		FreeMemory = float(splitList[10])
	else:
		print "bad response from GD"
		# system setup

		pclogging.log(ERROR, __name__, "GD failed from Pi to BatteryWatchDog")

		# say goodby  
        	response = util.sendCommandAndRecieve(ser, "GB")
		print("response=", response);
		ser.close()
		return
	
	print("ArInputCurrent =", ArInputCurrent)

     	# power efficiency
	if ( (SolarCellCurrent*SolarCellVoltage+BatteryCurrent*BatteryVoltage) == 0):
       		powerEfficiency = 10000.0; 
	else:
		powerEfficiency = (ArInputCurrent*ArInputVoltage/(SolarCellCurrent*SolarCellVoltage+BatteryCurrent*BatteryVoltage))*100


        # if power Efficiency < 0, then must be plugged in so add 500ma @ 5V
        if (powerEfficiency < 0.0):
		if ((SolarCellCurrent*SolarCellVoltage+BatteryCurrent*BatteryVoltage+5.0*500.0) == 0.0):
			powerEfficiency = 10000.0;
		else:	
        		powerEfficiency = (ArInputCurrent*ArInputVoltage/(SolarCellCurrent*SolarCellVoltage+BatteryCurrent*BatteryVoltage+5.0*500.0))*100



	# say goodby  
        response = util.sendCommandAndRecieve(ser, "GB")
	print("response=", response);

	ser.close()
		
	# now we have the data, stuff it in the database

	try:
		print("trying database")
    		con = mdb.connect('localhost', 'root', 'bleh0101', 'ProjectCuracao');

    		cur = con.cursor()
		print "before query"

		query = 'INSERT INTO batterywatchdogdata(TimeStamp, ArInputCurrent, ArInputVoltage, BatteryOutputCurrent, BatteryOutputVoltage, SolarOutputCurrent, SolarOutputVoltage, BatteryTemperature, PowerEfficiency, LastReboot, OutsideTemperature, OutsideHumidity, FreeMemory) VALUES(UTC_TIMESTAMP(), %.3f, %.3f, %.3f, %.3f, %.3f, %.3f, %.3f,%.3f,%s, %.3f, %.3f, %i)' % (ArInputCurrent, ArInputVoltage, BatteryCurrent, BatteryVoltage, SolarCellCurrent, SolarCellVoltage, BatteryTemperature, powerEfficiency, LastReboot, OutsideTemperature, OutsideHumidity, FreeMemory) 
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
