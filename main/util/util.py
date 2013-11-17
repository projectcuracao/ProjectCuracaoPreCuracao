#
#
# general utilities
# JCS 10/30/13
#
#
import time
import sys

sys.path.append('/home/pi/ProjectCuracao/main/config')

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


def returnPercentLeftInBattery(currentVoltage, maxVolt):

	scaledVolts = currentVoltage / maxVolt
	
	if (scaledVolts > 1.0):
		scaledVolts = 1.0
	
	
	if (scaledVolts > .9686):
		returnPercent = 10*(1-(1.0-scaledVolts)/(1.0-.9686))+90
		return returnPercent

	if (scaledVolts > 0.9374):
		returnPercent = 10*(1-(0.9686-scaledVolts)/(0.9686-0.9374))+80
		return returnPercent


	if (scaledVolts > 0.9063):
		returnPercent = 30*(1-(0.9374-scaledVolts)/(0.9374-0.9063))+50
		return returnPercent

	if (scaledVolts > 0.8749):
		returnPercent = 30*(1-(0.8749-scaledVolts)/(0.9063-0.8749))+20
		return returnPercent

	
	if (scaledVolts > 0.8437):
		returnPercent = 17*(1-(0.8437-scaledVolts)/(0.8749-0.8437))+3
		return returnPercent


   	if (scaledVolts > 0.8126):
		returnPercent = 1*(1-(0.8126-scaledVolts)/(0.8437-0.8126))+2
		return returnPercent



	if (scaledVolts > 0.7812):
		returnPercent = 1*(1-(0.7812-scaledVolts)/(0.7812-0.8126))+1
		return returnPercent

	return 0	




def sendEmail(source, message, subject, toaddress, fromaddress, filename):

	# if conflocal.py is not found, import default conf.py

	# Check for user imports
	try:
     		import conflocal as conf
	except ImportError:
     		import conf

	# Import smtplib for the actual sending function
	import smtplib

	# Here are the email package modules we'll need
	from email.mime.image import MIMEImage
	from email.mime.multipart import MIMEMultipart
	from email.mime.text import MIMEText

	COMMASPACE = ', '

	# Create the container (outer) email message.
	msg = MIMEMultipart()
	msg['Subject'] = subject 
	# me == the sender's email address
	# family = the list of all recipients' email addresses
	msg['From'] = fromaddress
	msg['To'] =  toaddress
	#msg.attach(message) 

	mainbody = MIMEText(message, 'plain')
	msg.attach(mainbody)

	# Assume we know that the image files are all in PNG format
    	# Open the files in binary mode.  Let the MIMEImage class automatically
       	# guess the specific image type.
	if (filename != ""):
    		fp = open(filename, 'rb')
       		img = MIMEImage(fp.read())
    		fp.close()
        	msg.attach(img)

	# Send the email via our own SMTP server.

	# open up a line with the server
	s = smtplib.SMTP("smtp.gmail.com", 587)
	s.ehlo()
	s.starttls()
	s.ehlo()

	# login, send email, logout
	s.login(conf.mailUser, conf.mailPassword)
	s.sendmail(conf.mailUser, toaddress, msg.as_string())
	#s.close()


	s.quit()

	return 0

