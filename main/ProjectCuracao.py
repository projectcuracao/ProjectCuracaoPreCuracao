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

# if conflocal.py is not found, import default conf.py

# Check for user imports
try:
	import conflocal as conf
except ImportError:
	import conf


if __name__ == '__main__':

    CRITICAL=50
    ERROR=40
    WARNING=30
    INFO=20
    DEBUG=10
    NOTSET=0

    # system setup
    
    # log system startup
 
    pclogging.log(pclogging.CRITICAL, __name__, "Project Curacao Startup")
    util.sendEmail("test", "ProjectCuracao Pi Bootup", "The Raspberry Pi has rebooted.", conf.notifyAddress,  conf.fromAddress, "");
    GPIO.setmode(GPIO.BOARD)	
    GPIO.setup(7, GPIO.OUT, pull_up_down=GPIO.PUD_DOWN)
    # set initial hardware actions 
    hardwareactions.setfan(False)




    scheduler = Scheduler()
    

    job = scheduler.add_cron_job(powerdatacollect.datacollect5minutes, minute="*/5", args=['main', 0])    
    job = scheduler.add_cron_job(watchdogdatacollect.watchdogdatacollect, minute="*/5", args=['main', 15])    
    job = scheduler.add_cron_job(environdatacollect.environdatacollect, minute="*/15", args=['main', 5])    
    job = scheduler.add_cron_job(systemstatistics.systemstatistics15minutes, minute="*/15", args=['main', 10])    



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
	time.sleep(30)
 
 


