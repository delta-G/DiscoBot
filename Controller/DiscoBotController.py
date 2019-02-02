#  pyBot  --  The Python control software for my robot
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
import DiscoBotServo
import time
import errno
from __builtin__ import False
from _socket import MSG_DONTWAIT
from _socket import SHUT_RDWR

import serial


useSerial = True
useWifi = False

class DiscoBotController:
    
    def putstring(self, aString):
        
        if self.printRedirect is not None:
            self.printRedirect(aString)
        
        print aString,
        
        return
    
    def initComs(self):
        
        if(useWifi):
        
            self.sockOut = socket.socket(socket.AF_INET , socket.SOCK_STREAM)
#             self.sockOut.setblocking(0)
        
#             self.sockArgs = ('10.10.0.24' , 1234)
#             self.sockArgs = ('192.168.4.1' , 1234)
            self.sockArgs = ('192.168.1.75' , 1234)
            
        if(useSerial):
            
            self.serOut = serial.Serial('/dev/ttyUSB0', 115200)
            
        
        return
    
    def __init__(self, aRedirect = None):
        
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
                
        self.putstring("Global Interface Initializing\n")
        
        self.initComs()

        

        self.joy = xbox.Joystick()
        
        self.putstring ("Controller attached!\n")

        self.returnBuffer = ""
        self.receivingReturn = False
        self.lastRMBheartBeat = time.time()
        self.RMBheartBeatWarningTime = time.time()
        self.lastGimbalTime = time.time()
        
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
        
        self.showCommands = False
        self.showReturns = False
        self.showDebug = False


        self.motorRight = 0
        self.motorLeft = 0
        
        self.invertShoulder = True
        self.invertElbow = True
        self.invertWrist = False
        
        self.lastY = 0
        self.lastA = 0
        self.lastB = 0
        self.lastX = 0
        self.lastGuide = 0
        self.lastThumbR = 0
        self.lastThumbL = 0
        self.controlMode = 0
        self.lastRunTime = 0
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
        self.armServos = [DiscoBotServo.DiscoBotServo("base", 1500, 544, 2400), 
                          DiscoBotServo.DiscoBotServo("shoulder" , 1214, 544, 2400), 
                          DiscoBotServo.DiscoBotServo("elbow" , 1215, 544, 2400), 
                          DiscoBotServo.DiscoBotServo("wrist" , 2000, 544, 2400), 
                          DiscoBotServo.DiscoBotServo("rotate", 1500, 544, 2400), 
                          DiscoBotServo.DiscoBotServo("grip", 2000, 1680, 2400), 
                          DiscoBotServo.DiscoBotServo("pan", 1500, 1000, 2400), 
                          DiscoBotServo.DiscoBotServo("tilt", 1500, 1000, 2400)]
        return
    
    def setRedirect(self, aRedirect):
        self.printRedirect = aRedirect
        return
     
     
    def connectToBot(self):
        self.putstring("Connecting to Robot\n")
        if(useWifi):
            self.sockOut = socket.socket(socket.AF_INET , socket.SOCK_STREAM)        
            self.sockOut.connect(self.sockArgs)
        self.socketConnected = True
        self.putstring ("Connected to Robot\n")   
        
        self.outPutRunner("<ESTART><ECONNECT><B,HB>")
        
        return    
    
    def killConnection(self):
        if(self.socketConnected):
            if(useWifi):
                self.putstring("Shutting Down Connection\n")
                self.sockOut.shutdown(SHUT_RDWR)
                self.sockOut.close()
            self.socketConnected = False
        else :
            self.putstring ("The connection is not open\n")
                
        return
    
    def outPutRunner(self, cs):
        if self.socketConnected:
            if(useWifi):
                self.sockOut.send(cs)
            if(useSerial):
                self.serOut.write(cs)
                self.serOut.flush()
        if self.showCommands:
            if not str(cs).startswith("<X,0D14"):
                self.putstring("COM--> " + str(cs) + '\n')
        
        return
    
    def moveToByAngle(self, aTup):
        i = 0
        for servo in self.armServos:
            servo.moveToImmediate(servo.angleToMicroseconds(aTup[i]))
            self.armCommandSender(i)
            i += 1
         
        return
    
    
    def runInterface(self):       
        
        if(self.joy.Start() and not self.socketConnected):
            
            self.connectToBot()
            
        if self.joy.Back() or not self.joy.connected():
            return False                
### REQUEST HEARTBEAT        
        if time.time() - self.lastRMBhbRequest >= 2:
            self.outPutRunner("<R,HB>")
            self.lastRMBhbRequest = time.time()
        if time.time() - self.lastRMBmotorRequest >= 0.5:
            self.outPutRunner("<R,M>")
            self.lastRMBmotorRequest = time.time()
            
### CONTROLLER LOOP        
        if time.time() - self.lastRunTime >= 0.02:
# ### JOY A            
#             joyA = self.joy.A()
#             if(joyA and not self.lastA):
#                 self.requestFromESP('B')
#             self.lastA = joyA
# ### JOY B            
#             joyB = self.joy.B()
#             if(joyB and not self.lastB):
#                 self.killConnection()
#             self.lastB = joyB
# ### JOY Y            
#             joyY = self.joy.Y()        
#             if (joyY and not self.lastY):
#                 self.controlMode += 1
#                 self.controlMode %= 2
#                 if(self.controlMode == 0):
#                     self.putstring("Drive Mode Activated\n")
#                 elif(self.controlMode == 1):
#                     self.putstring("Arm Mode Activated\n")
#             self.lastY = joyY
# ### JOY X
#             joyX = self.joy.X()
#             if (joyX and not self.lastX):
#                 self.outPutRunner("<EW>")
#             self.lastX = joyX
# ###  JOY GDUIE
#             joyG = self.joy.Guide()
#             if (joyG and not self.lastGuide):
#                 self.commandMode()
#             self.lastGuide = joyG
# 
#                 
#                 
#             
# ### END CONTROLLER LOOP
#             
#             if(self.controlMode == 0):
#                 self.driveMode()
#             elif(self.controlMode == 1):
#                 self.armMode()
            if self.socketConnected:    
                self.sendRawController()
            self.lastRunTime = time.time()
        
        self.listenForESP()
        
        if (time.time() - self.lastRMBheartBeat >= 10) and (time.time() - self.RMBheartBeatWarningTime >= 10):
            self.putstring ("*****   MISSING RMB HEARTBEAT "),
            self.putstring (time.time() - self.lastRMBheartBeat),
            self.putstring ("  Seconds  ****\n")
            self.rmbHeartbeatWarningLevel = "red"
            self.RMBheartBeatWarningTime = time.time()        
            
        return True
    
    
    def listenForESP(self):        
        
        if self.socketConnected:
            try:
                if(useWifi):
                    line_read = self.sockOut.recvfrom(1024, MSG_DONTWAIT)[0]
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

##########################
###########DRIVE MODES
##########################       
    def driveMode(self):
        
        self.dpadGimbal()
        
        leftBump = self.joy.leftBumper()
        rightBump = self.joy.rightBumper()
        leftTrigger = self.joy.leftTrigger()
        rightTrigger = self.joy.rightTrigger()
        
        self.armModeHelper(rightTrigger - leftTrigger, self.GRIP)
        if(leftBump):
            self.armServos[self.BASE].increment(1.0)
            self.armCommandSender(self.BASE)
        elif(rightBump):
            self.armServos[self.BASE].increment(-1.0)
            self.armCommandSender(self.BASE)
        
        leftY = self.joy.leftY()
        rightY = self.joy.rightY()
        
        ml = 0
        mr = 0
        
        
        if (leftY > 0) :
            ml = 1
        elif (leftY < 0) :
            ml = -1;
        else: 
            ml = 0    
        
        if rightY > 0 :
            mr = 1
        elif rightY < 0 :
            mr = -1;
        else: 
            mr = 0
            
        if ml != self.motorLeft:
            self.motorLeft = ml
            commandString = ""
            commandString += "<"
            commandString += "ML"
            commandString += ","
            commandString += str(self.motorLeft)
            commandString += ">"
            self.outPutRunner(commandString)
        
        if mr != self.motorRight:
            self.motorRight = mr
            commandString = ""
            commandString += "<"
            commandString += "MR"
            commandString += ","
            commandString += str(self.motorRight)
            commandString += ">"
            self.outPutRunner(commandString)   
            
        return
    
    def armModeHelper(self, stickPosition , servo, invert = False):
        if stickPosition != 0:
            if invert:
                stickPosition = -stickPosition

            self.armServos[servo].increment(stickPosition)
#             if(stickPosition > 0):
#                 self.armServos[servo].increase()
#                 self.armCommandSender(servo)
#             elif(stickPosition < 0):
#                 self.armServos[servo].decrease()
            self.armCommandSender(servo)
                
            return True
        
        return False
    
    def armCommandSender(self, servo):
        commandString = ""
        commandString += "<S"
        commandString += str(servo)
        commandString += ","
        commandString += str(self.armServos[servo].position)
        commandString += ">"
        self.outPutRunner(commandString)
        
        return
    
    def stickGimbal(self, panVal, tiltVal):
        
        if time.time() - self.lastGimbalTime >= 0.2:
            self.lastGimbalTime = time.time()
            
            self.armModeHelper(panVal, self.PAN)
            self.armModeHelper(tiltVal, self.TILT)            
        
        return
    
    def dpadGimbal(self):
        
        self.gimbalStepSize = 1
        
        if time.time() - self.lastGimbalTime >= 0.2:
            self.lastGimbalTime = time.time()
        
        
            dpad = ((self.joy.dpadDown() << 3) | (self.joy.dpadLeft() << 2) | (self.joy.dpadRight() << 1) | (self.joy.dpadUp()))
        
            ## Nothing Pressed
            if(dpad == 0):
                pass
            ## UP 
            elif(dpad == 1):
                self.armServos[self.TILT].increment(-self.gimbalStepSize)
                self.armCommandSender(self.TILT)
                
            ## RIGHT
            elif(dpad == 2):
                self.armServos[self.PAN].increment(-self.gimbalStepSize)
                self.armCommandSender(self.PAN)
            ## UP / RIGHT
            elif(dpad == 3):
                self.armServos[self.TILT].increment(-self.gimbalStepSize)
                self.armServos[self.PAN].increment(-self.gimbalStepSize)
                self.armCommandSender(self.TILT)
                self.armCommandSender(self.PAN)
            ## LEFT
            elif(dpad == 4):
                self.armServos[self.PAN].increment(self.gimbalStepSize)
                self.armCommandSender(self.PAN)
            ## UP / LEFT
            elif(dpad == 5):
                self.armServos[self.TILT].increment(-self.gimbalStepSize)
                self.armServos[self.PAN].increment(self.gimbalStepSize)
                self.armCommandSender(self.TILT)
                self.armCommandSender(self.PAN)
            ## DOWN
            elif(dpad == 8):
                self.armServos[self.TILT].increment(self.gimbalStepSize)
                self.armCommandSender(self.TILT)
            ## DOWN / RIGHT
            elif(dpad == 10):
                self.armServos[self.TILT].increment(self.gimbalStepSize)
                self.armServos[self.PAN].increment(-self.gimbalStepSize)
                self.armCommandSender(self.PAN)
                self.armCommandSender(self.TILT)
            ## DOWN / LEFT
            elif(dpad == 12):
                self.armServos[self.TILT].increment(self.gimbalStepSize)
                self.armServos[self.PAN].increment(self.gimbalStepSize)
                self.armCommandSender(self.PAN)
                self.armCommandSender(self.TILT)
            else:
                pass        
        
        
        
        
        return
    
        
    def dpadMotor(self):
        
        ml = 0
        mr = 0
        
        dpad = ((self.joy.dpadDown() << 3) | (self.joy.dpadLeft() << 2) | (self.joy.dpadRight() << 1) | (self.joy.dpadUp()))
        
        ## Nothing Pressed
        if(dpad == 0):
            ml = 0
            mr = 0
        ## UP 
        elif(dpad == 1):
            ml = 1
            mr  = 1
        ## RIGHT
        elif(dpad == 2):
            ml = 1
            mr  = -1
        ## UP / RIGHT
        elif(dpad == 3):
            ml = 1
            mr  = 0
        ## LEFT
        elif(dpad == 4):
            ml = -1
            mr  = 1
        ## UP / LEFT
        elif(dpad == 5):
            ml = 0
            mr  = 1
        ## DOWN
        elif(dpad == 8):
            ml = -1
            mr  = -1
        ## DOWN / RIGHT
        elif(dpad == 10):
            ml = -1
            mr  = 0
        ## DOWN / LEFT
        elif(dpad == 12):
            ml = 0
            mr  = -1
        else:
            ml = 0
            mr = 0
        
        
        if ml != self.motorLeft:
            self.motorLeft = ml
            commandString = ""
            commandString += "<"
            commandString += "ML"
            commandString += ","
            commandString += str(self.motorLeft)
            commandString += ">"
            self.outPutRunner(commandString)
        
        if mr != self.motorRight:
            self.motorRight = mr
            commandString = ""
            commandString += "<"
            commandString += "MR"
            commandString += ","
            commandString += str(self.motorRight)
            commandString += ">"
            self.outPutRunner(commandString)   
        
        return
        
    def armMode(self):
        
        self.dpadMotor()
        
        deadZ = 1000
            
        thumbR = self.joy.rightThumbstick()
        thumbL = self.joy.leftThumbstick()
        leftX = self.joy.leftX(deadZ);
        leftY = self.joy.leftY(deadZ);
        rightX = self.joy.rightX(deadZ);
        rightY = self.joy.rightY(deadZ);
        leftBump = self.joy.leftBumper()
        rightBump = self.joy.rightBumper()
        leftTrigger = self.joy.leftTrigger()
        rightTrigger = self.joy.rightTrigger()   
        
        
        self.armModeHelper(rightX, self.ROTATE)
        self.armModeHelper(rightY, self.WRIST, self.invertWrist)
        self.armModeHelper(leftX, self.SHOULDER, self.invertShoulder)
        self.armModeHelper(leftY, self.ELBOW, self.invertElbow)
        self.armModeHelper(rightTrigger - leftTrigger, self.GRIP)
        if(leftBump):
            self.armServos[self.BASE].increment(0.1)
            self.armCommandSender(self.BASE)
        elif(rightBump):
            self.armServos[self.BASE].increment(-0.1)
            self.armCommandSender(self.BASE)
        
        if thumbR and not self.lastThumbR:
            self.invertElbow = not self.invertElbow
            self.invertWrist = not self.invertWrist
        self.lastThumbR = thumbR
        
        if thumbL and not self.lastThumbL:
            self.invertShoulder = not self.invertShoulder
        self.lastThumbL = thumbL
        
        
        return
        
    
    
    def sittingHome(self):
        
#         self.outPutRunner("<S1,1500><S2,1500>,<S3,2000>")
        self.armServos[self.SHOULDER].moveToImmediate(1500)
        self.armCommandSender(self.SHOULDER)
        self.armServos[self.ELBOW].moveToImmediate(1500)
        self.armCommandSender(self.ELBOW)
        self.armServos[self.WRIST].moveToImmediate(2000)
        self.armCommandSender(self.WRIST)
        time.sleep(0.5)
#         self.outPutRunner("<S1,1950><S2,1950>")
        self.armServos[self.SHOULDER].moveToImmediate(1950)
        self.armServos[self.ELBOW].moveToImmediate(1950)
        self.armServos[self.WRIST].moveToImmediate(1400)
        self.armCommandSender(self.SHOULDER)
        self.armCommandSender(self.ELBOW)
        self.armCommandSender(self.WRIST)
        time.sleep(0.2)
#         self.outPutRunner("<S1,2400><S2,2400>")
        self.armServos[self.SHOULDER].moveToImmediate(2400)
        self.armServos[self.ELBOW].moveToImmediate(2400)
        self.armCommandSender(self.SHOULDER)
        self.armCommandSender(self.ELBOW)
        time.sleep(0.1)
#         self.outPutRunner("<S7,1350><S6,1050><S3,1400>")
        self.armServos[self.PAN].moveToImmediate(1350)
        self.armServos[self.TILT].moveToImmediate(1050)
        self.armServos[self.WRIST].moveToImmediate(1400)
        self.armCommandSender(self.PAN)
        self.armCommandSender(self.TILT)
        self.armCommandSender(self.WRIST)
        return
    
   
    def standingHome(self):
        
        self.armServos[self.SHOULDER].moveToImmediate(1080)
        self.armCommandSender(self.SHOULDER)
        self.armServos[self.ELBOW].moveToImmediate(880)
        self.armCommandSender(self.ELBOW)
        self.armServos[self.WRIST].moveToImmediate(895)
        self.armCommandSender(self.WRIST)

        self.armServos[self.PAN].moveToImmediate(1350)
        self.armServos[self.TILT].moveToImmediate(1220)
        self.armCommandSender(self.PAN)
        self.armCommandSender(self.TILT)
        return        
    
    
    def sendRawController(self):
        
        ###  Need to send as ascii hexadecimal 14 integers.  
#             uint16_t checkBytes;
#             uint16_t buttonState;
#             uint8_t leftTrigger;
#             uint8_t rightTrigger;
#             int16_t hatValues[4];

        ###  Let's start by getting everything packed up into 16 bit ints
        checkBytes = 0x140D
        
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
            buttonStateInt &= 0x0100
        if(self.joy.dpadRight()):
            buttonStateInt &= 0x0800
        if(self.joy.dpadDown()):
            buttonStateInt &= 0x0200
        if(self.joy.dpadLeft()):
            buttonStateInt &= 0x0400
        
        if(self.joy.Back()):
            buttonStateInt &= 0x2000
        if(self.joy.Start()):
            buttonStateInt &= 0x1000
        if(self.joy.leftThumbstick()):
            buttonStateInt &= 0x4000
        if(self.joy.rightThumbstick()):
            buttonStateInt &= 0x8000
            
        if(self.joy.leftBumper()):
            buttonStateInt &= 0x0001
        if(self.joy.rightBumper()):
            buttonStateInt &= 0x0002
            
        if(self.joy.B()):
            buttonStateInt &= 0x0020
        if(self.joy.A()):
            buttonStateInt &= 0x0010
        if(self.joy.X()):
            buttonStateInt &= 0x0040
        if(self.joy.Y()):
            buttonStateInt &= 0x0080
        
            
        if(self.joy.Guide()):
            buttonStateInt &= 0x0004
            
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
        
                ###  Need to send as ascii hexadecimal 14 integers.  
#             uint16_t checkBytes;
#             uint16_t buttonState;
#             uint8_t leftTrigger;
#             uint8_t rightTrigger;
#             int16_t hatValues[4];

        messtr = "%0.4X%0.4X%0.2X%0.2X%0.4X%0.4X%0.4X%0.4X" %((int)(checkBytes), (int)(buttonStateInt), (int)(leftTrigByte), (int)(rightTrigByte), (int)(leftHatX) & (2**16-1), (int)(leftHatY) & (2**16-1), (int)(rightHatX) & (2**16-1), (int)(rightHatY) & (2**16-1))

        newmess = "<X,"
        
        
        
        newmess += messtr[2] + messtr[3]
        newmess += messtr[0] + messtr[1]
        
        newmess += messtr[6] + messtr[7]
        newmess += messtr[4] + messtr[5]
        
        newmess += messtr[8] + messtr[9]
        newmess += messtr[10] + messtr[11]
        
        newmess += messtr[14] + messtr[15]
        newmess += messtr[12] + messtr[13]
        
        newmess += messtr[18] + messtr[19]
        newmess += messtr[16] + messtr[17]
        
        newmess += messtr[22] + messtr[23]
        newmess += messtr[20] + messtr[21]
        
        newmess += messtr[26] + messtr[27]
        newmess += messtr[24] + messtr[25]
        
        newmess += ">"
        
#         print "Raw Controller Message"
#         print newmess
        
        self.outPutRunner(newmess)

        
        return
