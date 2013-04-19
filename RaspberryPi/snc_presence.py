#!/usr/bin/python
# Import required Python libraries
from SOAPpy import SOAPProxy
import time
import RPi.GPIO as GPIO
def updateRecord(status):
        # instance to send to
        instance='<your instance name>'
        # username/password
        username='<your username>'
        password='<your password>'
        # proxy - NOTE: ALWAYS use https://INSTANCE.service-now.com, not https://www.service-now.com/INSTANCE for web services URL from now on!
        proxy = 'https://'+username+':'+password+'@'+instance+'.service-now.com/sys_user.do?SOAP'
        namespace = 'http://www.service-now.com/'
        server = SOAPProxy(proxy, namespace)
        # uncomment these for LOTS of debugging output
        #server.config.dumpHeadersIn = 1
        #server.config.dumpHeadersOut = 1
        #server.config.dumpSOAPOut = 1
        #server.config.dumpSOAPIn = 1
        response = server.update(sys_id='<sys_id of the user record this will update>',u_presence=status)
        return response
# Use BCM GPIO references
# instead of physical pin numbers
GPIO.setmode(GPIO.BCM)
# Define GPIO to use on Pi
GPIO_TRIGGER = 24
GPIO_ECHO = 24
# Set pin as output
GPIO.setup(GPIO_TRIGGER,GPIO.OUT)  # Trigger
# Set trigger to False (Low)
GPIO.output(GPIO_TRIGGER, False)
# Allow module to settle
time.sleep(0.5)
counter = 0
lastStatus = 'true'
while True:
        #print "Ultrasonic Measurement"
        #time.sleep(1)
        # Set pin as output
        GPIO.setup(GPIO_TRIGGER,GPIO.OUT)  # Trigger
        # Set trigger to False (Low)
        #GPIO.output(GPIO_TRIGGER, False)
        # Allow module to settle
        time.sleep(0.05)
        # Send 10us pulse to trigger
        GPIO.output(GPIO_TRIGGER, True)
        time.sleep(0.00001)
        GPIO.output(GPIO_TRIGGER, False)
        start = time.time()
        # Set pin as input
        GPIO.setup(GPIO_ECHO,GPIO.IN)      # Echo
        while GPIO.input(GPIO_ECHO)==0:
          start = time.time()
        while GPIO.input(GPIO_ECHO)==1:
          stop = time.time()
        # Calculate pulse length
        elapsed = stop-start
        # Distance pulse travelled in that time is time
        # multiplied by the speed of sound (cm/s)
        distance = elapsed * 34000
        # That was the distance there and back so halve the value
        distance = distance / 2
        print "Distance : %.1f" % distance
        if distance > 60:
          atdesk = 'false'
          print 'Not at desk: ' + str(counter)
        else:
          atdesk = 'true'
          print 'At desk: ' + str(counter)
        if atdesk == lastStatus and counter > 30:
          print 'Desk Status Changed'
          updatedSys = updateRecord(atdesk)
          counter = 0
          print updatedSys
        elif atdesk != lastStatus:
          print 'Initial Desk Status Change'
          counter = 1
        elif counter > 0:
          print 'Desk Status Not Changed'
          counter = counter + 1
        lastStatus = atdesk
        # Reset GPIO settings
        GPIO.cleanup()
