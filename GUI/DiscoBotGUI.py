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

import ServoPane
import TermFrame
import IndicatorFrame
import SelectFrame

import ArmGraphicFrame

class DiscoBotGUI(tk.Frame):
    
    def __init__(self, aParent, aController):
        
        self.parent = aParent
        tk.Frame.__init__(self, self.parent)
        self.controller = aController
        
        self.parent.config(padx=10, pady=10)
        
        self.colors = {
            'red' : '#FF0000',
            'green' : '#00FF00',
            'yellow' : '#FFFF00'
            }
        
        self.defaultFont = "Veranda 12 bold"
        
        self.leftSideFrame = tk.Frame(self)
        self.rightSideFrame = tk.Frame(self)
        
                
        self.topFrame = tk.Frame(self.leftSideFrame)
        
        self.indicatorFrame = IndicatorFrame.IndicatorFrame(self.topFrame, self, self.controller)
        
        self.selectFrame = SelectFrame.SelectFrame(self.topFrame, self.controller)        
        
        self.armGraphicFrame = ArmGraphicFrame.ArmGraphicFrame(self.rightSideFrame, self.controller)
        
        self.termFrame = TermFrame.TermFrame(self.leftSideFrame, self, self.controller) 
        self.servoPane = ServoPane.ServoPane(self.rightSideFrame, self, self.controller.armJoints)  
        
        #topFrame (part of leftSideFrame)
        self.indicatorFrame.pack(side=tk.LEFT, anchor=tk.W)
        self.selectFrame.pack(side=tk.LEFT)
        
        
        #leftSideFrame
        self.topFrame.pack(side=tk.TOP, anchor=tk.W)
        
        self.termFrame.pack(side=tk.LEFT)
        
        #rightSideFrame
        self.armGraphicFrame.pack(side=tk.TOP, anchor=tk.N)        
        self.servoPane.pack(side=tk.TOP)
        
        self.leftSideFrame.pack(side=tk.LEFT, anchor=tk.N)
        self.rightSideFrame.pack(side=tk.LEFT, anchor=tk.N)     
                
        self.pack()
        return
    
    
    def refresh(self):
        self.servoPane.updateData()
        self.indicatorFrame.check()
        self.armGraphicFrame.drawArm()
        self.selectFrame.update()
        if(self.controller.joyConnected):
            self.indicatorFrame.controllerConnectButton.config(bg=self.colors['green'])
        else:            
            self.indicatorFrame.controllerConnectButton.config(bg=self.colors['red'])
                
        if(self.controller.commsOn):
            self.indicatorFrame.comConnectButton.config(bg=self.colors['green'])
        else:            
            self.indicatorFrame.comConnectButton.config(bg=self.colors['red'])        
        return


