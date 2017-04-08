"""
This file was originally part of the pyadm300 library by ThreeSixes (https://github.com/ThreeSixes).
"""
import Queue
import serial
import threading
import time
import adm300parse

class adm300comm:
    def __init__(self, dev="/dev/ttyUSB0", baud=300, timeout=0.1):
        """
        Canberra/NRC ADM-300 communication class.
        """
        
        # Set class-wide device comm properties.
        self.__dev = dev
        self.__baud = baud
        self.__timeout = timeout
        
        # Pre and post-command chars.
        self.__cmdPrefix = "\r\n" # [0x0d, 0x0a]
        self.__cmdTail = "}\r\n"
        
        # Command body
        self.__cmdStartMon = "U"
        self.__cmdStopMon = "X"
        self.__cmdClearDose = "e"
        self.__cmdAlarmAck = "g"
        self.__cmdRateAlmSet = "11" # Send 11....###SE
        self.__cmdDoseAlmSet = "22" # Send 22....###SE
        
        # Serial queue
        self.__txQ = Queue.Queue() # Data _to_ the ADM-300
        
        # This flag tells us if we should keep running.
        self.__keepRunning = True
        
        # Default callback.
        self.__lineCb = self.__dummy
        
        # Sentence parser
        self.__ap = adm300parse.adm300parse()
        
        # Set up serial comm object.
        try:
            # http://pyserial.readthedocs.io/en/latest/shortintro.html
            self.__ser = serial.Serial(self.__dev, self.__baud, timeout=self.__timeout)
        
        except:
            raise
    
    def __dummy(self, arg):
        """
        Dummy callback for data sentences.
        """
        
        return
    
    def __serThread(self):
        """
        This thread communicates with the ADM-300.
        """
        
        try:
            while self.__keepRunning:
                try:
                    # Do we have a command to send the ADM-300?
                    workItem = self.__txQ.get(False)
                    self.__ser.write(workItem)
                    
                except Queue.Empty:
                    None
                
                except:
                    raise
                
                # Grab a line.
                line = self.__ser.readline()
                # Is it 47 chars long?
                if len(line) == 47:
                    # Might be valid data. Send it on.
                    try:
                        # Parse the line into a dict.
                        line = self.__ap.parseSentence(line)
                        
                        # Send the dict to the callback.
                        self.__lineCb(line)
                    
                    except:
                        # Couldn't parse the line or call the callback...
                        None
                
                # Wait so we don't suck CPU up completely.
                time.sleep(0.01)
        except:
            raise
    
    def __sendCmd(self, cmdStr):
        """
        Queue the command to be sent to the ADM-300.
        """
        
        try:
            # Build the command string.
            sendCmd = "%s%s%s" %(self.__cmdPrefix, cmdStr, self.__cmdTail)
            
            # Write the thing to the port.
            self.__txQ.put(sendCmd, block=False)
        
        except:
            raise
        
        return
    
    def kill(self):
        """
        Flag threads to stop running.
        """
        
        # Set shutdown flag.
        self.__keepRunning = False
    
    def setCallback(self, cb):
        """
        Set a callback function for the line of data. It must accept one argument: a dictionary containg parsed ADM-300 data.
        """
        
        # Set the reference.
        self.__lineCb = cb
    
    def begin(self):
        """
        Spin up the serial comms thread.
        """
        
        self.__serWk = threading.Thread(target=self.__serThread)
        self.__serWk.daemon = True
        self.__serWk.start()
    
        
    def startReports(self):
        """
        Start acquiring readings from the ADM-300.
        """
        
        worked = True
        
        try:
            self.__sendCmd(self.__cmdStartMon)
        
        except:
            worked = False
        
        return worked
    
    
    def stopReports(self):
        """
        Stop acquiring readings from the ADM-300.
        """
        
        worked = True
        
        try:
            self.__sendCmd(self.__cmdStopMon)
        
        except:
            worked = False
        
        return worked
    
    
    def clearDose(self):
        """
        Clear accumulated dose on the ADM-300.
        """
        
        worked = True
        
        try:
            self.__sendCmd(self.__cmdClearDose)
        
        except:
            worked = False
        
        return worked
    
    
    def clearAlarm(self):
        """
        Clear active alarms on the ADM-300.
        """
        
        worked = True
        
        try:
            self.__sendCmd(self.__cmdAlarmAck)
        
        except:
            worked = False
        
        return worked
    
    
    def setDoseAlarm(self, doseThresh):
        """
        Set the accumulated dose alarm threshold on the ADM-300 to the specified float.
        !!! THIS IS NOT YET IMPLEMENTED !!!
        """
        
        worked = False
        
        return worked
    
    
    def setRateAlarm(self, rateThresh):
        """
        Set the dose rate alarm threshold on the ADM-300 to the specified float.
        !!! THIS IS NOT YET IMPLEMENTED !!!
        """
        
        worked = False
        
        return worked

# If this is just being called puke out a test string.
if __name__ == "__main__":
    from pprint import pprint
    import traceback
    
    print("Start ADM-300 communications test.")
    
    try:
        # Set up the communication object.
        adc = adm300comm()
        
        # Set the callback we want to use to handle the dictionary of data.
        adc.setCallback(pprint)
        
        # Begin serial communication.
        adc.begin()
        
        # Ask the ADM-300 for updates every 2 seconds nicely.
        adc.startReports()
        
        # Loop until an exception is thrown or we fire a KeyboardInterrupt/SystemExit exception.
        while True:
            time.sleep(1)
    
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