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
import DiscoBotJoint
import time
import struct

import DiscoBotComms
import SharedDiscoBot




class DiscoBotController:
    
    def putstring(self, aString):
        
        if self.printRedirect is not None:
            self.printRedirect(aString)
        if self.logFile is not None:
            self.logFile.write(str(aString))
        
        print aString,
        
        return
    
    
    def initComs(self, aPort):
        
        self.comms.initComms(aPort)
            
        return
    
    
    
    def __init__(self, aRedirect = None, aLogFile = None):
        
        print """ 
        ***********************
*****   DiscoBotBot Interface   *******
 ***********************************
"""

        print """
        
*********************************************************************        
*********************************************************************        
******* DiscoBot  Copyright (C) 2016  David C.  *********************
**  This program comes with ABSOLUTELY NO WARRANTY; *****************
**  This is free software, and you are welcome to redistribute it  **
**  under certain conditions; ***************************************
*********************************************************************
*********************************************************************


    """
    
#         self.speedLog = open("robotSpeedLog.csv", "w")
        
        self.socketConnected = False 
        self.endProgram = False
        
        self.comms = DiscoBotComms.DiscoBotComms(self, self.returnParser)
        
        self.printRedirect = aRedirect
        self.logFile = aLogFile
                
        self.putstring("Global Interface Initializing\n")   
        
        self.joy = None
        
        self.sendingController = False
        
### Serial Recv variables
        self.lastRMBheartBeat = time.time()
        self.RMBheartBeatWarningTime = time.time()
### Comms Variables
        self.lastXboxSendTime = 0
        self.responseReceived = False  
        self.lastResponseTime = 0     
        self.turnAroundTime = 0.0 
        
        self.comTimeOut = 0.35
        
        self.lastBotSNR = 0
        self.lastBotRSSI = 0
        
        self.lastBaseSNR = 0
        self.lastBaseRSSI = 0
### Robot Variables
        self.botStatusByte1 = 0
        self.botStatusByte2 = 0
        self.armStatusByte = 0
        
        self.driveMode = ""
        self.cameraPower = False
        self.headlightPower = False
        self.armPower = False
        self.comPower = False
        self.armServoPower = False
        
        self.motorPower = False
        self.motorContEnable = False
        self.v12Power = False
        self.auxPower = False
        self.sonarPower = False
        
        
        self.rmbHeartbeatWarningLevel = SharedDiscoBot.colors['green']
        self.rmbBatteryVoltage = 0.0
        self.batteryVoltage = 0.0
        self.motorVoltage = 1.2
        self.mainVoltage = 2.3
        self.comVoltage = 3.4
        self.auxVoltage = 4.5
        self.v12Voltage = 5.6
        
        
        self.leftMotorCount = 0
        self.rightMotorCount = 0
        self.leftMotorOut = 0
        self.rightMotorOut = 0
        self.leftMotorSpeed = 0
        self.rightMotorSpeed = 0
        
        self.sonarDistance = 0
        
        self.sonarList = [100,200,300,400,1050,1050,700,800,900,1000,1100,1200,1300]
        
### Vars for GUI
        self.showCommands = False
        self.showReturns = False
        self.showDebug = False
        
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
        self.armJoints = [DiscoBotJoint.DiscoBotJoint("base", 37, 0, 600, -0.0, 2400, 3.31631),
                          DiscoBotJoint.DiscoBotJoint("shoulder", 105, 0, 544, -0.087266, 2400, 2.91470),
                          DiscoBotJoint.DiscoBotJoint("elbow", 98, 0, 544, 2.96706, 2400, -0.13963),
                          DiscoBotJoint.DiscoBotJoint("wrist", 158, 32, 605, -1.16937, 2400, 2.12930),
                          DiscoBotJoint.DiscoBotJoint("rotate", 0, 0, 564, -0.34907, 2400, 3.316126),
                          DiscoBotJoint.DiscoBotJoint("grip", 0, 0, 1680, 1.923, 2400, 3.1415),
                          DiscoBotJoint.DiscoBotJoint("pan", 0, 0, 600, 3.1415, 2350, 0),
                          DiscoBotJoint.DiscoBotJoint("tilt", 0, 80, 600, 0.8727, 1470, -0.5236)]

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
        if self.comms.commsOn:
            self.putstring("Connecting to Robot\n")
            self.socketConnected = True
            self.outPutRunner("<ESTART><ECONNECT><B,HB>")
            self.putstring ("Connected to Robot\n") 
        
        return    
    
    def killConnection(self):
        if(self.socketConnected):
            self.putstring ("Closing Connection\n")
            self.comms.close() 
            self.socketConnected = False           
        else :
            self.putstring ("The connection is not open\n")   
            self.comms.close()             
        return
    
    
    def setLoRaMode(self, aMode):
        
        ### flush the radio
        self.outPutRunner("<FFE>")        
        ### give some time for transmission        
        time.sleep(2.5)
        ### send control code for new mode
        self.outPutRunner("<lM" + aMode + ">")
        ### flush radio 
        self.outPutRunner("<FFE>")
        ### give some time for other radio to adjust        
        time.sleep(2.5)
        ### return to normal operation   
        if(aMode > 1):
            self.comTimeOut = 10
        else:
            self.comTimeOut = 0.35   
        return
    
    
    def sendToLog(self, cs, level = 0):
        if self.logFile is not None:
            self.logFile.write(str(time.time()))
            self.logFile.write(" :")
            self.logFile.write(str(level))
            self.logFile.write(": ")
            self.logFile.write(str(cs))
    
    
    def outPutRunner(self, cs):
        if self.socketConnected:
            self.comms.send(cs)                  
            self.sendToLog("OUT--> " + str(cs) + "\n")  
        if self.showCommands:
            self.putstring("COM--> " + str(cs) + '\n')       
        return
    
    def stopSendingController(self):
        self.sendingController = False
        return 
    
    def startSendingController(self):
        self.sendingController = True
        return
    
    #*****************************************#
    ###########################################
    ###########  runInterface  ################
    ###########################################
    #*****************************************#
    
    def runInterface(self):
                   
        if self.joy is not None:
            if(self.joy.connected()):
                if(self.joy.Guide()):
                    self.guideMode()    
                    
                if self.endProgram:
                    return False            
              
    ### CONTROLLER LOOP        
                if ((time.time() - self.lastXboxSendTime >= self.comTimeOut) or (self.responseReceived)):
       
                    if self.socketConnected:
                        if self.sendingController:    
                            self.sendRawController()
                            self.lastXboxSendTime = time.time()
                            self.responseReceived = False
#                         else:
#                             self.outPutRunner("<R,R><FFE>")
        
    ### COMMS WITH ROBOT
        if self.socketConnected:
            self.comms.runComms()
            
        
        if (time.time() - self.lastRMBheartBeat >= 10) and (time.time() - self.RMBheartBeatWarningTime >= 10):
            self.putstring ("*****   MISSING RMB HEARTBEAT "),
            self.putstring (time.time() - self.lastRMBheartBeat),
            self.putstring ("  Seconds  ****\n")
            self.rmbHeartbeatWarningLevel = SharedDiscoBot.colors['red']
            self.RMBheartBeatWarningTime = time.time()
        elif (time.time() - self.lastRMBheartBeat >= 2):
            self.rmbHeartbeatWarningLevel = SharedDiscoBot.colors['yellow']
        else:
            self.rmbHeartbeatWarningLevel = SharedDiscoBot.colors['green']
            
                    
            
        return True
    
    
    def guideMode(self):
        if not self.joy.Start():
            self.lastStart = False
            
        if(self.joy.Start() and not self.socketConnected):    
#             self.putstring("Connecting to socket")    
            self.putstring("<Connecting to socket>")                        
            self.connectToBot()
            self.startSendingController()
        
        if(self.joy.Start() and self.socketConnected and not self.lastStart):
            self.startSendingController()
            self.sendRawController()
            self.lastXboxSendTime = time.time()
            self.responseReceived = False
            self.lastStart = True
                    
        ### Back Button or lost connection ends program
        if self.joy.Back():
            self.killConnection()
            self.endProgram = True       
        
        return
    
    
    
    
    
    
    ###########   Parsers and Functional Code:  
    
    ###########   Should probably move to a new class to clean up
    
    
    
    def make16bitSigned(self, aNum):
        if((aNum > 32767) and (aNum <= 65535)):
            return (-65536 + aNum)
        else:
            return aNum
    
    def handleRawDataDump(self, aByteArray):
        
        self.sendToLog("DUMP--> ")
        
        dumpMessage = aByteArray
        
        self.botStatusByte1 = dumpMessage[3]
        self.botStatusByte2 = dumpMessage[4]
        self.throttleLevel = dumpMessage[5]
        self.rmbBatteryVoltage = dumpMessage[6] / 10.0
        self.leftMotorCount = (dumpMessage[7] << 8) + dumpMessage[8]
        self.leftMotorCount = self.make16bitSigned(self.leftMotorCount)
        self.leftMotorSpeed = (dumpMessage[9] << 8) + dumpMessage[10]        
        self.leftMotorSpeed = self.make16bitSigned(self.leftMotorSpeed)
        self.leftMotorOut = dumpMessage[11]
        self.rightMotorCount = (dumpMessage[12] << 8) + dumpMessage[13]
        self.rightMotorCount = self.make16bitSigned(self.rightMotorCount)
        self.rightMotorSpeed = (dumpMessage[14] << 8) + dumpMessage[15]        
        self.rightMotorSpeed = self.make16bitSigned(self.rightMotorSpeed)
        self.rightMotorOut = dumpMessage[16]
        self.lastBotSNR = dumpMessage[17]
        self.lastBotRSSI = -dumpMessage[18]
        self.lastBaseSNR = dumpMessage[19]
        self.lastBaseRSSI = -dumpMessage[20]
        
        self.readStatusByte()
        
#         for val in dumpMessage:
#             self.sendToLog(hex(val))
#             self.sendToLog(' ')
#             
#         self.sendToLog('\n')
        
        return 
    
    def readStatusByte(self):
        mb = self.botStatusByte1 & 3
        if mb == 1:
            self.driveMode = "DRIVE"
        elif mb == 2:
            self.driveMode = "ARM"
        elif mb == 3:
            self.driveMode = "MINE"  
        elif mb == 0:
            self.driveMode = "AUTO"          
        
        if(self.botStatusByte1 & 0x10):
            self.cameraPower = True
        else:
            self.cameraPower = False
            
        if(self.botStatusByte1 & 0x20):
            self.headlightPower = True
        else:
            self.headlightPower = False
            
        if(self.botStatusByte1 & 0x40):
            self.armPower = True
        else:
            self.armPower = False
            
        if(self.botStatusByte1 & 0x80):
            self.comPower = True
        else:
            self.comPower = False
            
        if(self.botStatusByte2 & 0x01):
            self.motorPower = True
        else:
            self.motorPower = False
            
        if(self.botStatusByte2 & 0x02):
            self.motorContEnable = True
        else:
            self.motorContEnable = False
            
        if(self.botStatusByte2 & 0x04):
            self.v12Power = True
        else:
            self.v12Power = False
            
        if(self.botStatusByte2 & 0x08):
            self.auxPower = True
        else:
            self.auxPower = False
            
        if(self.botStatusByte2 & 0x10):
            self.sonarPower = True
        else:
            self.sonarPower = False
        
        
            
        return
    
    
    def handleArmDump(self, aByteArray):
        
        self.sendToLog("ARM--> "  + "\n")
       
        dumpMessage = aByteArray
        
        if self.logFile is not None:
            for val in dumpMessage:
                self.logFile.write(hex(val))
                self.logFile.write(" ")
            self.logFile.write("\n")
        
        self.armStatusByte = dumpMessage[3]
        whichSet = dumpMessage[4]
        
        dataPoints = []
        
        for i in range(8):
            dp = ((dumpMessage[5+(2*i)] & 0xFF) << 8)
            dp |= dumpMessage[6+(2*i)] & 0xFF
            dataPoints.append(dp)
        
        if whichSet == ord('p'):
            self.sendToLog("pos--> "  + "\n")
            for i in range(8):
                self.servoInfo[i][0] = dataPoints[i]
        elif whichSet == ord('s'):
            self.sendToLog("spd--> "  + "\n")
            for i in range(8):
                self.servoInfo[i][1] = dataPoints[i]
        elif whichSet == ord('t'):
            self.sendToLog("targ--> "  + "\n")
            for i in range(8):
                self.servoInfo[i][2] = dataPoints[i]   
                
        if(self.armStatusByte & 1):
            self.armServoPower = True
        else:
            self.armServoPower = False
                    
        return 
    
    
    def handleArmCalDump(self, aByteArray):
        
        for i in range(6):
            inTuple = struct.unpack_from('ffHH', aByteArray[((12*i)+3):((12*i)+15)])
            self.armJoints[i].minAngle = inTuple[0]
            self.armJoints[i].maxAngle = inTuple[1]
            self.armJoints[i].minMicros = inTuple[2]
            self.armJoints[i].maxMicros = inTuple[3]
        
        
        return 
    
    
    def handleSonarDump(self, aByteArray):        
        if(aByteArray[2] == 10):
            self.sonarDistance = (aByteArray[3] << 8) + aByteArray[4]        
            self.sonarDistance = self.make16bitSigned(self.sonarDistance)
        elif(aByteArray[2] == 30):
            for i in range(13):
                temp = (aByteArray[(2*i)+3] << 8) + aByteArray[(2*i)+4]
                temp = self.make16bitSigned(temp)
#                 self.putstring(str(i) + " : " + str(temp) + "\n")
                self.sonarList[i]=temp
        return
    
    def handleVoltageDump(self, aByteArray):
        
        temp = (aByteArray[3] << 8) | aByteArray[4]
        self.batteryVoltage = temp/1000.0
        
        temp = (aByteArray[5] << 8) | aByteArray[6]
        self.motorVoltage = temp/1000.0
        
        temp = (aByteArray[7] << 8) | aByteArray[8]
        self.mainVoltage = temp/1000.0
        
        temp = (aByteArray[9] << 8) | aByteArray[10]
        self.comVoltage = temp/1000.0
        
        temp = (aByteArray[11] << 8) | aByteArray[12]
        self.auxVoltage = temp/1000.0
        
        temp = (aByteArray[13] << 8) | aByteArray[14]
        self.v12Voltage = temp/1000.0
        
        return 
    
    
    def parseReturnString(self, aBuffer):
        
        if aBuffer == "<RMB HBoR>":
            self.lastRMBheartBeat = time.time()
            
        elif aBuffer.startswith("<SR,"):
            self.speedLog.write(aBuffer)
            self.speedLog.write('\n')
            print (aBuffer)
#         elif aBuffer.startswith("<BAT,"):
#             tndx = aBuffer.rfind(',')
#             self.rmbBatteryVoltage = aBuffer[tndx+1:-1]
#         
#         elif aBuffer.startswith("<Cnts,"):
#             tup = tuple(aBuffer.split(','))
#             self.leftMotorCount = tup[1]
#             self.rightMotorCount = tup[2]
#         
#         elif aBuffer.startswith("<Out,"):
#             tup = tuple(aBuffer.split(','))
#             self.leftMotorOut = tup[1]
#             self.rightMotorOut = tup[2]
#         elif aBuffer.startswith("<Spd,"):
#             tup = tuple(aBuffer.split(','))
#             self.leftMotorSpeed = tup[1]
#             self.rightMotorSpeed = tup[2]
#         
#         elif aBuffer.startswith(("<p,")):
#             tup = tuple(aBuffer.split(','))
#             for t in tup:
#                 self.servoInfo[t[0]][0] = t[1]
#         elif aBuffer.startswith(("<t,")):
#             tup = tuple(aBuffer.split(','))
#             for t in tup:
#                 self.servoInfo[t[0]][1] = t[1]
#         elif aBuffer.startswith(("<s,")):
#             tup = tuple(aBuffer.split(','))
#             for t in tup:
#                 self.servoInfo[t[0]][2] = t[1]
                    
        elif aBuffer.startswith("<E-HB"):
            self.currentRssi = aBuffer[5:aBuffer.rfind('>')]
        elif aBuffer.startswith("<E  NewClient @"):
            self.currentSSID = aBuffer[16 : aBuffer.rfind(',')]
            self.currentRssi = aBuffer[aBuffer.rfind(',') : aBuffer.rfind('>')]
        elif aBuffer.startswith("<##"):
            if self.showDebug:
                self.putstring(aBuffer)
            pass
        else:
            self.putstring ("returnBuffer --> ") 
            self.putstring( aBuffer)  
            for c in aBuffer:
                if ord(c) < 33:
                    self.putstring(ord(c))
                    self.putstring(',')
            self.putstring('\n')      
        return              
    
    def setResponseRecieved(self):
        self.responseReceived = True
        self.lastResponseTime = time.time()
        self.turnAroundTime = time.time() - self.lastXboxSendTime
        return 
    
    
    def returnParser(self, aByteArray):
        if len(aByteArray) >= 3:
            if (aByteArray[0] == ord('<')):
                if(aByteArray[1] >= 0x12) and (aByteArray[1] <= 0x14):
                    if (len(aByteArray) >= aByteArray[2]) and (aByteArray[aByteArray[2]-1] == ord('>')):                        
                        if (aByteArray[1] == 0x13) and (aByteArray[2] == 22):
                            self.handleRawDataDump(aByteArray)
                            self.setResponseRecieved()
                        elif (aByteArray[1] == 0x13) and (aByteArray[2] == 16):
                            self.handleVoltageDump(aByteArray)
                        elif (aByteArray[1] == 0x13) and ((aByteArray[2] == 10) or (aByteArray[2] == 30)):
                            self.handleSonarDump(aByteArray)
                            self.setResponseRecieved()
                        elif aByteArray[1] == 0x12:
                            if aByteArray[2] == 22:
                                self.handleArmDump(aByteArray)
                                self.setResponseRecieved()
                            elif aByteArray[2] == 76:
                                self.handleArmCalDump(aByteArray) 
                else:
                    self.parseReturnString(aByteArray.decode("ascii"))
                        
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
        
        self.comms.write(rawMessage)
        if self.logFile is not None:
            self.logFile.write("RAW -->")
            for val in rawMessage:
                self.logFile.write(hex(val))
                self.logFile.write(" ")
            self.logFile.write("\n")
        
        return
