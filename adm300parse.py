"""
This file was originally part of the pyadm300 library by ThreeSixes (https://github.com/ThreeSixes).
"""

import math

class adm300parse:
    def __init__(self):
        """
        Python class parse sentences from Canberra/NRC ADM-300 survey meter.
        """
        
        # Baud rate
        self.__baud = 300
        
        # Fixed-length sentence.
        self.__sentenceLen = 47
        
        # Data sentence info
        self.__readingOver = "]"
        
        # These chars are sent on boot...
        self.__bootChars = [0x00, 0x00] # FIX ME!!!
        
        # Symbols.
        self.__symR = "R/hr"
        self.__symSv = "Sv/hr" # Not implemented.
        
        # Structure of readings.
        # Example:
        # 01a020-1 003-1 000-1 ...L.I00U00A2521 600-1 55]
        self.__readingStruct = {
            'seqNo': [0, 2], # Sequence number. Increments per line.
            'id': [2, 3], # ADM-300 id is "a"
            'rtRaw': [3, 8], # Raw rate in NNNSE format
            'dsRaw': [9, 14], # Dose rate DDSE
            'uRtRaw': [15, 20], # Unfiltered dose rate UUUSE
            'flgRaw': [21, 25], # Raw flags . = False, R = rate alam, D = dose alarm, B = battery low, G = high-range GM / L = Low-range GM,
            'dbgRaw': [26, 37], # Debug field.
            'dbgDat': [38, 43], # Debug data.
            'cksum': [44, 46] # Checksum
        }
    
    def parseNumNotation(self, sciStr):
        """
        Take numbers in NNNSE or NNSE notation and convert them to decimals.
        """
        
        # Return number.
        num = 0
        
        try:
            # Check string length.
            if len(sciStr) == 4:
                # Split out the number.
                num = float(sciStr[0:2])
                # - and set the divisor.
                divisor = 10000.0
            
            elif len(sciStr) == 5:
                # Split out the number.
                num = float(sciStr[0:3])
                # - and set the divisor.
                divisor = 100000.0
            
            else:
                raise ValueError
            
            # Scale the number and get the exponent.
            num /= divisor
            exp = int(sciStr[-1])
            
            # Get the sign string.
            signStr = sciStr[-2]
            
            # Figure out where to put the decimal point.
            if signStr == "-":
                # Move smaller.
                num *= math.pow(.1, exp)
            
            elif signStr == "+":
                # Move larger.
                num *= math.pow(10.0, exp)
            
            else:
                raise ValueError
        
        except:
            raise
        
        return num
    
    
    def parseDebug(self, debugRaw, debugDat):
        """
        Parse debug data and dump a dictionary containing the new data.
        """
        
        retVal = {}
        
        try:
            # Get the debug data ID.
            debugID = debugRaw[10:11]
            
            # Figure out what's in the debug data field and handle it.
            if debugID == "1":
                # We have a dose rate alarm threshold.
                retVal.update({'rateAlarmThresh': round(self.parseNumNotation(debugDat), 6)})
            
            elif debugID == "2":
                # We have a dose alarm threshold.
                retVal.update({'doseAlarmThresh': round(self.parseNumNotation(debugDat), 6)})
            
            else:
                # ???
                retVal.update({
                    'debugDataID': debugID,
                    'debugData': debugDat,
                    'debugUnk': debugRaw[1:10]
                })
            
            # Tack on additional data.
            retVal.update({
                'probeFlag': debugRaw[0:1]
            })
        
        except:
            raise
        
        return retVal 
    
    
    def parseSentence(self, sentence):
        """
        Parse a serial sentence from the ADM-300.
        """
        
        # Valid flag - assume it's invalid until we have validated it.
        valid = False
        
        # Return value.
        retVal = {}
        
        try:
            # Strip whitespace.
            sentence = sentence.strip()
            
            # Do we have a sentence of the appropriate length with the correct ending char?
            if (len(sentence) == self.__sentenceLen) and (sentence[46:47] == self.__readingOver):
                # For each entry in the 
                for part in self.__readingStruct:
                    # Tack in pieces of the structure.
                    retVal.update({part: sentence[self.__readingStruct[part][0]:self.__readingStruct[part][1]]})
                
                # Get flag.
                rFlg = retVal.pop('flgRaw')
                
                # Split flag strings...
                rtAl = rFlg[0:1]
                doAl = rFlg[1:2]
                btAl = rFlg[2:3]
                prb = rFlg[3:4]
                
                # Rate alarm triggered?
                if rtAl == ".":
                    rateAlarm = False
                elif rtAl == "R":
                    rateAlarm = True
                else:
                    raise ValueError
                
                # Dose alarm triggered?
                if doAl == ".":
                    doseAlarm = False
                elif doAl == "D":
                    doseAlarm = True
                else:
                    raise ValueError
                
                # Dose alarm triggered?
                if btAl == ".":
                    battAlarm = False
                elif btAl == "B":
                    battAlarm = True
                else:
                    raise
                
                # Which probe are we getting info from?
                if prb == "L":
                    probe = "Internal low range"
                elif prb == "G":
                    probe = "Internal high range"
                else:
                    # Not sure what this changes to if there's an external probe attached...
                    probe = "Unknown"
                
                # Update our return value with data.
                retVal.update({
                    'seqNo': int(retVal['seqNo']), # Sequence number. Starts at 1 when readings start.
                    'doseRt': round(self.parseNumNotation(retVal.pop('rtRaw')), 6), # Dose rate.
                    'doseAcc': round(self.parseNumNotation(retVal.pop('dsRaw')), 6), # Accumulated dose.
                    'doseRtUnf': round(self.parseNumNotation(retVal.pop('uRtRaw')), 6), # "Unfiltered" dose rate.
                    'rateAlarm': rateAlarm, # Is the dose rate alarm active?
                    'doseAlarm': doseAlarm, # Is the accumulated dose alarm active?
                    'battAlarm': battAlarm, # Is the low battery alarm active?
                    'probe': probe, # Probe information.
                    'unit': self.__symR, # This should be set up as either R/hr or Sv/hr depending on decimal placement in dose rate? IDK.
                    'checksum': int(retVal.pop('cksum'), 16) # Checksum as integer. Need to verify it.
                })
                
                # Extract what we can from the debug data.
                retVal.update(
                    self.parseDebug(
                        retVal.pop('dbgRaw'),
                        retVal.pop('dbgDat')
                    )
                )
                
                # Set valid flag.
                valid = True
        
        except (KeyboardInterrupt, SystemExit):
            raise
        
        except:
            raise
        
        finally:
            retVal.update({'valid': valid})
        
        return retVal