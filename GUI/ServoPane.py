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


class ServoPane(tk.Frame):
    
    
    def __init__(self, aParent, aGui, jointList):
        
        self.parent = aParent
        tk.Frame.__init__(self, self.parent, padx=5, pady=5)
        
        self.gui = aGui
        
        self.labels = []
        
        count = 0
        
        for joint in jointList:
            tmp = OneServo(self, self.gui, joint.name, count)
            self.labels.append(tmp)
            tmp.pack()       
            count += 1 
        
        return
    
    def updateData(self):
        
        for l in self.labels:
            l.updateData()        
        return
    

class OneServo(tk.Frame):
    
    def __init__(self, aParent, aGui, aName, aNum):
        
        self.number = aNum
        self.parent = aParent
        tk.Frame.__init__(self, self.parent, bd=1, relief=tk.SUNKEN)
        
        self.gui = aGui
                
        self.servoLabel = tk.Label(self, text=str(aName)+' -- ', pady=5, width=12, font="Verdana 12")
        self.positionLabel = tk.Label(self, text=str(1500), pady=5, width=5, font="Verdana 12 bold")
        self.speedLabel = tk.Label(self, text=str(100), pady=5, width=5, font="Verdana 12 bold")
        self.targetLabel = tk.Label(self, text=str(1500), pady=5, width=5, font="Verdana 12 bold")
        self.servoLabel.pack(side=tk.LEFT)
        self.positionLabel.pack(side=tk.LEFT)
        self.speedLabel.pack(side=tk.LEFT)     
        self.targetLabel.pack(side=tk.LEFT)  
        
        return
    
    
    def updateData(self):
        self.positionLabel.config(text=str(self.gui.controller.servoInfo[self.number][0]))
        self.speedLabel.config(text=str(self.gui.controller.servoInfo[self.number][1]))
        self.targetLabel.config(text=str(self.gui.controller.servoInfo[self.number][2]))
        
        return
    
    
    
    
    
    
    
    



