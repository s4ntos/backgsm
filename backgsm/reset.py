#!/usr/bin/env python
# vim: ai ts=4 sts=4 et sw=4
# see LICENSE file (it's BSD)


import time
import pprint 
from pygsm import GsmModem


# all arguments to GsmModem.__init__ are optional, and passed straight
# along to pySerial. for many devices, this will be enough:
gsm = GsmModem(
    port="/dev/ttyUSB0",
    logger=GsmModem.debug_logger).boot()


print "Reseting for network..."
s = gsm.reset()
