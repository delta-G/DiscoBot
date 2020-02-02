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

class SonarGraphicFrame(tk.Frame):
    
    def __init__ (self, aParent, aController):
        
        self.parent = aParent
        tk.Frame.__init__(self, self.parent)
        self.controller = aController
        
        self.canvasWidth = 250
        self.canvasHeight = 200
        
        self.canvas = tk.Canvas(self, width=self.canvasWidth, height=self.canvasHeight)
        
        self.canvas.pack() 
        
        self.originPoint = ((self.canvasWidth/2), 20)
        
        self.scale = 3000.0/(self.canvasWidth/2) # mm range / pixel
        
        return 
    
    def createArc(self, aDist, aColor):
        
        scaled = aDist / self.scale        
        
        self.canvas.create_arc(self.originPoint[0]-scaled, (self.canvasHeight - self.originPoint[1]) - scaled, self.originPoint[0]+scaled, (self.canvasHeight - self.originPoint[1]) + scaled,start=0, extent=180, fill=aColor)
        
        return 
    
    def squareCanvas(self):
        w = (self.canvasWidth - 1)
        h = (self.canvasHeight - 1)
        self.canvas.create_line(1,1,1,h)
        self.canvas.create_line(1,h,w,h)
        self.canvas.create_line(w,h,w,1)
        self.canvas.create_line(w,1,1,1)
        
        d = [2500, 2000, 1500, 1000, 750, 500, 250]
        c = ["purple", "blue", "cyan", "green", "yellow", "orange", "red"]
        
        for i in range(7):
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
        self.drawSegment((xy[0] - aSize, xy[1] - aSize), (xy[0] + aSize, xy[1] + aSize), "black")
        self.drawSegment((xy[0] - aSize, xy[1] + aSize), (xy[0] + aSize, xy[1] - aSize), "black")
        
        return 
    
    def display(self, aList):
        
        self.canvas.delete("all")
        self.squareCanvas()
        
#         self.displayPoint(self.originPoint, 5)
        self.drawSegment(self.toCanvasCoords(self.originPoint),self.toCanvasCoords((self.originPoint[0], self.originPoint[1] - 20)),"black")
        self.drawSegment(self.toCanvasCoords(self.originPoint),self.toCanvasCoords((self.originPoint[0]-5, self.originPoint[1] - 5)),"black")
        self.drawSegment(self.toCanvasCoords(self.originPoint),self.toCanvasCoords((self.originPoint[0]+5, self.originPoint[1] - 5)),"black")        
        
        
        for i in range(13):
            
            ang = (i/12.0)*math.pi
            dist = aList[i] / self.scale
            
            point = self.solveTriangle(dist, ang)
            
            point = ((point[0] + self.originPoint[0]) , (point[1] + self.originPoint[1]))
            
            self.displayPoint(point, 2)
            
        return
            
    
    
    
    
    
    
    
        
        ####END
