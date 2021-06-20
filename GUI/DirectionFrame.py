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


class DirectionFrame(tk.Frame):
    
    def __init__(self, aParent, aController):
        
        self.parent = aParent
        tk.Frame.__init__(self, self.parent, **SharedDiscoBot.frameConfig)
        self.controller = aController
        
        self.angle = 0.0
        self.lineColor = "white"
        
        self.canvasWidth = 50
        self.canvasHeight = 50
        
        
        
        self.canvasFrame = tk.Frame(self, padx=20, **SharedDiscoBot.frameConfig)
        
        self.canvas = tk.Canvas(self.canvasFrame, width=self.canvasWidth, height=self.canvasHeight, **SharedDiscoBot.canvasConfig)
        self.canvas.config(highlightthickness=0)
        self.canvas.pack()
        
        
        self.canvasFrame.pack()       
        
        
        return 
    
    
    def calculateAngle(self):
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
        self.angle = math.pi / 4.0
        if(ls == 0):
            if(rs > 0):
                self.angle = math.pi / 2.0
            elif(rs<0):
                self.angle = 3*math.pi/2.0
                
        else:
            self.angle = math.atan(rs/ls)
        self.angle = self.angle + (math.pi / 4.0)
        
        if(ls<0):
            self.angle = self.angle + (math.pi)
        
        if(self.angle < 0):
            self.angle = self.angle + (2 * math.pi)
        
        if(self.angle > math.pi):
            self.angle = (3*math.pi) - self.angle
            self.lineColor = "red"
        else:
            self.lineColor = "white"
        
        return self.angle
    
    
    
    def display(self):
        
        self.canvas.delete("all")
        
        ls = self.controller.getProperty('leftMotorSpeed')
        rs = self.controller.getProperty('rightMotorSpeed')
        self.diameter = 50
        circleColor = "white"
        fill=None
        if (ls == 0) or (rs == 0):
            circleColor = "red"
            fill="red"
        else:  
            self.calculateAngle()
            
            x = ((self.diameter / 2) * math.cos(self.angle)) + (self.diameter / 2)
            y = ((self.diameter / 2) * math.sin(self.angle)) + (self.diameter / 2)
            
            self.canvas.create_line((self.diameter / 2), (self.diameter / 2), x, self.canvasHeight - y, width=2, fill=self.lineColor)
        
        self.canvas.create_oval(0, 0, self.diameter, self.diameter, outline=circleColor, width=2, fill=fill)
        
        
        
        return
        
        
    
    