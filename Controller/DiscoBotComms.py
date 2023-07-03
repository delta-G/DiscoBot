#  DiscoBot  --  The Python control software for my robot
#     Copyright (C) 2016  David C.
# 
#     This program is free software: you can redistribute it and/or modify
#     it under the terms of the GNU General Public License as published by
#     the Free Software Foundation, either version 3 of the License, or
#     (at your option) any later version.
# 
#     This program is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#     GNU General Public License for more details.
# 
#     You should have received a copy of the GNU General Public License
#     along with this program.  If not, see <http://www.gnu.org/licenses/>.

import serial
import time
import SharedDiscoBot
import socket
from _socket import MSG_DONTWAIT, SHUT_RDWR

class DiscoBotComms:
    
    def __init__(self, aController, aParser):
        
        self.controller = aController
        
        self.serOut = None
        self.sockOut = None
        self.sockArgs = ('192.168.1.75' , 1234)
        
        self.wifiMode = False
        
        self.commsOn = False
        
        self.established = False
        
        self.outputBuffer = bytearray()
        self.inputBuffer = bytearray()
        self.receivingReturn = False
        
        self.returnParser = aParser
        
        return 
    
    def initComms(self, aPort):
        
        if not self.commsOn:
            try: 
                if(aPort == "---WiFi---"):
                    self.wifiMode = True;
                    self.sockOut = socket.socket(socket.AF_INET , socket.SOCK_STREAM)
                    self.sockOut.connect(self.sockArgs)
                    self.serOut = None
                    
                else:
                    self.wifiMode = False;                                       
                    self.serOut = serial.Serial(aPort, 115200)
                    self.sockOut = None
    
            except Exception as ex:
                self.commsOn=False
                self.controller.putstring("--ERROR@initComms--")
                self.controller.putstring(ex)  
                self.controller.putstring('\n') 
            else:
                self.commsOn = True
            
        return
    
    def connected(self):
        return self.commsOn
    
    def runComms(self):
        
        if self.commsOn:
            try:
                loopStartTime = time.time()
                if(self.wifiMode == True):
                    line_read = self.sockOut.recvfrom(251, MSG_DONTWAIT)[0]
                    for c in line_read:
                        self.handleCharacter(c)
                else:
                    while self.serOut.inWaiting() and time.time() - loopStartTime < 1:
                        c = self.serOut.read()          
#                     print("READ ->", c)
                        self.handleCharacter(ord(c))    
                        
            except Exception as e:
                err = e.args[0]
                if((self.wifiMode == True) and (err == 11)):    
                    pass
                else:                
                    print (e)
                    self.controller.logger.logByteArray("COMMS_ERROR", self.inputBuffer, 1)
                    self.controller.putstring("COMS-ERROR:")
                    self.controller.putstring(err)
                            
                                    
        return     
    
    def handleCharacter(self, aChar):
        if (len(self.inputBuffer) >= 2) and ((self.inputBuffer[1] >= 0x12) and (self.inputBuffer[1] <= 0x14)):
            
            self.receivingReturn = False
            self.inputBuffer.append(aChar)
            
            if len(self.inputBuffer) == self.inputBuffer[2]:
                if self.inputBuffer[-1] == ord('>'):
                    self.returnParser(self.inputBuffer)
                    self.inputBuffer = bytearray()
                else:
                    self.inputBuffer = bytearray()
                                        
        elif aChar == ord('<'):
            self.inputBuffer = bytearray()
            self.receivingReturn = True
            
        if self.receivingReturn == True:
            if aChar != None:                            
                if aChar<128:
                    self.inputBuffer.append(aChar)
                else:
                    ### Bail out on non-ascii characters in an ascii command
                    ### This indicates a comms error                                
                    self.receivingReturn = False
#                                 self.controller.logger.logString("COMMS_ERROR", 1)
                    self.controller.logger.logByteArray("COMMS_ERROR", self.inputBuffer, 1)
                    self.inputBuffer = bytearray()
                    
            if aChar == ord('>'):
                self.receivingReturn = False
                self.returnParser(self.inputBuffer)
                self.inputBuffer = bytearray()
        return
        

    
    def buffer(self, aMess):
        self.outputBuffer.extend(bytearray(aMess, encoding='ascii'))
        return
    
    def flush(self):
        if(self.wifiMode == True):
            self.sockOut.send(self.outputBuffer)
        else:        
            self.serOut.write(self.outputBuffer)
            self.serOut.flush()
        
        self.outputBuffer = bytearray()
        return 
    
    def send(self, aMess):            
        self.buffer(aMess)
        self.flush()
        return
    
    def write(self, aMess):    
        if(self.wifiMode == True):
            self.sockOut.send(aMess)
        else:
            self.serOut.write(aMess)
        return 
    
    def read(self):    
        retval = None
        if(self.wifiMode == True):
            retval = self.sockOut.recv(256)
        else:
            retval = self.serOut.read()
        return retval
    
    def close(self):    
        if self.commsOn:
            try:
                if(self.wifiMode == True):
                    if self.sockOut != None:
                        self.sockOut.shutdown(SHUT_RDWR)
                        self.sockOut.close()
                else:
                    if self.serOut != None:
                        self.serOut.flushInput()
                        self.serOut.flushOutput()
                        self.serOut.close()
                        
            except Exception as ex:
                self.controller.putstring("--ERROR@COMMS Close--")
                self.controller.putstring(ex)
                self.controller.putstring('\n')
            
            else:
                self.commsOn=False
        else:
            self.controller.putstring("Comms are not on.")
        return 
    
    
    def getIndicatorState(self):
        if self.commsOn:
            return SharedDiscoBot.colors['green']
        else:
            return SharedDiscoBot.colors['red']
            
    
    def isWiFiMode(self):
        return self.wifiMode
    