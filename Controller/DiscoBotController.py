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

import xbox
import socket
import DiscoBotJoint
import time
import errno
from __builtin__ import False
from _socket import MSG_DONTWAIT
from _socket import SHUT_RDWR

import serial

useSerial = True
useWifi = not useSerial

class DiscoBotController:
    
    def putstring(self, aString):
        
        if self.printRedirect is not None:
            self.printRedirect(aString)
        if self.logFile is not None:
            self.logFile.write(str(aString))
        
        print aString,
        
        return
    
    def initComs(self):
        
        if not self.commsOn:
            try:
                                    
                if(useSerial):
                    
                    self.serOut = serial.Serial('/dev/ttyUSB0', 115200)
    
            except Exception as ex:
                self.commsOn=False
                self.putstring(ex)  
                self.putstring('\n') 
#                 self.sockOut = socket.socket(socket.AF_INET , socket.SOCK_STREAM)
    #             self.sockOut.setblocking(0)
            else:
                self.commsOn = True
            
        return
    
    def __init__(self, aRedirect = None, aLogFile = None):
        
        print """ 
        ***********************
*********   pyBot Interface   *******
 ***********************************
"""

        print """
        
*********************************************************************        
*********************************************************************        
******* pyBot  Copyright (C) 2016  David C.  ************************
**  This program comes with ABSOLUTELY NO WARRANTY; *****************
**  This is free software, and you are welcome to redistribute it  **
**  under certain conditions; ***************************************
*********************************************************************
*********************************************************************


    """
        
        self.socketConnected = False 
        
        self.printRedirect = aRedirect
        self.logFile = aLogFile
                
        self.putstring("Global Interface Initializing\n")   
        
        self.joy = None
        
### Serial Recv variables
        self.returnBuffer = ""
        self.receivingReturn = False
        self.lastRMBheartBeat = time.time()
        self.RMBheartBeatWarningTime = time.time()
        self.lastGimbalTime = time.time()
### Comms Variables
        self.lastXboxSendTime = 0
        self.responseReceived = False       
        self.turnAroundTime = 0.0 
        
        self.lastBotSNR = 0
        self.lastBotRSSI = 0
        
        self.lastBaseSNR = 0
        self.lastBaseRSSI = 0
### Robot Variables
        self.botStatusByte = 0
        self.armStatusByte = 0
        
        self.driveMode = ""
        self.cameraPower = False
        self.headlightPower = False
        self.armPower = False
        self.comPower = False
        self.armServoPower = False
        
        self.rmbHeartbeatWarningLevel = "green"
        self.rmbBatteryVoltage = 0.0
        self.leftMotorCount = 0
        self.rightMotorCount = 0
        self.leftMotorOut = 0
        self.rightMotorOut = 0
        self.leftMotorSpeed = 0
        self.rightMotorSpeed = 0
        self.currentRssi = 0
        self.currentSSID = 0
        
### Vars for GUI
        self.showCommands = False
        self.showReturns = False
        self.showDebug = False
        
        self.commsOn = False


        self.motorRight = 0
        self.motorLeft = 0
        self.throttleLevel = 0
        
        self.invertShoulder = True
        self.invertElbow = True
        self.invertWrist = False
        
        self.lastStart = 0
        self.lastY = 0
        self.lastA = 0
        self.lastB = 0
        self.lastX = 0
        self.lastGuide = 0
        self.lastThumbR = 0
        self.lastThumbL = 0
        self.controlMode = 0
        self.lastRMBhbRequest = 0
        self.lastRMBmotorRequest = 0

        self.BASE = 0
        self.SHOULDER = 1
        self.ELBOW = 2
        self.WRIST = 3
        self.ROTATE = 4
        self.GRIP = 5
        self.PAN = 7
        self.TILT = 6
        
        #########   DiscoBotJoint   ( name , length, offset, minMicros, minAngle, maxMicros, maxAngle)
        self.armJoints = [DiscoBotJoint.DiscoBotJoint("base", 37, 0, 544, -0.34907, 2400, 3.31631),
                          DiscoBotJoint.DiscoBotJoint("shoulder", 105, 0, 544, -0.087266, 2400, 2.91470),
                          DiscoBotJoint.DiscoBotJoint("elbow", 98, 0, 544, 2.96706, 2400, -0.13963),
                          DiscoBotJoint.DiscoBotJoint("wrist", 158, 32, 605, -1.16937, 2400, 2.12930),
                          DiscoBotJoint.DiscoBotJoint("rotate", 0, 0, 564, -0.34907, 2400, 3.316126),
                          DiscoBotJoint.DiscoBotJoint("grip", 0, 0, 1680, 1.923, 2400, 3.1415),
                          DiscoBotJoint.DiscoBotJoint("pan", 0, 0, 600, -1.57, 2350, 3.1415),
                          DiscoBotJoint.DiscoBotJoint("tilt", 0, 0, 600, 0.87, 1470, -0.35)]

        self.servoInfo = []
        for i in range(8):
            self.servoInfo.append([1500,100,1234])
        
        return
            
    
    def setRedirect(self, aRedirect):
        self.printRedirect = aRedirect
        return
     
    def connectJoystick(self):
        if self.joy == None:
            try:
                self.joy = xbox.Joystick()            
            except Exception as ex:
                self.joy = None
                self.putstring(ex)  
                self.putstring('\n')
                        
        return
    
     
    def connectToBot(self):
        if self.commsOn:
            self.putstring("Connecting to Robot\n")
            ###TODO:   WHAT GOES HERE????
            self.socketConnected = True
            self.putstring ("Connected to Robot\n")   
            if(useSerial):
                self.outPutRunner("<ESTART><ECONNECT><B,HB>")
        
        return    
    
    def killConnection(self):
        if(self.socketConnected):
            self.putstring ("Closing Connection\n")
            ###  TODO:  WHAT GOES HERE???            
        else :
            self.putstring ("The connection is not open\n")                
        return
    
    
    
    def sendToLog(self, cs):
        if self.logFile is not None:
            self.logFile.write(cs)
    
    
    def outPutRunner(self, cs):
        if self.socketConnected:
            if(useSerial):
                time.sleep(0.2)
                self.serOut.write(cs)
                self.serOut.flush()
                time.sleep(0.2)
        if self.showCommands:
#             if not str(cs).startswith("<X,0D14"):
            self.putstring("COM--> " + str(cs) + '\n')
        
        self.sendToLog("OUT--> " + str(cs) + "\n")
        
        return
    
#     def moveToByAngle(self, aTup):
#         i = 0
#         for servo in self.armServos:
#             servo.moveToImmediate(servo.angleToMicroseconds(aTup[i]))
#             self.armCommandSender(i)
#             i += 1
#          
#         return
    
    
    def runInterface(self):       
        if self.joy is not None:
            if(self.joy.connected()):
                if not self.joy.Start():
                    self.lastStart = False
            
                if(self.joy.Start() and not self.socketConnected):                
                    self.connectToBot()
        ### Back Button or lost connection ends program
                if(self.joy.Start() and self.socketConnected and not self.lastStart):
                    self.sendRawController()
                    self.lastStart = True
                if self.joy.Back():
                    return False                
    ### REQUEST HEARTBEAT        
#             if time.time() - self.lastRMBhbRequest >= 2:
#     #             self.outPutRunner("<R,HB>")
#                 self.lastRMBhbRequest = time.time()
#             if time.time() - self.lastRMBmotorRequest >= 0.5:
#     #             self.outPutRunner("<R,M>")
#                 self.lastRMBmotorRequest = time.time()
                
    ### CONTROLLER LOOP        
#             if ((time.time() - self.lastXboxSendTime >= 0.2) or (self.responseReceived)):
            if self.responseReceived:
   
                if self.socketConnected:    
                    self.sendRawController()
                    self.lastXboxSendTime = time.time()
                    self.responseReceived = False
        
#         self.listenForESP()
        self.listenForRawSerial()
            
        
        if (time.time() - self.lastRMBheartBeat >= 10) and (time.time() - self.RMBheartBeatWarningTime >= 10):
            self.putstring ("*****   MISSING RMB HEARTBEAT "),
            self.putstring (time.time() - self.lastRMBheartBeat),
            self.putstring ("  Seconds  ****\n")
            self.rmbHeartbeatWarningLevel = "red"
            self.RMBheartBeatWarningTime = time.time()        
            
        return True
    
    def make16bitSigned(self, aNum):
        if((aNum > 32767) and (aNum < 65535)):
            return (-65536 + aNum)
        else:
            return aNum
    
    def handleRawDataDump(self):
        
#         self.putstring("***  RAW_DATA  ***")
        self.sendToLog("DUMP--> ")
        
        while self.serOut.inWaiting() < 19:
            pass
        
        dumpMessage = bytearray()
        dumpMessage.append(ord('<'))
        dumpMessage.append(0x13)
        
        
        for i in range(19):
            dumpMessage.append(ord(self.serOut.read()))
        
#         numBytesToRead = dumpMessage[2]
        self.botStatusByte = dumpMessage[3]
        self.throttleLevel = dumpMessage[4]
        self.rmbBatteryVoltage = dumpMessage[5] / 10.0
        self.leftMotorCount = (dumpMessage[6] << 8) + dumpMessage[7]
        self.leftMotorCount = self.make16bitSigned(self.leftMotorCount)
        self.leftMotorSpeed = (dumpMessage[8] << 8) + dumpMessage[9]        
        self.leftMotorSpeed = self.make16bitSigned(self.leftMotorSpeed)
        self.leftMotorOut = dumpMessage[10]
        self.rightMotorCount = (dumpMessage[11] << 8) + dumpMessage[12]
        self.rightMotorCount = self.make16bitSigned(self.rightMotorCount)
        self.rightMotorSpeed = (dumpMessage[13] << 8) + dumpMessage[14]        
        self.rightMotorSpeed = self.make16bitSigned(self.rightMotorSpeed)
        self.rightMotorOut = dumpMessage[15]
        self.lastBotSNR = dumpMessage[16]
        self.lastBotRSSI = -dumpMessage[17]
        self.lastBaseSNR = dumpMessage[18]
        self.lastBaseRSSI = -dumpMessage[19]
        
        self.readStatusByte()
        
        for val in dumpMessage:
            self.sendToLog(hex(val))
            self.sendToLog(' ')
            
        self.sendToLog('\n')
        
        return 
    
    def readStatusByte(self):
        mb = self.botStatusByte & 3
        if mb == 1:
            self.driveMode = "DRIVE"
        elif mb == 2:
            self.driveMode = "ARM"
        elif mb == 3:
            self.driveMode = "MINE"            
        
        if(self.botStatusByte & 0x10):
            self.cameraPower = True
        else:
            self.cameraPower = False
            
        if(self.botStatusByte & 0x20):
            self.headlightPower = True
        else:
            self.headlightPower = False
            
        if(self.botStatusByte & 0x40):
            self.armPower = True
        else:
            self.armPower = False
            
        if(self.botStatusByte & 0x80):
            self.comPower = True
        else:
            self.comPower = False
            
        return
    
    
    def handleArmDump(self):
        
#         self.putstring("*** ARM_DUMP ***")
        self.sendToLog("ARM--> "  + "\n")
        
        while self.serOut.inWaiting() < 20:
            pass
        
        dumpMessage = bytearray()
        dumpMessage.append(ord('<'))
        dumpMessage.append(0x12)        
        
        for i in range(20):
            dumpMessage.append(ord(self.serOut.read()))
        
        
        numBytesToRead = dumpMessage[2]
        self.armStatusByte = dumpMessage[3]
        whichSet = dumpMessage[4]
        
        dataPoints = []
        
        for i in range(8):
            dp = ((dumpMessage[5+(2*i)] & 0xFF) << 8)
            dp |= dumpMessage[6+(2*i)] & 0xFF
            dataPoints.append(dp)
        
        if whichSet == 'p':
            for i in range(8):
                self.servoInfo[i][0] = dataPoints[i]
        elif whichSet == 's':
            for i in range(8):
                self.servoInfo[i][1] = dataPoints[i]
        elif whichSet == 't':
            for i in range(8):
                self.servoInfo[i][2] = dataPoints[i]   
                
        if(self.armStatusByte & 1):
            self.armServoPower = True
        else:
            self.armServoPower = False
                    
        return 
    
    
    def listenForRawSerial(self):
        
        if self.socketConnected:
            try:
                if(useSerial):
                    while self.serOut.inWaiting():
                        c = self.serOut.read()
                        ###  If we are at the first character and it 
                        ###  is the control code
                        if (self.returnBuffer == "<"):
                            if ord(c) == 0x13:
                                self.handleRawDataDump()
                                self.returnBuffer = ""
                                self.receivingReturn = False
                                self.responseReceived = True
                                self.turnAroundTime = time.time() - self.lastXboxSendTime
                            elif ord(c) == 0x12:
                                self.handleArmDump()
                                self.returnBuffer = ""
                                self.receivingReturn = False    
                                self.responseReceived = True   
                                self.turnAroundTime = time.time() - self.lastXboxSendTime                         
                                                  
                        if c == '<':
                            self.returnBuffer = ""
                            self.receivingReturn = True                            
                        if self.receivingReturn == True:
                            if c != None:
                                self.returnBuffer += str(c)                            
                            if c == '>':
                                self.parseReturnString()
                                self.receivingReturn = False    
                                if self.showReturns:
                                    self.putstring("RET--> " + self.returnBuffer + '\n')
                                self.sendToLog("RET--> " + self.returnBuffer + "\n")
                                    
                        
            except socket.error, e:
                err = e.args[0]
                if err == errno.EAGAIN or err == errno.EWOULDBLOCK:
#                     self.putstring("EAGAIN or EWOULDBLOCK")
                    pass
                else:
                    # a REAL error occurred
                    self.putstring("Bad Error in linstenForRawSerial")
                    self.putstring (err)
                    self.putstring ('\n')        
        
        return 
    
    def listenForESP(self):        
        
        if self.socketConnected:
            try:
                if(useSerial):
                    line_read = self.serOut.read(self.serOut.in_waiting)
        
            except socket.error, e:
                err = e.args[0]
                if err == errno.EAGAIN or err == errno.EWOULDBLOCK:
#                     self.putstring("EAGAIN or EWOULDBLOCK")
                    pass
                else:
                    # a REAL error occurred
                    self.putstring("Bad Error in linstenForESP")
                    self.putstring (err)
                    self.putstring ('\n')
            else:
                for c in line_read:                        
                    if c == '<':
                        self.returnBuffer = ""
                        self.receivingReturn = True                            
                    if self.receivingReturn == True:
                        if c != None:
                            self.returnBuffer += str(c)                            
                        if c == '>':
                            self.parseReturnString()
                            self.receivingReturn = False    
                            if self.showReturns:
                                self.putstring("RET--> " + self.returnBuffer + '\n')                   
        return
    
    
    def parseReturnString(self):
        if self.returnBuffer == "<RMB HBoR>":
            self.lastRMBheartBeat = time.time()
            self.rmbHeartbeatWarningLevel = "green"
#             self.putstring ("Good Heart --> ") 
#             self.putstring ( self.returnBuffer)
#             self.putstring('\n')
        elif self.returnBuffer.startswith("<BAT,"):
            tndx = self.returnBuffer.rfind(',')
            self.rmbBatteryVoltage = self.returnBuffer[tndx+1:-1]
        
        elif self.returnBuffer.startswith("<Cnts,"):
            tup = tuple(self.returnBuffer.split(','))
            self.leftMotorCount = tup[1]
            self.rightMotorCount = tup[2]
        
        elif self.returnBuffer.startswith("<Out,"):
            tup = tuple(self.returnBuffer.split(','))
            self.leftMotorOut = tup[1]
            self.rightMotorOut = tup[2]
        elif self.returnBuffer.startswith("<Spd,"):
            tup = tuple(self.returnBuffer.split(','))
            self.leftMotorSpeed = tup[1]
            self.rightMotorSpeed = tup[2]
        
        elif self.returnBuffer.startswith(("<p,")):
            tup = tuple(self.returnBuffer.split(','))
            for t in tup:
                self.servoInfo[t[0]][0] = t[1]
        elif self.returnBuffer.startswith(("<t,")):
            tup = tuple(self.returnBuffer.split(','))
            for t in tup:
                self.servoInfo[t[0]][1] = t[1]
        elif self.returnBuffer.startswith(("<s,")):
            tup = tuple(self.returnBuffer.split(','))
            for t in tup:
                self.servoInfo[t[0]][2] = t[1]
                    
        elif self.returnBuffer.startswith("<E-HB"):
            self.currentRssi = self.returnBuffer[5:self.returnBuffer.rfind('>')]
        elif self.returnBuffer.startswith("<E  NewClient @"):
            self.currentSSID = self.returnBuffer[16 : self.returnBuffer.rfind(',')]
            self.currentRssi = self.returnBuffer[self.returnBuffer.rfind(',') : self.returnBuffer.rfind('>')]
        elif self.returnBuffer.startswith("<##"):
            if self.showDebug:
                self.putstring(self.returnBuffer)
            pass
        else:
            self.putstring ("returnBuffer --> ") 
            self.putstring( self.returnBuffer)  
            for c in self.returnBuffer:
                if ord(c) < 33:
                    self.putstring(ord(c))
                    self.putstring(',')
            self.putstring('\n')      
        return        
    
    
    def requestFromESP(self, reqStr):
        
        commandString = ""
        commandString += "<"
        commandString += "R,"
        commandString += reqStr
        commandString += ">"
        self.outPutRunner(commandString)        
        return    
    
    def commandMode(self):
        
        while (self.joy.Guide()):
            
#             leftX = self.joy.leftY()
            leftY = self.joy.leftY()
#             rightX = self.joy.rightY()            
#             rightY = self.joy.rightY()

            if(self.joy.X()):
                self.outPutRunner("<V1>")
                return
            if(self.joy.A()):
                self.outPutRunner("<V0>")
                return
            if(self.joy.leftBumper()):
                self.outPutRunner("<H1>")
                return
            if(self.joy.rightBumper()):
                self.outPutRunner("<H0>")
                return
                
            
            if (leftY < -0):
                self.sittingHome()
                return
            if (leftY > 0):
                self.standingHome()
                return
        
        return

      
    
    
    def sendRawController(self):
        
        ###  Need to send as 14 integers.  
#             uint16_t checkBytes;
#             uint16_t buttonState;
#             uint8_t leftTrigger;
#             uint8_t rightTrigger;
#             int16_t hatValues[4];


        
#         enum ButtonMaskEnum {
#         UP = 0x0100,
#         RIGHT = 0x0800,
#         DOWN = 0x0200,
#         LEFT = 0x0400,
#         BACK = 0x2000,
#         START = 0x1000,
#         L3 = 0x4000,
#         R3 = 0x8000,
#         L2 = 0,
#         R2 = 0,
#         L1 = 0x0001,
#         R1 = 0x0002,
# 
#         B = 0x0020,
#         A = 0x0010,
#         X = 0x0040,
#         Y = 0x0080,
# 
#         XBOX = 0x0004,
#         SYNC = 0x0008,
# };
        ### That's for ButtonState
        buttonStateInt = 0
        if(self.joy.dpadUp()):
            buttonStateInt |= 0x0100
        if(self.joy.dpadRight()):
            buttonStateInt |= 0x0800
        if(self.joy.dpadDown()):
            buttonStateInt |= 0x0200
        if(self.joy.dpadLeft()):
            buttonStateInt |= 0x0400
        
        if(self.joy.Back()):
            buttonStateInt |= 0x2000
        if(self.joy.Start()):
            buttonStateInt |= 0x1000
        if(self.joy.leftThumbstick()):
            buttonStateInt |= 0x4000
        if(self.joy.rightThumbstick()):
            buttonStateInt |= 0x8000
            
        if(self.joy.leftBumper()):
            buttonStateInt |= 0x0001
        if(self.joy.rightBumper()):
            buttonStateInt |= 0x0002
            
        if(self.joy.B()):
            buttonStateInt |= 0x0020
        if(self.joy.A()):
            buttonStateInt |= 0x0010
        if(self.joy.X()):
            buttonStateInt |= 0x0040
        if(self.joy.Y()):
            buttonStateInt |= 0x0080
        
            
        if(self.joy.Guide()):
            buttonStateInt |= 0x0004
            
        leftTrigByte = self.joy.leftTrigger() * 255
        rightTrigByte = self.joy.rightTrigger() * 255
        
        ###  Hat Values
#         enum HatEnum {
#         LeftHatX = 0,
#         LeftHatY = 1,
#         RightHatX = 2,
#         RightHatY = 3,
# };

        leftHatX = self.joy.leftX(1000) * 32767
        leftHatY = self.joy.leftY(1000) * 32767
        rightHatX = self.joy.rightX(1000) * 32767
        rightHatY = self.joy.rightY(1000) * 32767
        
                ###  Need to send as 14 integers.  
#             uint16_t checkBytes;
#             uint16_t buttonState;
#             uint8_t leftTrigger;
#             uint8_t rightTrigger;
#             int16_t hatValues[4];
        
        rawMessage = bytearray()
        rawMessage.append(0x3C)                                         ##0
        rawMessage.append(0x14)                                         ##1
        rawMessage.append(16)                                           ##2
        rawMessage.append(((int)(buttonStateInt) >> 8) & 0xFF)          ##3
        rawMessage.append(((int)(buttonStateInt)) & 0xFF)               ##4
        rawMessage.append(((int)(leftTrigByte)) & 0xFF)                 ##5
        rawMessage.append(((int)(rightTrigByte)) & 0xFF)                ##6
        rawMessage.append(((int)(leftHatX) >> 8) & 0xFF)                ##7
        rawMessage.append(((int)(leftHatX)) & 0xFF)                     ##8
        rawMessage.append(((int)(leftHatY) >> 8) & 0xFF)                ##9
        rawMessage.append(((int)(leftHatY)) & 0xFF)                     ##10
        rawMessage.append(((int)(rightHatX) >> 8) & 0xFF)               ##11
        rawMessage.append(((int)(rightHatX)) & 0xFF)                    ##12
        rawMessage.append(((int)(rightHatY) >> 8) & 0xFF)               ##13
        rawMessage.append(((int)(rightHatY)) & 0xFF)                    ##14
        rawMessage.append(0x3E)                                         ##15
        
        self.serOut.write(rawMessage)
        self.logFile.write("RAW -->")
        for val in rawMessage:
            self.logFile.write(hex(val))
            self.logFile.write(" ")
        self.logFile.write("\n")
        
        return
