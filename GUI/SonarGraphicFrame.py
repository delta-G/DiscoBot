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

import SharedDiscoBot

class SonarGraphicFrame(tk.Frame):
    
    def __init__ (self, aParent, aController):
        
        self.parent = aParent
        tk.Frame.__init__(self, self.parent, **SharedDiscoBot.frameConfig)
        self.controller = aController
        
        self.zoom = False
        self.range = 3000.0
        self.scanning = False
        
        self.canvasWidth = 250
        self.canvasHeight = 150
        
        self.buttonFrame = tk.Frame(self, **SharedDiscoBot.frameConfig)
        self.canvasFrame = tk.Frame(self, padx=20, **SharedDiscoBot.frameConfig)
        
        self.canvas = tk.Canvas(self.canvasFrame, width=self.canvasWidth, height=self.canvasHeight, **SharedDiscoBot.canvasConfig)
        self.canvas.pack()
        
        
        
        self.zoomButton = tk.Button(self.buttonFrame, width=10, height=1, text="Zoom", command=self.toggleZoom, **SharedDiscoBot.buttonConfig)
        self.scanButton = tk.Button(self.buttonFrame, width=10, height=1, text="Scan", command=self.toggleScan, **SharedDiscoBot.buttonConfig)
        self.singleButton = tk.Button(self.buttonFrame, width=10, height=1, text="Single", command=self.singleScan, **SharedDiscoBot.buttonConfig)
        self.zoomButton.pack(side=tk.TOP)
        self.scanButton.pack(side=tk.TOP)
        self.singleButton.pack(side=tk.TOP)
        
        
        self.buttonFrame.pack(side=tk.LEFT, anchor=tk.W)
        self.canvasFrame.pack(side=tk.LEFT) 
        
        
        self.originPoint = ((self.canvasWidth/2), 20)
        
        self.scale = 3000.0/(self.canvasWidth/2) # mm range / pixel
        
        
        
        return 
    
    def toggleZoom(self):        
        self.zoom = not self.zoom
        if(self.zoom == True):
            self.range = 1000.0
        else:
            self.range = 3000.0
        return
    
    def toggleScan(self):
        self.scanning = not self.scanning
        if(self.scanning == True):
            self.controller.outPutRunner("<U,C>")
        else:            
            self.controller.outPutRunner("<U,C0>")
        return        
    
    def singleScan(self):
        self.controller.outPutRunner("<U,W>")
        return
    
    
    def createArc(self, aDist, aColor, fill=None):
        
        scaled = aDist / self.scale        
        style = tk.CHORD
        if(fill == None):
            style = tk.ARC
        
        self.canvas.create_arc(self.originPoint[0]-scaled, (self.canvasHeight - self.originPoint[1]) - scaled, self.originPoint[0]+scaled, (self.canvasHeight - self.originPoint[1]) + scaled,start=0, extent=180, outline=aColor, fill=fill, style=style)
        
        return 
    
    def squareCanvas(self):
#         w = (self.canvasWidth - 1)
#         h = (self.canvasHeight - 1)
#         self.canvas.create_line(1,1,1,h)
#         self.canvas.create_line(1,h,w,h)
#         self.canvas.create_line(w,h,w,1)
#         self.canvas.create_line(w,1,1,1)
        
        d = [3000, 2500, 2000, 1500, 1000, 750, 500, 250]
        c = ["white", "purple", "blue", "cyan", "green", "yellow", "orange", "red"]
        
        self.createArc(self.range, "black", fill="black")        
        for i in range(len(d)):
            self.createArc(d[i],c[i])       
        return
    
    
    def toCanvasCoords(self, aXYAtuple):
        reX = aXYAtuple[0]
        reY = (self.canvasHeight - aXYAtuple[1])
        
        return (reX, reY)
    
    
    def drawSegment(self, aXYtuple1, aXYtuple2, aColor):
        
        self.canvas.create_line(aXYtuple1[0], aXYtuple1[1], aXYtuple2[0], aXYtuple2[1], width=2, fill=aColor)
        return

    
    ###  Need to take in distance and Angle and spit out 
    ###  X and Y coords of the point on the canvas.
    
    def solveTriangle(self, aDist, aAng):
        
        reX = aDist * math.cos(aAng)
        reY = aDist * math.sin(aAng)
           
        return (reX , reY)
    
    def displayPoint(self, aXYtuple, aSize):
        xy = self.toCanvasCoords(aXYtuple)
        self.drawSegment((xy[0] - aSize, xy[1] - aSize), (xy[0] + aSize, xy[1] + aSize), "white")
        self.drawSegment((xy[0] - aSize, xy[1] + aSize), (xy[0] + aSize, xy[1] - aSize), "white")
        
        return 
    
    def display(self, aList):
        
        self.canvas.delete("all")
        self.scale = self.range/(self.canvasWidth/2) # mm range / pixel
        self.squareCanvas()
        
#         ###  Draw an arrow to mark where the sensor is
#         self.drawSegment(self.toCanvasCoords(self.originPoint),self.toCanvasCoords((self.originPoint[0], self.originPoint[1] - 20)),"red")
#         self.drawSegment(self.toCanvasCoords(self.originPoint),self.toCanvasCoords((self.originPoint[0]-5, self.originPoint[1] - 5)),"red")
#         self.drawSegment(self.toCanvasCoords(self.originPoint),self.toCanvasCoords((self.originPoint[0]+5, self.originPoint[1] - 5)),"red")        
        
        
        for i in range(13):
            
            ang = (i/12.0)*math.pi
            dist = aList[i]
            
            if(dist < self.range):
                point = self.solveTriangle((dist / self.scale), ang)
            
                point = ((point[0] + self.originPoint[0]) , (point[1] + self.originPoint[1]))
            
                self.displayPoint(point, 2)
            
        return
    
    def refresh(self):
        
        self.display(self.controller.sonarList)
        pointerTip = self.solveTriangle(3000 / self.scale, self.controller.getProperty('sonarPanAngle'))
        pointerTipOnCanvas = self.toCanvasCoords(((pointerTip[0] + self.originPoint[0]), (pointerTip[1]+self.originPoint[1])))
        self.drawSegment(self.toCanvasCoords(self.originPoint),pointerTipOnCanvas,"white")
        
        return
            
    
    
    
    
    
    
    
        
        ####END
