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
    
    def initComms(self):
        
        if not self.commsOn:
            try:                    
                self.serOut = serial.Serial('/dev/ttyUSB0', 115200)
    
            except Exception as ex:
                self.commsOn=False
                self.putstring(ex)  
                self.putstring('\n') 
            else:
                self.commsOn = True
            
        return
    
    
    def runComms(self):
        
        if self.commsOn:
            try:
                while self.serOut.inWaiting():
                    c = self.serOut.read()
                    if (len(self.inputBuffer) >= 2) and ((self.inputBuffer[1] >= 0x12) and (self.inputBuffer[1] <= 0x14)):
                        self.receivingReturn = False
                        self.inputBuffer.append(ord(c))
                        
                        if len(self.inputBuffer) == self.inputBuffer[2]:
                            if self.inputBuffer[-1] == '>':
                                self.returnParser(self.inputBuffer)
                                self.inputBuffer = bytearray()
                            else:
                                self.inputBuffer = bytearray()
                                                    
                    elif c == '<':
                        self.inputBuffer = bytearray()
                        self.receivingReturn = True
                    if self.receivingReturn == True:
                        if c != None:
                            self.inputBuffer.append(ord(c))
                        if c == '>':
                            self.receivingReturn = False
                            self.returnParser(self.inputBuffer)
                            self.inputBuffer = bytearray()
                            
            except Exception as e:
                err = e.args[0]
                self.controller.putstring(err)
                            
                                    
        return     

    
    def buffer(self, aMess):
        self.outputBuffer.extend(bytearray(aMess))
        return
    
    def flush(self):
        for b in self.outputBuffer:
            self.serOut.write(b)
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
    