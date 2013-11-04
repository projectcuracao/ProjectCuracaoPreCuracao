#
#
# general utilities
# JCS 10/30/13
#
#
import time


def  sendCommandAndRecieve(ser,command):

     timeout = True
     # send the first "are you there? command - RD - return from Arduino OK"
     print("sending command=",command)
     ser.write(command+'\n') 
     # wait no more than 10 seconds
     t = 10
                
     st = ''
     initTime = time.time()
     while True:
               st +=  ser.readline()
	       if (len(st) > 0):
			break;
	       print("after readline.  st=",st)
               if timeout and (time.time() - initTime > t) :
                    break


     return st	


