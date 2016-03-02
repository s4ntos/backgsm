#!/usr/bin/env python
# vim: ai ts=4 sts=4 et sw=4
# see LICENSE file (it's BSD)


import time
import pprint 
import subprocess
import sys
from pygsm import GsmModem
from optparse import OptionParser
import socket

DETACHED_PROCESS = 0x00000008

parser = OptionParser()
parser.add_option("-p", dest="pin", default=1234,
                  help="Pin for the system")
parser.add_option("-m", dest="msisdn", action="append", type="string", 
                  help="Msidns that require access add -m with the numbers")
(options, args) = parser.parse_args()
pprint.pprint("Waiting for commands from: %s" % options.msisdn)
# all arguments to GsmModem.__init__ are optional, and passed straight
# along to pySerial. for many devices, this will be enough:
gsm = GsmModem(
    port="/dev/ttyUSB0").boot(pin = options.pin)

class do_something():
     def __init__ (self, *args, **kwargs):
         if "gsm" in kwargs:
              self.gsm = kwargs.pop("gsm")
     def Test(self,msisdn):
	 gsm.send_sms(msisdn,"it works AHAHAHAHAH") 
     def Ping(self,msisdn):
	 gsm.send_sms(msisdn,time.strftime("%a, %d %b %Y %H:%M:%S +0000", time.gmtime()))
     def Connect(self,msisdn):
         pid = subprocess.Popen([sys.executable, "/usr/bin/wvdial internet"], creationflags=DETACHED_PROCESS).pid
         gsm.send_sms(msisdn,"My ip is 1.1.1.1 whats your ip ?")
         message = gsm.next_message(fetch=True)
         while message is None:
	      time.sleep(1)
              message = gsm.next_message(fetch=True)
         try:
             socket.inet_aton(message.text) # legal
         except socket.error: # Not legal
             gsm.send_sms(msisdn,"Disconnecting your IP is invalid please try again in 30s")
         print("Adding routing for you %s" % message.text)

Actions = do_something()

print "Waiting for network..."
s = gsm.wait_for_network()
# start query the memory
try:
  while True:
    message = gsm.next_message(fetch=True)
    if message is None:
	time.sleep(1)
    else:
        pprint.pprint("Received message: %s " % message)
        if any(message.sender in s for s in options.msisdn):
	     print "Your command master is: %s" % message.text
	     try:
                func = getattr(Actions,message.text)
		func(message.sender)
             except Exception, e:
		  exp = '*** I made a booboo : %s: %s' % (e.__class__, e)
		  print exp

             
except Exception, e:
    exp = '*** Caught exception: %s: %s' % (e.__class__, e)
    print exp
    quit(1)
