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


import Tkinter as tk
import math
import ArmCalWindow
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
        
        self.canvas.pack()   
        self.canvas.bind("<Double-Button-1>", self.launchCalibrationWindow)
        return 
    
    def launchCalibrationWindow(self, event):
        
        if not self.gui.calibrationWindowActive:
            self.gui.calibrationWindowActive = True
            armCalWindow = ArmCalWindow.ArmCalibrationWindowClass(self.gui, self.controller)
            
        
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
        
        
        
        return 
            
        
    
        
    