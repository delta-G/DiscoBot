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
import math
import GUI.ArmCalWindow
import SharedDiscoBot

class ArmGraphicFrame(tk.Frame):
    
    def __init__ (self, aParent, aController, aGui):
        
        self.parent = aParent
        self.gui = aGui
        tk.Frame.__init__(self, self.parent, **SharedDiscoBot.frameConfig)
        self.controller = aController
        
        self.canvasWidth = 250
        self.canvasHeight = 200
        
        self.canvas = tk.Canvas(self, width=self.canvasWidth, height=self.canvasHeight, **SharedDiscoBot.canvasConfig)
        
        self.xLabel = tk.Label(self, width=12, text="x", **SharedDiscoBot.highlightLabelConfig)
        self.yLabel = tk.Label(self, width=12, text="y", **SharedDiscoBot.highlightLabelConfig)
        self.zLabel = tk.Label(self, width=12, text="z", **SharedDiscoBot.highlightLabelConfig)
        self.phiLabel = tk.Label(self, width=12, text="phi", **SharedDiscoBot.highlightLabelConfig)
        
        self.baseLabel = tk.Label(self, width=12, text="base", **SharedDiscoBot.highlightLabelConfig)
        self.shoulderLabel = tk.Label(self, width=12, text="shoul", **SharedDiscoBot.highlightLabelConfig)
        self.elbowLabel = tk.Label(self, width=12, text="elbow", **SharedDiscoBot.highlightLabelConfig)
        self.wristLabel = tk.Label(self, width=12, text="wrist", **SharedDiscoBot.highlightLabelConfig)
        
        
        self.canvas.pack(side=tk.LEFT)   
        self.canvas.bind("<Double-Button-1>", self.launchCalibrationWindow)
        self.xLabel.pack(side=tk.TOP)
        self.yLabel.pack(side=tk.TOP)
        self.zLabel.pack(side=tk.TOP)
        self.phiLabel.pack(side=tk.TOP)
        
        self.baseLabel.pack(side=tk.TOP)
        self.shoulderLabel.pack(side=tk.TOP)
        self.elbowLabel.pack(side=tk.TOP)
        self.wristLabel.pack(side=tk.TOP)
        
        
        self.driveAngle = 0.0
        self.driveLineColor = "white"
        self.driveIndicatorHeight = 50
        self.driveIndicatorWidth = 50        
        
        return 
    
    def launchCalibrationWindow(self, event):
        
        if not self.gui.calibrationWindowActive:
            self.gui.calibrationWindowActive = True
            armCalWindow = GUI.ArmCalWindow.ArmCalibrationWindowClass(self.gui, self.controller)
            
        
#         global calibrationWindow
#         try:
#             if calibrationWindow.state() == "normal" :
#                 calibrationWindow.focus()
#                 calibrationWindow.lift()
#                  
#         except NameError as e:
#             print(e)
#             calibrationWindow = tk.Toplevel(self.parent)
#             ArmCalWindow.ArmCalibrationWindowClass(self.controller)
                        
        
        return  
     
       
    
     
    def squareCanvas(self):
        w = (self.canvasWidth - 1)
        h = (self.canvasHeight - 1)
        self.canvas.create_line(1,1,1,h)
        self.canvas.create_line(1,h,w,h)
        self.canvas.create_line(w,h,w,1)
        self.canvas.create_line(w,1,1,1)
        return
           
        
    def toCanvasCoords(self, aXYAtuple, aRatio):
        reX = aXYAtuple[0]
        reY = (self.canvasHeight - aXYAtuple[1])
        
        return (reX, reY)
        
    
    def drawSegment(self, aXYtuple1, aXYtuple2, aColor):
        
        self.canvas.create_line(aXYtuple1[0], aXYtuple1[1], aXYtuple2[0], aXYtuple2[1], width=2, fill=aColor)
        return
    
    
    def refresh(self):
        self.drawArm()
        self.baseLabel.configure(text='{0:>02.3f}'.format(self.controller.armJoints[0].getCurrentAngle()))
        self.shoulderLabel.configure(text='{0:>02.3f}'.format(self.controller.armJoints[1].getCurrentAngle()))
        self.elbowLabel.configure(text='{0:>02.3f}'.format(self.controller.armJoints[2].getCurrentAngle()))
        self.wristLabel.configure(text='{0:>02.3f}'.format(self.controller.armJoints[3].getCurrentAngle()))
        tip = self.controller.getGripperXYZ()
        self.xLabel.configure(text='{0:>02.3f}'.format(tip[0]))
        self.yLabel.configure(text='{0:>02.3f}'.format(tip[1]))
        self.zLabel.configure(text='{0:>02.3f}'.format(tip[2]))
        self.phiLabel.configure(text='{0:>02.3f}'.format(tip[3]))
        return 
    
    
    
    ###  Draw arm with base at x,y of this tuple 
    def drawArm(self):
        
        aXYAtuple = (100, 50, 1.5708)
        
        totalHeightPossible = self.controller.armJoints[0].length + self.controller.armJoints[1].length + self.controller.armJoints[2].length + self.controller.armJoints[3].length
        
        guiHeight = self.canvas.winfo_height() - aXYAtuple[1]
        
        sizeRatio = 1.0 * guiHeight / (1.0 * totalHeightPossible)
        
        largestX = 0
        
        basePoint = (aXYAtuple[0], aXYAtuple[1], 1.5708)
        if(abs(basePoint[0]) > largestX):
            largestX = abs(basePoint[0])
        shoulderPoint = (aXYAtuple[0], (aXYAtuple[1] + (self.controller.armJoints[0].length * sizeRatio)), 1.5708)         
        if(abs(shoulderPoint[0]) > largestX):
            largestX = abs(shoulderPoint[0])       
        elbowPoint = self.controller.armJoints[1].findEndXYandApproach(shoulderPoint, self.controller.servoInfo[1][0], sizeRatio)
        if(abs(elbowPoint[0]) > largestX):
            largestX = abs(elbowPoint[0])
        wristPoint = self.controller.armJoints[2].findEndXYandApproach(elbowPoint, self.controller.servoInfo[2][0], sizeRatio)
        if(abs(wristPoint[0]) > largestX):
            largestX = abs(wristPoint[0])
        gripperWristPoint = self.controller.armJoints[3].findOffsetPoint(wristPoint, self.controller.armJoints[3].offset, self.controller.servoInfo[3][0], sizeRatio)
        if(abs(gripperWristPoint[0]) > largestX):
            largestX = abs(gripperWristPoint[0])
        gripperTipPoint = self.controller.armJoints[3].findEndXYandApproach(wristPoint, self.controller.servoInfo[3][0], sizeRatio)
        if(abs(gripperTipPoint[0]) > largestX):
            largestX = abs(gripperTipPoint[0])
        
        baseAngle = -(self.controller.armJoints[0].microsToAngle(self.controller.servoInfo[0][0])) # + math.pi
        
                
        baseCoords = self.toCanvasCoords(basePoint, sizeRatio)
        shoulderCoords = self.toCanvasCoords(shoulderPoint, sizeRatio)
        elbowCoords = self.toCanvasCoords(elbowPoint, sizeRatio)
        wristCoords = self.toCanvasCoords(wristPoint, sizeRatio)
        gripperWristCoords = self.toCanvasCoords(gripperWristPoint, sizeRatio)
        gripperTipCoords = self.toCanvasCoords(gripperTipPoint, sizeRatio)       
        
        self.canvas.delete("all")
        
        self.squareCanvas()
        self.drawSegment(baseCoords, shoulderCoords, "white")
        self.drawSegment(shoulderCoords, elbowCoords, "cyan")
        self.drawSegment(elbowCoords, wristCoords, "red")
        self.drawSegment(wristCoords, gripperWristCoords, "white")
        self.drawSegment(gripperWristCoords, gripperTipCoords, "green")
        
        self.canvas.create_oval(200, 150, 250, 200, outline="white", width=2)
        self.canvas.create_oval(224, 174, 226, 176, outline="white", width=2)        
        circleRatio = 25.0 / (totalHeightPossible - self.controller.armJoints[0].length)
        
        segmentLength = largestX * circleRatio
        
        armLengthSegX = (segmentLength * (math.cos(baseAngle))) + 225
        armLengthSegY = (segmentLength * (math.sin(baseAngle))) + 175
        
        self.drawSegment((225 , 175), (armLengthSegX, armLengthSegY), "magenta")
        
        ####  GIMBAL SECTION ###
        
        gimbalPanAngle = baseAngle + ((self.controller.armJoints[6].microsToAngle(self.controller.servoInfo[6][0])) - (math.pi/2))
        gimbalTiltAngle = gripperWristPoint[2] + ((self.controller.armJoints[7].microsToAngle(self.controller.servoInfo[7][0])) - (math.pi/2))
        
        panSegLength = 25
        
        panX = (panSegLength * (math.cos(gimbalPanAngle))) + 225
        panY = (panSegLength * (math.sin(gimbalPanAngle))) + 175
        
        self.drawSegment((armLengthSegX , armLengthSegY), (panX, panY), "cyan")
        
        gimbalOffsetPoint = self.controller.armJoints[3].findOffsetPoint(wristPoint, self.controller.armJoints[7].offset, self.controller.servoInfo[3][0], sizeRatio)
        gimbalOffsetCoords = self.toCanvasCoords(gimbalOffsetPoint, sizeRatio)
        
        self.drawSegment(wristCoords, gimbalOffsetCoords, "white")
        
        tiltX = ((panSegLength) * (math.cos(gimbalTiltAngle))) + gimbalOffsetCoords[0]
        tiltY = ((panSegLength) * (-math.sin(gimbalTiltAngle))) + gimbalOffsetCoords[1]
        
#         tiltCoords = self.toCanvasCoords((tiltX, tiltY), sizeRatio)
        tiltCoords = (tiltX, tiltY)
        
        self.drawSegment(gimbalOffsetCoords, tiltCoords, "cyan")
        
        
        #####   Draw Drive Angle indicator      
        
        
        ls = self.controller.getProperty('leftMotorSpeed')
        rs = self.controller.getProperty('rightMotorSpeed')
        diameter = 50
        circleColor = "white"
        fill=None
        circleOffset = 5
        if (ls == 0) and (rs == 0):
            circleColor = None
            fill="red"
        else:  
            self.calculateDriveAngle()
            
            x = ((diameter / 2) * math.cos(self.driveAngle)) + (diameter / 2)
            y = ((diameter / 2) * math.sin(self.driveAngle)) + (diameter / 2)
            
            
            
            self.canvas.create_line(((diameter / 2)+circleOffset), ((self.canvasHeight-(diameter / 2))-circleOffset), (x+circleOffset), (self.canvasHeight - y)-circleOffset, width=2, fill=self.driveLineColor)
        
        self.canvas.create_oval(circleOffset, (self.canvasHeight - diameter)-circleOffset, diameter+circleOffset, self.canvasHeight-circleOffset, outline=circleColor, width=2, fill=fill, stipple='gray50')
        
        
        
        return 
            
        
    
        
    def calculateDriveAngle(self):
        ###  See the controller functions for RobotMainBrain
        ###  in the driveWithOneStick function to understand
        ###  how this works.  I'm going to calculate an angle
        ###  and rotate it 45 degrees ccw to get back to the 
        ###  stick position
        ###  But we gotta rotate the other way so the axes reverse
        ###  Just draw a damn picture if you don't get it
        ###  left motor is on x axis and right motor on y 
        ls = self.controller.getProperty('leftMotorSpeed') * 1.0
        rs = self.controller.getProperty('rightMotorSpeed') * 1.0
        self.driveAngle = math.pi / 4.0
        if(ls == 0):
            if(rs > 0):
                self.driveAngle = math.pi / 2.0
            elif(rs<0):
                self.driveAngle = 3*math.pi/2.0
                
        else:
            self.driveAngle = math.atan(rs/ls)
        self.driveAngle = self.driveAngle + (math.pi / 4.0)
        
        if(ls<0):
            self.driveAngle = self.driveAngle + (math.pi)
        
        if(self.driveAngle < 0):
            self.driveAngle = self.driveAngle + (2 * math.pi)
        
        if(self.driveAngle > math.pi):
            self.driveAngle = (3*math.pi) - self.driveAngle
            self.driveLineColor = "red"
        else:
            self.driveLineColor = "white"
        
        return self.driveAngle
    
    
    
    
    
    
    
    
    
    
    
    
    
    ##############
        
    