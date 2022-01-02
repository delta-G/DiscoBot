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

import SharedDiscoBot

class Gauge(tk.Frame):
    
    def __init__(self, aParent, aController, aLabel, aKeyword, aWidth = 50, aHeight = 15, aMinval=0.0, aMaxval=20.0, aLowRed=3.0, aLowYellow=6.0, aHighYellow=14.0, aHighRed=17.0):
        self.parent = aParent
        self.controller = aController
        self.label = aLabel
        self.keyword = aKeyword
        self.width = aWidth
        self.height = aHeight
        self.minVal = aMinval
        self.maxVal = aMaxval
        self.lowRed = aLowRed
        self.lowYellow = aLowYellow
        self.highYellow = aHighYellow
        self.highRed = aHighRed
        
        if self.highRed > self.maxVal:
            self.highRed = self.maxVal
        if self.highYellow > self.highRed:
            self.highYellow = self.highRed
        if self.lowRed < self.minVal:
            self.lowRed = self.minVal
        if self.lowYellow < self.lowRed:
            self.lowYellow = self.lowRed
            
        self.litStipple = None
        self.unlitStipple = 'gray25'
        
        
        tk.Frame.__init__(self, self.parent, **SharedDiscoBot.highlightFrameConfig)        
        
        self.nameLabel = tk.Label(self, text=aLabel, width=7, anchor=tk.W, **SharedDiscoBot.labelConfig)
        self.nameLabel.pack(side=tk.LEFT, anchor=tk.W)
        self.nameLabel.update()
        self.height = self.nameLabel.winfo_reqheight()
        self.gaugeCanvas = tk.Canvas(self, width=self.width, height=self.height, **SharedDiscoBot.canvasConfig)
        
        
        
        self.gaugeCanvas.pack(side=tk.LEFT, anchor=tk.W)
        
        return 
    
    def refresh(self):
        self.gaugeCanvas.delete('all')
        level = self.controller.getProperty(self.keyword)
        if level < self.minVal:
            level = self.minVal
        if level > self.maxVal:
            level = self.maxVal
            
        fillPercent = (level - self.minVal)/(self.maxVal - self.minVal)
        fillLine = self.width * fillPercent
        lowRedLine = self.width * ((self.lowRed - self.minVal)/(self.maxVal - self.minVal))
        lowYellowLine = self.width * ((self.lowYellow - self.minVal)/(self.maxVal - self.minVal))
        highYellowLine = self.width * ((self.highYellow - self.minVal)/(self.maxVal - self.minVal))
        highRedLine = self.width * ((self.highRed - self.minVal)/(self.maxVal - self.minVal))
        
        if self.lowRed > self.minVal:
            self.drawBlock(fillLine, 0, lowRedLine, 'red')
        if self.lowYellow >self.lowRed:
            self.drawBlock(fillLine, lowRedLine, lowYellowLine, 'yellow')
        self.drawBlock(fillLine, lowYellowLine, highYellowLine, 'green')
        if self.highYellow < self.highRed:
            self.drawBlock(fillLine, highYellowLine, highRedLine, 'yellow')
        if self.highRed < self.maxVal:
            self.drawBlock(fillLine, highRedLine, self.width, 'red')            
        
#         fillBlock = self.gaugeCanvas.create_rectangle(0,2,fillLine,self.height-2, fill='green', stipple='gray50')
        self.gaugeCanvas.create_text(0,self.height / 2, text='{0:>02.1f}'.format(self.controller.getProperty(self.keyword)), anchor = tk.W, fill='black')                
        
        return
    
    def drawBlock(self, fillLine, minLine, maxLine, color):
        
        if fillLine < minLine:
            ## draw whole thing stippled
            self.gaugeCanvas.create_rectangle(minLine,2,maxLine,self.height-2, fill=color, stipple=self.unlitStipple)
        elif fillLine > maxLine:
            ## draw whole thing solid
            self.gaugeCanvas.create_rectangle(minLine,2,maxLine,self.height-2, fill=color, stipple=self.litStipple)
        else:
            self.gaugeCanvas.create_rectangle(minLine,2,fillLine,self.height-2, fill=color, stipple=self.litStipple)
            self.gaugeCanvas.create_rectangle(fillLine,2,maxLine,self.height-2, fill=color, stipple=self.unlitStipple)            
        return 
    
    
    
    


