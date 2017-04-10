#!/usr/bin/python

"""
This file is part of pyadm300 (https://github.com/ThreeSixes/pyadm300).

pyadm300 is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

pyadm300 is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with pyadm300.  If not, see <http://www.gnu.org/licenses/>.

This file demostrates how to get communication with an ADM-300
running via callbacks.
"""

import time
import traceback
import adm300comm
from pprint import pprint

def dumpRawHex(data):
    """
    Dump raw data as hex.
    """
    
    try:
        #print(" ".join("{:02x}".format(ord(c)) for c in data))
        print(data)
    
    except:
        print("Exception:\n%s" %traceback.format_exc())
    
    return

def printAll(data):
    """
    Pretty print our data.
    """
    
    try:
        pprint(data)
    
    except:
        print("Exception:\n%s" %traceback.format_exc())
    
    return

print("Start ADM-300 communications test. Press Ctrl+C to quit.")

try:
    # Set up the communication object. Could be COM3 in Windows for example.
    adc = adm300comm.adm300comm(dev='/dev/ttyUSB0')
    
    # Set the callback we want to use to handle raw data [optional]
    adc.setRawCallback(dumpRawHex)
    
    # Set the callback we want to use to handle the dictionary of data.
    adc.setCallback(printAll)
    
    # Begin serial communication.
    adc.begin()
    
    print "Waiting for ADM-300 to be powered up..."
    
    # Loop until we see the ADM-300 power up or get valid data...
    while (not adc.gotPowerOn) and (not adc.gotSentence):
        # Wait.
        time.sleep(0.01)
    
    # If we haven't gotten reports yet...
    if not adc.gotSentence:
        print("Powered up. Waiting for ADM-300 to settle...")
        time.sleep(5)
        
        print("Requesting readings...")
        
        # Ask the ADM-300 for reports...
        adc.startReports()
    
    # Loop until an exception is thrown or we fire a KeyboardInterrupt/SystemExit exception.
    while True:
        time.sleep(10)

except (KeyboardInterrupt, SystemExit):
    print("\nShutting down...")
    
except:
    print("Explosion:\n%s" %traceback.format_exc())
    
finally:
    try:
        # Stop the serial reports.
        adc.stopReports()
        
        # Send threads the shutodwn command.
        adc.kill()
    
    except:
        None

print("Finally exiting.")
