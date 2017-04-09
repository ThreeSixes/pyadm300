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
"""

import time
import traceback
import adm300comm
from pprint import pprint

print("Start ADM-300 communications test. Press Ctrl+C to quit.")

try:
    # Set up the communication object.
    adc = adm300comm.adm300comm()
    
    # Set the callback we want to use to handle raw data [optional]
    adc.setRawCallback(pprint)
    
    # Set the callback we want to use to handle the dictionary of data.
    adc.setCallback(pprint)
    
    # Begin serial communication.
    adc.begin()
    
    # Ask the ADM-300 for updates every 2 seconds nicely.
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
