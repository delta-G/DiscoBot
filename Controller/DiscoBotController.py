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

import Controller.JoyReader as JoyReader

import Controller.DiscoBotJoint
import time
import struct

import Controller.DiscoBotComms
import SharedDiscoBot
import Controller.DiscoBotKinematics as dbk




class DiscoBotController:
    
    def putstring(self, aString):
        
        if self.printRedirect is not None:
            self.printRedirect(aString)
        self.logger.logString(str(aString))
        
        print (aString)
        
        return
    
    
    def initComs(self, aPort):
        
        self.comms.initComms(aPort)
            
        return
    
    
    
    def __init__(self, aRedirect = None, aLogger = None):
        
        print (""" 
        ***********************
*****   DiscoBotBot Interface   *******
 ***********************************
""")

        print ("""
        
*********************************************************************        
*********************************************************************        
******* DiscoBot  Copyright (C) 2016  David C.  *********************
**  This program comes with ABSOLUTELY NO WARRANTY; *****************
**  This is free software, and you are welcome to redistribute it  **
**  under certain conditions; ***************************************
*********************************************************************
*********************************************************************


    """)
    
#         self.speedLog = open("robotSpeedLog.csv", "w")
        
        self.properties = {}
        
        self.connectedToBot = False
        self.endProgram = False
        
        self.comms = Controller.DiscoBotComms.DiscoBotComms(self, self.returnParser)
        
        self.printRedirect = aRedirect
        self.logger = aLogger
                
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
        
        self.comTimeOut = 1.0
        
        self.lastBotSNR = 0
        self.lastBotRSSI = 0
        
        self.lastBaseSNR = 0
        self.lastBaseRSSI = 0
### Robot Variables
        self.botStatusByte1 = 0
        self.botStatusByte2 = 0
        self.armStatusByte = 0
        
        self.properties['driveMode'] = ""
        self.properties['cameraPower'] = 0
        self.properties['headlightPower'] = 0
        self.properties['armPower'] = 0
        self.properties['comPower'] = 0
        self.properties['armServoPower'] = 0
        
        self.properties['motorPower'] = 0
        self.properties['motorContEnable'] = 0
        self.properties['v12Power'] = 0
        self.properties['auxPower'] = 0
        self.properties['sonarPower'] = 0
        
        
        self.rmbHeartbeatWarningLevel = SharedDiscoBot.colors['green']
        
#         self.properties['rmbBatteryVoltage'] = 0.0
        self.properties['batteryVoltage'] = 14.55
        self.properties['motorVoltage'] = 1.23
        self.properties['mainVoltage'] = 1.23
        self.properties['comVoltage'] = 1.23
        self.properties['auxVoltage'] = 1.23
        self.properties['v12Voltage'] = 1.23
        
        
        self.properties['leftMotorCount'] = 0
        self.properties['rightMotorCount'] = 0
        self.properties['leftMotorOut'] = 0
        self.properties['rightMotorOut'] = 0
        self.properties['leftMotorSpeed'] = 0
        self.properties['rightMotorSpeed'] = 0
        
        self.sonarDistance = 0
        self.properties['sonarPanAngle'] = 2.25
        
        self.sonarList = [100,200,300,400,1050,1050,700,800,900,1000,1100,1200,1300]
        
        self.properties['baseServoMicros'] = 1500
        self.properties['baseAngle'] = 1.57
        self.properties['shoulderServoMicros'] = 1500
        self.properties['shoulderAngle'] = 1.57
        self.properties['elbowServoMicros'] = 1500
        self.properties['elbowAngle'] = 1.57
        self.properties['wristServoMicros'] = 1500
        self.properties['wristAngle'] = 1.57
        
        self.properties['lastController'] = "LastController"
        
        
### Vars for GUI
        self.showCommands = False
        self.showReturns = False
        self.showDebug = False
        
        self.motorRight = 0
        self.motorLeft = 0
        self.properties['throttleLevel'] = 0
        
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
        self.armJoints = [Controller.DiscoBotJoint.DiscoBotJoint("base", 37, 0, 750, -0.0, 2350, 3.14),
                          Controller.DiscoBotJoint.DiscoBotJoint("shoulder", 103, 0, 544, -0.24, 2400, 2.86),
                          Controller.DiscoBotJoint.DiscoBotJoint("elbow", 97, 0, 544, 2.67, 2400, -0.33),
                          Controller.DiscoBotJoint.DiscoBotJoint("wrist", 165, 31, 650, -1.2, 2400, 2.09),
                          Controller.DiscoBotJoint.DiscoBotJoint("rotate", 0, 0, 564, -0.34907, 2400, 3.316126),
                          Controller.DiscoBotJoint.DiscoBotJoint("grip", 0, 0, 1680, 1.923, 2400, 3.1415),
                          Controller.DiscoBotJoint.DiscoBotJoint("pan", 0, 0, 600, 3.1415, 2350, 0),
                          Controller.DiscoBotJoint.DiscoBotJoint("tilt", 0, 80, 600, 0.8727, 1470, -0.5236)]

        self.servoInfo = []
        for i in range(8):
            self.servoInfo.append([1500,100,1234])
        
        return
    
    def getGripperXYZ(self):
        return dbk.findEndEffectorTip(self.armJoints[0].getCurrentAngle(), self.armJoints[1].getCurrentAngle(), self.armJoints[2].getCurrentAngle(), self.armJoints[3].getCurrentAngle())
    
    
    def getProperty(self, aKey):
        return self.properties[aKey]       
    
    def setRedirect(self, aRedirect):
        self.printRedirect = aRedirect
        return
     
    def connectJoystick(self):
        if self.joy == None:
            
            try:
                self.joy = JoyReader.JoyReader()   
                while not self.joy.connected():
                    self.joy.run()        
            except Exception as ex:
                self.joy = None
                self.putstring(ex)  
                self.putstring('\n')
                        
        return
    
 
    def connectToBot(self):
        if self.comms.commsOn:
            self.putstring("Connecting to Robot\n")            
            if self.comms.wifiMode == True:
                self.outPutRunner("<EP123>")
                time.sleep(0.2)
                self.outPutRunner("<B,E,RMB_RESP>")
            else:
                self.outPutRunner("<P123>")
                time.sleep(0.2)
                self.outPutRunner("<B,E,RMB_RESP><R,F><FFE>")
        
        return    
    
    def killConnection(self):
        if(self.comms.connected()):
            self.putstring ("Closing Connection\n")
            self.comms.close() 
            self.connectedToBot = False           
        else :
            self.putstring ("The connection is not open\n")   
            self.comms.close()             
        return
    
    
    def setLoRaMode(self, aMode):
        if self.comms.wifiMode == False:
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
                self.comTimeOut = 1
        return
    
    
    def outPutRunner(self, cs):
        if self.comms.connected():
            self.comms.send(cs)                  
            self.logger.logString("OUT--> " + str(cs), 2)  
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
#                     if self.sendingController and not self.responseReceived:
#                         self.logger.logString("MISSED RESPONSE")       
                    if self.connectedToBot:
                        if self.sendingController:    
                            if not self.responseReceived:
                                self.logger.logString("MISSED RESPONSE")
                            self.sendRawController()
                            self.lastXboxSendTime = time.time()
                            self.responseReceived = False
#                         else:
#                             self.outPutRunner("<R,R><FFE>")
        
    ### COMMS WITH ROBOT
        if self.comms.connected():
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
            
        if(self.joy.Start() and not self.connectedToBot and not self.lastStart):    
#             self.putstring("Connecting to socket")    
            self.putstring("<Connecting to robot>")                        
            self.connectToBot()
            self.startSendingController()
            self.lastStart = True
        
        if(self.joy.Start() and self.connectedToBot and not self.lastStart):
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
        
        self.logger.logByteArray("DUMP--> ", aByteArray)
        
        dumpMessage = aByteArray
        
        self.botStatusByte1 = dumpMessage[3]
        self.botStatusByte2 = dumpMessage[4]
        self.properties['throttleLevel'] = dumpMessage[5]
#         self.properties['rmbBatteryVoltage'] = dumpMessage[6] / 10.0
        self.properties['sonarPanAngle'] = dumpMessage[6] * (3.1415/256)
        temp = (dumpMessage[7] << 8) + dumpMessage[8]
        self.properties['leftMotorCount'] = self.make16bitSigned(temp)
        temp = (dumpMessage[9] << 8) + dumpMessage[10]        
        self.properties['leftMotorSpeed'] = self.make16bitSigned(temp)
        self.properties['leftMotorOut'] = dumpMessage[11]
        temp = (dumpMessage[12] << 8) + dumpMessage[13]
        self.properties['rightMotorCount'] = self.make16bitSigned(temp)
        temp = (dumpMessage[14] << 8) + dumpMessage[15]        
        self.properties['rightMotorSpeed'] = self.make16bitSigned(temp)
        self.properties['rightMotorOut'] = dumpMessage[16]
        self.lastBotSNR = dumpMessage[17]
        self.lastBotRSSI = -dumpMessage[18]
        self.lastBaseSNR = dumpMessage[19]
        self.lastBaseRSSI = -dumpMessage[20]
        
        self.readStatusByte()
        
        
        return 
    
    def readStatusByte(self):
        mb = self.botStatusByte1 & 3
        if mb == 1:
            self.properties['driveMode'] = "DRIVE"
        elif mb == 2:
            self.properties['driveMode'] = "ARM"
        elif mb == 3:
            self.properties['driveMode'] = "MINE"  
        elif mb == 0:
            self.properties['driveMode'] = "AUTO"          
        
        if(self.botStatusByte1 & 0x10):
            self.properties['cameraPower'] = 1
        else:
            self.properties['cameraPower'] = 0
            
        if(self.botStatusByte1 & 0x20):
            self.properties['headlightPower'] = 1
        else:
            self.properties['headlightPower'] = 0
            
        if(self.botStatusByte1 & 0x40):
            self.properties['armPower'] = 1
        else:
            self.properties['armPower'] = 0
            
        if(self.botStatusByte1 & 0x80):
            self.properties['comPower'] = 1
        else:
            self.properties['comPower'] = 0
            
        if(self.botStatusByte2 & 0x01):
            self.properties['motorPower'] = 1
        else:
            self.properties['motorPower'] = 0
            
        if(self.botStatusByte2 & 0x02):
            self.properties['motorContEnable'] = 1
        else:
            self.properties['motorContEnable'] = 0
            
        if(self.botStatusByte2 & 0x04):
            self.properties['v12Power'] = 1
        else:
            self.properties['v12Power'] = 0
            
        if(self.botStatusByte2 & 0x08):
            self.properties['auxPower'] = 1
        else:
            self.properties['auxPower'] = 0
            
        if(self.botStatusByte2 & 0x10):
            self.properties['sonarPower'] = 1
        else:
            self.properties['sonarPower'] = 0
        
        
            
        return
    
    
    def handleArmDump(self, aByteArray):
        
        self.logger.logByteArray("ARM--> ", aByteArray)
       
        dumpMessage = aByteArray
        
        
        self.armStatusByte = dumpMessage[3]
        whichSet = dumpMessage[4]
        
        dataPoints = []
        
        for i in range(8):
            dp = ((dumpMessage[5+(2*i)] & 0xFF) << 8)
            dp |= dumpMessage[6+(2*i)] & 0xFF
            dataPoints.append(dp)
        
        if whichSet == ord('p'):
            self.logger.logString("pos--> ")
            for i in range(8):
                self.servoInfo[i][0] = dataPoints[i]
                self.armJoints[i].currentMicros = dataPoints[i]
        elif whichSet == ord('s'):
            self.logger.logString("spd--> ")
            for i in range(8):
                self.servoInfo[i][1] = dataPoints[i]
                self.armJoints[i].speed = dataPoints[i]
        elif whichSet == ord('t'):
            self.logger.logString("targ--> ")
            for i in range(8):
                self.servoInfo[i][2] = dataPoints[i]
                self.armJoints[i].target = dataPoints[i]  
                
        if(self.armStatusByte & 1):
            self.properties['armServoPower'] = 1
        else:
            self.properties['armServoPower'] = 0
        
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
        self.properties['batteryVoltage'] = temp/1000.0
        
        temp = (aByteArray[5] << 8) | aByteArray[6]
        self.properties['motorVoltage'] = temp/1000.0
        
        temp = (aByteArray[7] << 8) | aByteArray[8]
        self.properties['mainVoltage'] = temp/1000.0
        
        temp = (aByteArray[9] << 8) | aByteArray[10]
        self.properties['comVoltage'] = temp/1000.0
        
        temp = (aByteArray[11] << 8) | aByteArray[12]
        self.properties['auxVoltage'] = temp/1000.0
        
        temp = (aByteArray[13] << 8) | aByteArray[14]
        self.properties['v12Voltage'] = temp/1000.0
        
        return 
    
    
    def parseReturnString(self, aBuffer):
        
        if aBuffer == "<RMB HBoR>":
            self.lastRMBheartBeat = time.time()
        elif aBuffer == "<RMB_RESP>":
            self.connectedToBot = True
            self.putstring ("Connected to Robot\n")
            
#         elif aBuffer.startswith("<SR,"):
#             self.speedLog.write(aBuffer)
#             self.speedLog.write('\n')
#             print (aBuffer)

                    
        elif aBuffer.startswith("<E-HB"):
            self.currentRssi = aBuffer[5:aBuffer.rfind('>')]
        elif aBuffer.startswith("<E  NewClient @"):
            self.currentSSID = aBuffer[16 : aBuffer.rfind(',')]
            self.currentRssi = aBuffer[aBuffer.rfind(',') : aBuffer.rfind('>')]
        elif aBuffer.startswith("<!"):
            self.putstring("ERROR!! -> ")
            self.putstring(aBuffer)
            self.logger.logString("ERROR!! -> " + aBuffer, 99)
        else:
            self.putstring ("returnBuffer --> ") 
            self.putstring( aBuffer)  
#             for c in aBuffer:
#                 if ord(c) < 33:
#                     self.putstring(ord(c))
#                     self.putstring(',')
            self.putstring('\n')      
        return              
    
    def setResponseRecieved(self):
        self.responseReceived = True
        self.lastResponseTime = time.time()
        self.turnAroundTime = time.time() - self.lastXboxSendTime
        self.lastRMBheartBeat = time.time()
        return 
    
    
    def returnParser(self, aByteArray):
        
        self.logger.logByteArray("RET-->", aByteArray)
            
        if len(aByteArray) >= 3:
            if (aByteArray[0] == ord('<')):
                if(aByteArray[1] >= 0x12) and (aByteArray[1] <= 0x14):
                    if (len(aByteArray) >= aByteArray[2]) and (aByteArray[aByteArray[2]-1] == ord('>')):                        
                        if (aByteArray[1] == 0x13) and (aByteArray[2] == 22):
                            self.handleRawDataDump(aByteArray)
                            self.setResponseRecieved()
                        elif (aByteArray[1] == 0x13) and (aByteArray[2] == 16):
                            self.handleVoltageDump(aByteArray)
                            self.setResponseRecieved()                            
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
#                     print ('..')
                        
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
        
        self.properties['lastController'] = self.displayRawMessage(rawMessage)
        
        self.comms.write(rawMessage)
        self.logger.logByteArray("RAW -->", rawMessage)
        
        return
    
    
    def displayRawMessage(self, aMessage):
        
        retText = ""
        
        for val in aMessage:
            retText += hex(val)               
        
        return retText
    
    
    
    
    
    
#####
