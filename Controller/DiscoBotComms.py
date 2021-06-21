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

class DiscoBotComms:
    
    def __init__(self, aController, aParser):
        
        self.controller = aController
        
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
                self.serOut = serial.Serial(aPort, 115200)
    
            except Exception as ex:
                self.commsOn=False
                self.controller.putstring(ex)  
                self.controller.putstring('\n') 
            else:
                self.commsOn = True
            
        return
    
    
    def runComms(self):
        
        if self.commsOn:
            try:
                loopStartTime = time.time()
                while self.serOut.inWaiting() and time.time() - loopStartTime < 1:
                    c = self.serOut.read()          
#                     print("READ ->", c)
                    if (len(self.inputBuffer) >= 2) and ((self.inputBuffer[1] >= 0x12) and (self.inputBuffer[1] <= 0x14)):
                        
                        self.receivingReturn = False
                        self.inputBuffer.append(ord(c))
                        
                        if len(self.inputBuffer) == self.inputBuffer[2]:
                            if self.inputBuffer[-1] == ord('>'):
                                self.returnParser(self.inputBuffer)
                                self.inputBuffer = bytearray()
                            else:
                                self.inputBuffer = bytearray()
                                                    
                    elif c == b'<':
#                         print("START OF PACKET")
                        self.inputBuffer = bytearray()
                        self.receivingReturn = True
                    if self.receivingReturn == True:
#                         print("READ ->", c)
                        if c != None:                            
                            if ord(c)<127:
                                self.inputBuffer.append(ord(c))
                            else:
                                ### Bail out on non-ascii characters in an ascii command
                                ### This indicates a comms error
                                self.inputBuffer = bytearray()
                                self.receivingReturn = False
                                self.controller.logger.logString("COMMS_ERROR", 1)
                                
                        if c == b'>':
                            self.receivingReturn = False
                            self.returnParser(self.inputBuffer)
                            self.inputBuffer = bytearray()
                            
            except Exception as e:
                err = e.args[0]
                print (e)
                self.controller.putstring("COMS-ERROR:")
                self.controller.putstring(err)
                            
                                    
        return     

    
    def buffer(self, aMess):
        self.outputBuffer.extend(bytearray(aMess, encoding='ascii'))
        return
    
    def flush(self):
        self.serOut.write(self.outputBuffer)
        self.outputBuffer = bytearray()
        self.serOut.flush()
        return 
    
    def send(self, aMess):        
        self.buffer(aMess)
        self.flush()
        return
    
    def write(self, aMess):
        self.serOut.write(aMess)
        return 
    
    def read(self):
        return self.serOut.read()
    
    def close(self):
        self.serOut.flushInput()
        self.serOut.flushOutput()
        self.serOut.close()
        self.commsOn=False
        return 
    
    
    def getIndicatorState(self):
        if self.commsOn:
            return SharedDiscoBot.colors['green']
        else:
            return SharedDiscoBot.colors['red']
            
    