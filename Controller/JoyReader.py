#  joyReader.py  --  reading joystick information from /dev/input/js0
#     Copyright (C) 2021  David C.
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


import os
import io 
import struct
import time


JOY_PATH = '/dev/input/js0'
EVENT_STRUCT_MASK = "IhBB"
EVENT_SIZE = struct.calcsize(EVENT_STRUCT_MASK)

if EVENT_SIZE != 8:
    print("ERROR:  EVENT_SIZE NOT CALCULATED RIGHT IN joyReader")



analogIndices = {
    "leftHatX" : 0,
    "leftHatY" : 1,
    "rightHatX" : 2,
    "rightHatY" : 3,
    "rightTrigger" : 4,
    "leftTrigger" : 5,
    "dpadX" : 6,
    "dpadY" : 7
    }

buttonIndices = {
    "A" : 0,
    "B" : 1,
    "X" : 2,
    "Y" : 3,
    "L1" : 4,
    "R1" : 5,
    "back" : 6,
    "start" : 7,
    "xbox" : 8,
    "L3" : 9,
    "R3" : 10,
    "R2" : 11, ### R2 and L2 are backwards because that's how they are on the analog side
    "L2" : 12,  ###  on the analog side they match the numbers that come from the events. 
    "dpadLeft" : 13,
    "dpadRight" : 14,
    "dpadUp" : 15,
    "dpadDown" : 16
    
    }

class JoyReader:
    
    def testFunction(self):
        
        while(1):
            self.run()
            self.displayData()
            time.sleep(0.1)        
        return 
    
    def __init__(self):
        
#         self.leftHatX = 0
#         self.leftHatY = 0
#         self.rightHatX = 0
#         self.rightHatY = 0
#         self.dpadX = 0
#         self.dpadY = 0
#         self.rightTrigger = 0
#         self.leftTrigger = 0

        self.connectStatus = False 
        
        self.analogVals = [0,0,0,0,-32767,-32767,0,0]
        self.buttons = 0
        
        self.joyFile = io.open(JOY_PATH, "rb")
        os.set_blocking(self.joyFile.fileno(), False)
        
        self.run()
        
        return 
    
    def close(self):
        self.joyFile.close()
        return
    
    def run(self):
        
        ev = self.joyFile.read(8)
        while ev is not None:
            ####  WARNING   UNTESTED ERROR HANDLING  ####
            if len(ev) < 8:
                ev.append(self.joyFile.read(8-len(ev)))
            #######################
            self.connectStatus = True
            self.handleEvent(ev)
            ev = self.joyFile.read(8)
        
        return 
    
    def handleEvent(self, aByteArray):
        
        arrayLen = len(aByteArray)
        if(arrayLen != EVENT_SIZE):
            print("ERROR:  Array length not 8 in joyReader.handleEvent")
        
        (ms, data, type, number) = struct.unpack("IhBB", aByteArray)
        
        ###  analog Data
        if type == 2 and number < 8:
            self.analogVals[number] = data
            ###  Triggers can be buttons too
            if number == 4 or number == 5:
                if data <= 0:
                    self.buttons &= ~(1<<(number+7))
                else:
                    self.buttons |= (1<<(number+7))
            elif number == 6 or number == 7:
                if data < 0:
                    self.buttons |= (1<<((2*number)+1))
                elif data > 0:
                    self.buttons |= (2<<((2*number)+1))
                else:
                    self.buttons &= ~(3<<((2*number)+1))
                    
        
        elif type == 1 and number < 11:
            if data == 0:
                self.buttons &= ~(1<<number)
            else:
                self.buttons |= (1<<number)          
        
        return 
    
    def displayData(self):
        
        print ("LX: ", self.getAnalog('leftHatX'),
            "LY: ", self.getAnalog('leftHatY'),
            "RX: ", self.getAnalog('rightHatX'),
            "RY: ", self.getAnalog('rightHatY'),
            "RT: ", self.getAnalog('rightTrigger'),
            "LT: ", self.getAnalog('leftTrigger'),
            "DX: ", self.getAnalog('dpadX'),
            "DY: ", self.getAnalog('dpadY'),
            "BUT:", self.buttons)
        
        print ("A  :", self.getButton("A"),
               "B  :", self.getButton("B"),
               "X  :", self.getButton("X"),
               "Y  :", self.getButton("Y"),
               "L1  :", self.getButton("L1"),
               "R1  :", self.getButton("R1"),
               )
        
        return
    
    def connected(self):
        return self.connectStatus
    
    def getButton(self, aName):
        self.run()
        if(self.buttons & (1<<buttonIndices[aName])):
            return 1        
        return 0
    
    def getAnalog(self, aName):
        self.run()
        idx = analogIndices[aName]
        retval = self.analogVals[idx]
#         ### Triggers need special treatment for existing code compatibility
#         ### To be compatible with existing discobot code they need to return 0-255
#         ### Currently they return -32767 to 32767
#         if idx == 4 or idx == 5:
# #             retval = retval / 32767  ###  scale to -1.0 to 1.0 
# #             retval = retval / 2      ###  scale to -0.5 to 0.5
# #             retval = retval + 0.5    ###  move scale to 0.0 - 1.0
# #             retval = retval * 255    ###  scale to 0 - 255
#             retval = int(((retval / 65534) + 0.5) * 255)
                    
        return (retval)
    
    ####  Functions for compatibility with old DiscoBot code
    def axisScale(self, raw, deadzone):        
        if abs(raw) < deadzone:
            return 0.0
        else:
            if raw < 0:
                return (raw + deadzone) / (32768.0 - deadzone)
            else:
                return (raw - deadzone) / (32767.0 - deadzone)
    
    def A(self):
        return self.getButton('A')
    
    def B(self):
        return self.getButton('B')
    
    def X(self):
        return self.getButton('X')
    
    def Y(self):
        return self.getButton('Y')
    
    def leftBumper(self):
        return self.getButton('L1')
    
    def rightBumper(self):
        return self.getButton('R1')
    
    def Back(self):
        return self.getButton('back')
    
    def Start(self):
        return self.getButton('start')
    
    def Guide(self):
        return self.getButton('xbox')
    
    def leftThumbstick(self):
        return self.getButton('L3')
    
    def rightThumbstick(self):
        return self.getButton('R3')
    
    def dpadLeft(self):
        return self.getButton('dpadLeft')
    
    def dpadRight(self):
        return self.getButton('dpadRight')
    
    def dpadUp(self):
        return self.getButton('dpadUp')
    
    def dpadDown(self):
        return self.getButton('dpadDown')
    
    def leftTrigger(self):
        return ((self.getAnalog('leftTrigger')/ 65534.0) + 0.5)
    
    def rightTrigger(self):
        return ((self.getAnalog('rightTrigger')/ 65534.0) + 0.5)
    
    def leftX(self, deadzone=4000):
        return self.axisScale(self.getAnalog('leftHatX'), deadzone)
    
    def leftY(self, deadzone=4000):
        return -(self.axisScale(self.getAnalog('leftHatY'), deadzone))
    
    def rightX(self, deadzone=4000):
        return self.axisScale(self.getAnalog('rightHatX'), deadzone)
    
    def rightY(self, deadzone=4000):
        return -(self.axisScale(self.getAnalog('rightHatY'), deadzone))
    
    
    
    
    












#####