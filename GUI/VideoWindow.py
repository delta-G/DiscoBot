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


import tkinter as tk
import PIL.Image, PIL.ImageTk
import SharedDiscoBot
import cv2
import time
import math

class VideoWindow(tk.Toplevel):
    
    def __init__(self, aParent, aController, aVidSource=0):
        
        self.controller = aController
        self.parent = aParent
        self.vidSource = aVidSource
        tk.Toplevel.__init__(self, width=200, height=200, **SharedDiscoBot.highlightFrameConfig)
        self.protocol("WM_DELETE_WINDOW", self.onClose)
        
        self.mainFrame = tk.Frame(self, **SharedDiscoBot.frameConfig)
        self.vidFrame = tk.Frame(self.mainFrame, pady=30, padx=10, **SharedDiscoBot.frameConfig)
        self.buttonFrame = tk.Frame(self.mainFrame, **SharedDiscoBot.frameConfig)
        
        self.cap = Vidcap(self.controller, self.vidSource)
        self.recording = False 
        self.vidOut = None 
        self.lastFrame = None
        
        self.canvas = tk.Canvas(self.vidFrame, width=self.cap.width, height=self.cap.height, **SharedDiscoBot.canvasConfig)
        self.canvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        
        self.snapButton = tk.Button(self.buttonFrame, text="Snap", width=5, command=self.snapshot, **SharedDiscoBot.buttonConfig)
        self.snapButton.pack(side=tk.LEFT)
        
        self.recordButton = tk.Button(self.buttonFrame, text="Record", width=7, **SharedDiscoBot.buttonConfig)
        self.recordButton.config(command=self.toggleRecording)
        self.recordButton.pack(side=tk.LEFT)
        
        self.mainFrame.pack(fill=tk.BOTH, expand=True)
        
        self.buttonFrame.pack(side=tk.BOTTOM, anchor=tk.S)
        self.vidFrame.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)
        
        return
    
    def snapshot(self):
        ret, frame = self.cap.getFrame()   
        if ret:
            stamp=int(time.time())
            filename="/home/david/robot/001caps/snap"+str(stamp)+".jpg" 
            cv2.imwrite(filename, frame)
        else:
            print("NO FRAME FOR SNAPSHOT!")        
        return 
    
    def toggleRecording(self):
        
        if self.recording:
            self.vidOut.release()
            self.recording = False
            self.recordButton.config(text="Record")
        else:
            size = (int(self.cap.vid.get(3)), int(self.cap.vid.get(4)))
            stamp=int(time.time())
            filename="/home/david/robot/001caps/snap"+str(stamp)+".mp4" 
            self.recording = True
            self.vidOut = cv2.VideoWriter(filename, cv2.VideoWriter_fourcc(*'mp4v'), 29.97, size)            
            self.recordButton.config(text="Stop")
        return 
    
    
    def refresh(self):
        ret, frame = self.cap.getFrame()
        if ret:
            
            imgw = frame.shape[1]
            imgh = frame.shape[0]
            imgr = imgw / imgh
            
            ##  The 22 and 62 are from the padding on the x and y sides.  Need to get rid of magic numbers. 
            winw = self.vidFrame.winfo_width() - 22
            winh = self.vidFrame.winfo_height() - 62
            winr = winw / winh
            
            neww = imgw
            newh = imgh            
            
            ## if ratio is too small then width is constraining.  If ratio is too large then height is small and constraining
            if(winr < imgr):
                neww = winw
                newh = winw/imgr
            elif(winr > imgr):
                newh = winh
                neww = winh*imgr
            
            newsize = (int(neww), int(newh))            
            reFrame = cv2.resize(frame, newsize)           
            
            self.image = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(cv2.cvtColor(reFrame, cv2.COLOR_BGR2RGB)))
            self.canvas.create_image(winw/2,winh/2,image=self.image, anchor=tk.CENTER)
            self.lastFrame = reFrame
            
            if self.recording:
                self.vidOut.write(frame)
        return
    
    def onClose(self):
        self.parent.videoOpen = False
        self.cap.release()
        if self.vidOut != None:
            self.vidOut.release()
        self.destroy()
        
    
#     def __del__(self):
#         self.parent.videoOpen = False
#         self.cap.release()
#         return 
    
    
    
    
    
    
class Vidcap():
    def __init__(self, aController, vidSource=0):
        self.vid = cv2.VideoCapture(vidSource)
        self.controller = aController
        
        if not self.vid.isOpened():
            print("VIDEO FAILED TO OPEN")
            
        self.width = self.vid.get(cv2.CAP_PROP_FRAME_WIDTH)
        self.height = self.vid.get(cv2.CAP_PROP_FRAME_HEIGHT)
        
        self.telemetryColor = (20,255,57)
        
        self.armLineThickness = 2
        
        return 
    
    def getFrame(self):
        if self.vid.isOpened():
            ret, frame = self.vid.read()
            if ret:
                self.addTelemetry(frame)
                return (ret, frame)
            else:
                return (ret, None)
        else:
            return (False, None)
    
    def snapshot(self, aFilename):
        ret, frame = self.getFrame()
        
        if ret:
            cv2.imwrite(aFilename, cv2.cvtColor(frame, cv2.COLOR_RGB2BGR))
        else:
            print("NO FRAME FOR SNAPSHOT!")
                
        return 
    
    def release(self):
        if self.vid.isOpened():            
            self.vid.release()
            return 
        
    def convertCoords(self, aStart, aXYAtup):
        x = aStart[0] + aXYAtup[0]
        y = aStart[1] - aXYAtup[1]
        return(int(x), int(y))
        
    def addTelemetry (self, aFrame):
        
        widthFraction = 4
        heightFraction = 4
        
        width = int(self.vid.get(3))
        height = int(self.vid.get(4))
        
        totalHeightPossible = self.controller.armJoints[0].length + self.controller.armJoints[1].length + self.controller.armJoints[2].length + self.controller.armJoints[3].length
        
        
        startingPoint = (int(width - (width/(widthFraction * 2))) , int(height/heightFraction))
        
        ###  Height of the window / height of the arm
        sizeRatio = (1.0 * (height/heightFraction)) / (1.0 * (totalHeightPossible))
        
        ## X Y coordinate and approach angle XYA
        basePointXYA = (0, 0, 1.5708)
        
        shoulderPoint = (basePointXYA[0], basePointXYA[1], 1.5708) 
        elbowPoint = self.controller.armJoints[1].findEndXYandApproach(shoulderPoint, self.controller.servoInfo[1][0], sizeRatio)
        wristPoint = self.controller.armJoints[2].findEndXYandApproach(elbowPoint, self.controller.servoInfo[2][0], sizeRatio)
        gripperWristPoint = self.controller.armJoints[3].findOffsetPoint(wristPoint, self.controller.armJoints[3].offset, self.controller.servoInfo[3][0], sizeRatio)
        gripperTipPoint = self.controller.armJoints[3].findEndXYandApproach(wristPoint, self.controller.servoInfo[3][0], sizeRatio)
        
        cv2.line(aFrame, startingPoint, self.convertCoords(startingPoint, shoulderPoint), self.telemetryColor , self.armLineThickness)
        cv2.line(aFrame, self.convertCoords(startingPoint, shoulderPoint), self.convertCoords(startingPoint, elbowPoint), self.telemetryColor , self.armLineThickness)
        cv2.line(aFrame, self.convertCoords(startingPoint, elbowPoint), self.convertCoords(startingPoint, wristPoint), self.telemetryColor , self.armLineThickness)
        cv2.line(aFrame, self.convertCoords(startingPoint, wristPoint), self.convertCoords(startingPoint, gripperWristPoint),self.telemetryColor , self.armLineThickness)
        cv2.line(aFrame, self.convertCoords(startingPoint, gripperWristPoint), self.convertCoords(startingPoint, gripperTipPoint), self.telemetryColor , self.armLineThickness)
        
        gimbalOffsetPoint = self.controller.armJoints[3].findOffsetPoint(wristPoint, self.controller.armJoints[7].offset, self.controller.servoInfo[3][0], sizeRatio)
        gimbalOffsetCoords = self.convertCoords(startingPoint, gimbalOffsetPoint)
        
        
        gimbalTiltAngle = gripperWristPoint[2] + ((self.controller.armJoints[7].microsToAngle(self.controller.servoInfo[7][0])) - (math.pi/2))
        tiltX = ((25) * (math.cos(gimbalTiltAngle))) + gimbalOffsetCoords[0]
        tiltY = ((25) * (-math.sin(gimbalTiltAngle))) + gimbalOffsetCoords[1]
        tiltCoords = (int(tiltX), int(tiltY))
        
        cv2.line(aFrame, self.convertCoords(startingPoint, wristPoint), gimbalOffsetCoords, self.telemetryColor, self.armLineThickness)
        cv2.line(aFrame, gimbalOffsetCoords, tiltCoords, self.telemetryColor, self.armLineThickness)
        
        
        
        #### Directional Circle
        
        circleCenter = (startingPoint[0], startingPoint[1] + 40)
        circleDiameter = 25
        
        cv2.circle(aFrame, circleCenter, circleDiameter, self.telemetryColor, 1)
        
        
        ### Tic Marks
        
        
        numberOfTics = 16
        ticSeparation = 2 * math.pi / numberOfTics
        
        for tic in range(numberOfTics):
            ticLength = 2
            if tic % 4 == 0:
                ticLength = 6
            elif tic % 4 == 2:
                ticLength = 4
            
            ticAngle = ticSeparation * tic
            ticBegin = ( int((circleDiameter) * math.cos(ticAngle)) + circleCenter[0], int((circleDiameter) * math.sin(ticAngle)) + circleCenter[1])
        
            ticEnd = (int((circleDiameter + ticLength) * math.cos(ticAngle)) + circleCenter[0], int((circleDiameter + ticLength) * math.sin(ticAngle)) + circleCenter[1])
            
            cv2.line(aFrame, ticBegin, ticEnd, self.telemetryColor, 1)
            
        
        
        
        
        
        ###  Base Angle
        baseAngle = -(self.controller.armJoints[0].microsToAngle(self.controller.servoInfo[0][0]))
        armSegEnd = (int((circleDiameter-8) * math.cos(baseAngle)) + circleCenter[0] ,  int((circleDiameter-8) * math.sin(baseAngle)) + circleCenter[1])
        
        cv2.line(aFrame, circleCenter, armSegEnd, self.telemetryColor, 2)
        
        ####  Camera Angle
        gimbalPanAngle = baseAngle + ((self.controller.armJoints[6].microsToAngle(self.controller.servoInfo[6][0])) - (math.pi/2))
        
        gimbalSegBegin = ( int((circleDiameter - 4) * math.cos(gimbalPanAngle)) + circleCenter[0], int((circleDiameter - 4) * math.sin(gimbalPanAngle)) + circleCenter[1])
        
        gimbalSegEnd = (int((circleDiameter) * math.cos(gimbalPanAngle)) + circleCenter[0], int((circleDiameter) * math.sin(gimbalPanAngle)) + circleCenter[1])
        
        cv2.line(aFrame, gimbalSegBegin, gimbalSegEnd, self.telemetryColor, 2)
        
        
        #### Drive Angle
        
        ls = self.controller.getProperty('leftMotorSpeed')
        rs = self.controller.getProperty('rightMotorSpeed')
        
        if not ((ls==0) and (rs==0)):
            driveAngle = math.pi / 4.0
            ## guard against divide by 0
            if(ls == 0):
                if(rs > 0):
                    driveAngle = math.pi / 2.0
                elif(rs<0):
                    driveAngle = 3*math.pi/2.0
            else:
                driveAngle = math.atan(rs/ls) 
            
            ### Rotate to stick frame (see ArmGraphicFrame)
            driveAngle = driveAngle + (math.pi/4.0)
            
            if(ls<0):
                driveAngle = driveAngle + math.pi 
            
            if driveAngle < 0:
                driveAngle = driveAngle + (2*math.pi)
                
            driveAngle = -driveAngle
            
            driveSegBegin = ( int((circleDiameter) * math.cos(driveAngle)) + circleCenter[0], int((circleDiameter) * math.sin(driveAngle)) + circleCenter[1])
        
            driveSegEnd = (int((circleDiameter + 10) * math.cos(driveAngle)) + circleCenter[0], int((circleDiameter + 10) * math.sin(driveAngle)) + circleCenter[1])
            
            cv2.line(aFrame, driveSegBegin, driveSegEnd, self.telemetryColor, 2)
        
        
        ##### TEXT SECTION
        font = cv2.FONT_HERSHEY_SIMPLEX
        textSeparation = 10
        textStart = (circleCenter[0] + 10 , circleCenter[1] + int(circleDiameter * 1.5) )
        
        cv2.putText(aFrame, f"BATT: {self.controller.getProperty('batteryVoltage'):.2f}V", textStart, font, 0.3, self.telemetryColor, 1, cv2.LINE_AA)
        
        textStart = (textStart[0] , textStart[1] + textSeparation)
        cv2.putText(aFrame, f"THR: {self.controller.getProperty('throttleLevel'):03d}", textStart, font, 0.3, self.telemetryColor, 1, cv2.LINE_AA)
        
        textStart = (textStart[0] , textStart[1] + textSeparation)
        cv2.putText(aFrame, f"MODE: {self.controller.getProperty('driveMode')}", textStart, font, 0.3, self.telemetryColor, 1, cv2.LINE_AA)
        
        if self.controller.comms.isWiFiMode():
            textStart = (textStart[0] , textStart[1] + textSeparation)
            cv2.putText(aFrame, f"RSSI: {self.controller.lastWifiRSSI}", textStart, font, 0.3, self.telemetryColor, 1, cv2.LINE_AA)
        else:
            textStart = (textStart[0] -5 , textStart[1] + textSeparation)
            cv2.putText(aFrame, "BOT:", textStart, font, 0.3, self.telemetryColor, 1, cv2.LINE_AA)
            textStart = (textStart[0] +5, textStart[1] + textSeparation)
            cv2.putText(aFrame, f"SNR: {self.controller.lastBotSNR}", textStart, font, 0.3, self.telemetryColor, 1, cv2.LINE_AA)
            textStart = (textStart[0], textStart[1] + textSeparation)
            cv2.putText(aFrame, f"RSSI: {self.controller.lastBotRSSI}", textStart, font, 0.3, self.telemetryColor, 1, cv2.LINE_AA)
            textStart = (textStart[0] -5 , textStart[1] + textSeparation)
            cv2.putText(aFrame, "BASE:", textStart, font, 0.3, self.telemetryColor, 1, cv2.LINE_AA)
            textStart = (textStart[0] +5, textStart[1] + textSeparation)
            cv2.putText(aFrame, f"SNR: {self.controller.lastBaseSNR}", textStart, font, 0.3, self.telemetryColor, 1, cv2.LINE_AA)
            textStart = (textStart[0], textStart[1] + textSeparation)
            cv2.putText(aFrame, f"RSSI: {self.controller.lastBaseRSSI}", textStart, font, 0.3, self.telemetryColor, 1, cv2.LINE_AA)
            
          
        
        return 
        
        
###  TODO:  See https://stackoverflow.com/questions/14140495/how-to-capture-a-video-and-audio-in-python-from-a-camera-or-webcam
###  for more on finishing the recorder and adding audio to it with ffmpeg
        
# class VideoRecorder():
#     
#     def __init__(self, aVidSource=0):
#         
#         self.open = True
#         self.vidSource = aVidSource
#         self.fps=6
#         self.fourcc="MJPG"
#         self.frameSize=(640,480)
#         self.vidFile="/home/david/robot/VideoTemp/videofile.avi"
#         self.vidcap=Vidcap(0)
#         self.vidWrite=cv2.VideoWriter_fourcc(*self.fourcc)
#         self.vidOut=cv2.VideoWriter(self.vidFile, self.vidWrite, self.fps, self.frameSize)
#         self.frameCount=1
#         
#         return 
#     
#     def record(self):
#         
#         return 
#     
        
        
    


