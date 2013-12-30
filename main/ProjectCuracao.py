"""
ProjectCuracao main program
JCS 9/10/2013 Version 1.0

This program runs the data collection, graph preperation, housekeeping and actions
"""

# shelves:
# 	datacollect - sensor data collection - disabled to RAM
#	graphprep - building system graphs
#	housekeeping - fan check , general health and wellfare
# 	alarmchecks - checks for system health alarms 
#	actions - specific actions scheduled (i.e. camera picture)
 
from datetime import datetime, timedelta
import sys
import time
import RPi.GPIO as GPIO
from apscheduler.scheduler import Scheduler
from apscheduler.jobstores.shelve_store import ShelveJobStore



sys.path.append('./graphprep')
sys.path.append('./datacollect')
sys.path.append('./hardware')
sys.path.append('./housekeeping')
sys.path.append('./pclogging')
sys.path.append('./actions')
sys.path.append('./util')
sys.path.append('./alarmchecks')
sys.path.append('./state')

import powerdatacollect
import powersupplygraph
import systemstatusgraph
import environmentalgraph
import environmentalgraph2
import batterywatchdogcurrentgraph 
import batterywatchdogvoltagegraph
import systemstatistics
import powersupplyvoltagesgraph 
import environdatacollect
import watchdogdatacollect

import hardwareactions
import useCamera
import pclogging
import util
import sendPictureEmail
import recieveInterruptFromBW 
import sendWatchDogTimer

import globalvars



# if conflocal.py is not found, import default conf.py

# Check for user imports
try:
	import conflocal as conf
except ImportError:
	import conf


# interrupt Handler

def handleInterrupt(reason):

	if (reason == globalvars.NOINTERRUPT):
		return

	if (reason == globalvars.NOREASON):
		return

	if (reason == globalvars.SHUTDOWN):
    		pclogging.log(pclogging.CRITICAL, __name__, "Project Curacao Pi Shutdown")
		util.shutdownPi()
		return

	if (reason == globalvars.GETLOG):
    		pclogging.log(pclogging.INFO, __name__, "Fetch Battery Watchdog Log ")
		return

	if (reason == globalvars.ALARM1):
    		pclogging.log(pclogging.INFO, __name__, "Battery Watchdog Alarm 1")
		return

	if (reason == globalvars.ALARM2):
    		pclogging.log(pclogging.INFO, __name__, "Battery Watchdog Alarm 2")
		return

	if (reason == globalvars.ALARM3):
    		pclogging.log(pclogging.INFO, __name__, "Battery Watchdog Alarm 3")
		return

	if (reason == globalvars.REBOOT):
    		pclogging.log(pclogging.CRITICAL, __name__, "Project Curacao Pi Reboot")
		util.rebootPi()
		return




# interrupt callback
def arduino_callback(channel):
    global hasBWInterrupted
    print('Edge detected on channel %s'%channel)
    hasBWInterrupted = True
    print("hasBWSet-2=", hasBWInterrupted)


if __name__ == '__main__':


    # system setup
    
    # log system startup
 
    pclogging.log(pclogging.INFO, __name__, "Project Curacao Startup")
    util.sendEmail("test", "ProjectCuracao Pi Startup", "The Raspberry Pi has rebooted.", conf.notifyAddress,  conf.fromAddress, "");
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BOARD)	
    GPIO.setup(7, GPIO.OUT, pull_up_down=GPIO.PUD_DOWN)
    # set initial hardware actions 
    hardwareactions.setfan(False)

    # arudino interrupt - from battery watchdog
    hasBWInterrupted = False  # interrupt state variable
    #GPIO.setup(11, GPIO.IN )
    GPIO.setup(11, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    #GPIO.add_event_detect(11, GPIO.RISING, callback=arduino_callback)  # add rising edge detection on a channel
    #GPIO.add_event_detect(11, GPIO.RISING)  # add rising edge detection on a channel



    scheduler = Scheduler()
    

    job = scheduler.add_cron_job(powerdatacollect.datacollect5minutes, minute="*/5", args=['main', 0])    
    job = scheduler.add_cron_job(watchdogdatacollect.watchdogdatacollect, minute="*/5", args=['main', 30])    
    job = scheduler.add_cron_job(environdatacollect.environdatacollect, minute="*/15", args=['main', 10])    
    job = scheduler.add_cron_job(systemstatistics.systemstatistics15minutes, minute="*/15", args=['main', 20])    



    job = scheduler.add_cron_job(powersupplygraph.powersystemsupplygraph, minute="*/15", args=['main',5,60])    
    job = scheduler.add_cron_job(powersupplyvoltagesgraph.powersystemsupplyvoltagegraph, minute="*/15", args=['main',5, 120])    

    job = scheduler.add_cron_job(systemstatusgraph.systemstatusgraph, minute="*/15", args=['main',5,180])    
    
    job = scheduler.add_cron_job(environmentalgraph.environmentalgraph, minute="*/15", args=['main',5, 240])    
    job = scheduler.add_cron_job(environmentalgraph2.environmentalgraph2, minute="*/15", args=['main',5,300])    

    job = scheduler.add_cron_job(batterywatchdogcurrentgraph.batterywatchdogcurrentgraph, minute="*/15", args=['main',5,360])    
    job = scheduler.add_cron_job(batterywatchdogvoltagegraph.batterywatchdogvoltagegraph, minute="*/15", args=['main',5,720])    


    # camera 
    job = scheduler.add_cron_job(useCamera.takeSinglePicture, hour="*", args=['main',50])    
    # send daily picture
    job = scheduler.add_cron_job(sendPictureEmail.sendPictureEmail, hour="22",minute="20", args=['main',0])    


    sys.stdout.write('Press Ctrl+C to exit\n')
    scheduler.start()

    scheduler.print_jobs()

    while True:
        sys.stdout.write('.'); sys.stdout.flush()
	myDateString = time.strftime("%Y-%m-%d", time.gmtime())
	myTimeString = time.strftime("%H:%M:%S", time.gmtime())
	print "-%s %s-" % (myDateString, myTimeString)

	print ("hasBW=", hasBWInterrupted)
	# respond to interrupt
	#if (hasBWInterrupted == True):
	#if ((GPIO.event_detected(11) == True) or (hasBWInterrupted == True)):
	if ((GPIO.input(11) == True) or (hasBWInterrupted == True)):
		# The routine will be executed now 
		hasBWInterrupted = True;
		result = recieveInterruptFromBW.recieveInterruptFromBW("test", 1)	
		print("result=", result);
		if (result > globalvars.FAILED):
			hasBWInterrupted = False
			#interrupt handled
			sys.stdout.write("BW Interrupt Handled\n")
        		sys.stdout.flush()

			# now do the interrupt reason
			handleInterrupt(result)

		
	if (hasBWInterrupted == True):
		time.sleep(15)
	else:
		time.sleep(30)
 
 

