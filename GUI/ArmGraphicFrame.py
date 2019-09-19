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

class ArmGraphicFrame(tk.Frame):
    
    def __init__ (self, aParent, aController):
        
        self.parent = aParent
        tk.Frame.__init__(self, self.parent)
        self.controller = aController
        
        self.canvasWidth = 250
        self.canvasHeight = 200
        
        self.canvas = tk.Canvas(self, width=self.canvasWidth, height=self.canvasHeight)
        
        self.canvas.pack()    
        
     
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
        
        basePoint = (aXYAtuple[0], aXYAtuple[1], 1.5708)
        shoulderPoint = (aXYAtuple[0], (aXYAtuple[1] + (self.controller.armJoints[0].length * sizeRatio)), 1.5708)        
        elbowPoint = self.controller.armJoints[1].findEndXYandApproach(shoulderPoint, self.controller.servoInfo[1][0], sizeRatio)
        wristPoint = self.controller.armJoints[2].findEndXYandApproach(elbowPoint, self.controller.servoInfo[2][0], sizeRatio)
        gripperWristPoint = self.controller.armJoints[3].findOffsetPoint(wristPoint, self.controller.servoInfo[3][0], sizeRatio)
        gripperTipPoint = self.controller.armJoints[3].findEndXYandApproach(wristPoint, self.controller.servoInfo[3][0], sizeRatio)
        
        
        
        
        baseCoords = self.toCanvasCoords(basePoint, sizeRatio)
        shoulderCoords = self.toCanvasCoords(shoulderPoint, sizeRatio)
        elbowCoords = self.toCanvasCoords(elbowPoint, sizeRatio)
        wristCoords = self.toCanvasCoords(wristPoint, sizeRatio)
        gripperWristCoords = self.toCanvasCoords(gripperWristPoint, sizeRatio)
        gripperTipCoords = self.toCanvasCoords(gripperTipPoint, sizeRatio)       
        
        self.canvas.delete("all")
        
        self.squareCanvas()
        self.drawSegment(baseCoords, shoulderCoords, "black")
        self.drawSegment(shoulderCoords, elbowCoords, "cyan")
        self.drawSegment(elbowCoords, wristCoords, "red")
        self.drawSegment(wristCoords, gripperWristCoords, "black")
        self.drawSegment(gripperWristCoords, gripperTipCoords, "green")
        
        
        return 
            
        
        
        
    