

import Tkinter as tk

class ArmGraphicFrame(tk.Frame):
    
    def __init__ (self, aParent, aController):
        
        self.parent = aParent
        tk.Frame.__init__(self, self.parent)
        self.controller = aController
        
        self.canvas = tk.Canvas(self, width=100, height=100)
        
        self.canvas.pack()
        
        self.canvas.create_line(1,1,1,99)
        self.canvas.create_line(1,99,99,99)
        self.canvas.create_line(99,99,99,1)
        self.canvas.create_line(99,1,1,1)
        
        
        
        self.canvas.create_line(25, 25, 75, 95)
     
    def squareCanvas(self):
        self.canvas.create_line(1,1,1,99)
        self.canvas.create_line(1,99,99,99)
        self.canvas.create_line(99,99,99,1)
        self.canvas.create_line(99,1,1,1)
        return
           
        
    def toCanvasCoords(self, aXYAtuple, aRatio):
        reX = aXYAtuple[0]
        reY = (100 - aXYAtuple[1])
        
        return (reX, reY)
        
    
    def drawSegment(self, aXYtuple1, aXYtuple2, aColor):
        
        self.canvas.create_line(aXYtuple1[0], aXYtuple1[1], aXYtuple2[0], aXYtuple2[1], width=2, fill=aColor)
        return
    
    
    ###  Draw arm with base at x,y of this tuple 
    def drawArm(self):
        
        aXYAtuple = (50, 20, 1.5708)
        
        totalHeightPossible = self.controller.armJoints[0].length + self.controller.armJoints[1].length + self.controller.armJoints[2].length + self.controller.armJoints[3].length
        
        guiHeight = 100 - aXYAtuple[1]
        
        sizeRatio = 1.0 * guiHeight / (2.0 * totalHeightPossible)
        
        basePoint = (aXYAtuple[0], aXYAtuple[1], 1.5708)
        shoulderPoint = (aXYAtuple[0], (aXYAtuple[1] + (self.controller.armJoints[0].length * sizeRatio)), 1.5708)        
        elbowPoint = self.controller.armJoints[1].findEndXYandApproach(shoulderPoint, self.controller.servoInfo[1][0], sizeRatio)
        wristPoint = self.controller.armJoints[2].findEndXYandApproach(elbowPoint, self.controller.servoInfo[2][0], sizeRatio)
        gripperTipPoint = self.controller.armJoints[3].findEndXYandApproach(wristPoint, self.controller.servoInfo[3][0], sizeRatio)
        
        
        
        
        baseCoords = self.toCanvasCoords(basePoint, sizeRatio)
        shoulderCoords = self.toCanvasCoords(shoulderPoint, sizeRatio)
        elbowCoords = self.toCanvasCoords(elbowPoint, sizeRatio)
        wristCoords = self.toCanvasCoords(wristPoint, sizeRatio)
        gripperTipCoords = self.toCanvasCoords(gripperTipPoint, sizeRatio)       
        
        self.canvas.delete("all")
        
        self.squareCanvas()
        self.drawSegment(baseCoords, shoulderCoords, "black")
        self.drawSegment(shoulderCoords, elbowCoords, "red")
        self.drawSegment(elbowCoords, wristCoords, "blue")
        self.drawSegment(wristCoords, gripperTipCoords, "green")
        
        
        return 
            
        
        
        
    