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
import gc

from apscheduler.scheduler import Scheduler
from apscheduler.jobstores.shelve_store import ShelveJobStore



sys.path.append('./graphprep')
sys.path.append('./datacollect')
sys.path.append('./hardware')
sys.path.append('./housekeeping')
sys.path.append('./pclogging')

import powerdatacollect
import powersupplygraph
import systemstatusgraph
import environmentalgraph
import environmentalgraph2
import systemstatistics
import powersupplyvoltagesgraph 
import environdatacollect

import hardwareactions

import pclogging


if __name__ == '__main__':

    CRITICAL=50
    ERROR=40
    WARNING=30
    INFO=20
    DEBUG=10
    NOTSET=0

    # system setup
    
    # log system startup
 
    pclogging.log(CRITICAL, __name__, "Project Curacao Startup")

    # set initial hardware actions 
    hardwareactions.setfan(False)




    scheduler = Scheduler()
    

    job = scheduler.add_cron_job(powerdatacollect.datacollect5minutes, minute="*/5", args=['main', 0])    
    job = scheduler.add_cron_job(environdatacollect.environdatacollect, minute="*/15", args=['main', 5])    
    job = scheduler.add_cron_job(systemstatistics.systemstatistics15minutes, minute="*/15", args=['main', 10])    



    job = scheduler.add_cron_job(powersupplygraph.powersystemsupplygraph, minute="*/15", args=['main',5,60])    
    job = scheduler.add_cron_job(powersupplyvoltagesgraph.powersystemsupplyvoltagegraph, minute="*/15", args=['main',5, 120])    

    job = scheduler.add_cron_job(systemstatusgraph.systemstatusgraph, minute="*/15", args=['main',5,180])    
    
    job = scheduler.add_cron_job(environmentalgraph.environmentalgraph, minute="*/15", args=['main',5, 240])    
    job = scheduler.add_cron_job(environmentalgraph2.environmentalgraph2, minute="*/15", args=['main',5,300])    



    sys.stdout.write('Press Ctrl+C to exit\n')
    scheduler.start()

    scheduler.print_jobs()

    while True:
        sys.stdout.write('.'); sys.stdout.flush()
	time.sleep(30)
 
 


