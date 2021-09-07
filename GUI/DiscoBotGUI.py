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

import SharedDiscoBot

import tkinter as tk

import GUI.ServoPane
import GUI.TermFrame
import GUI.IndicatorFrame
import GUI.SelectFrame
import GUI.DirectionFrame
import GUI.VoltageFrame
import GUI.VideoWindow

import GUI.ArmGraphicFrame
import GUI.SonarGraphicFrame

class DiscoBotGUI(tk.Frame):
    
    def __init__(self, aParent, aController):
        
        self.parent = aParent
        tk.Frame.__init__(self, self.parent, **SharedDiscoBot.highlightFrameConfig)
        self.controller = aController
        self.videoOpen = False
        
        self.calibrationWindowActive = False
        
        self.parent.configure(background='black')
        
        
        self.parent.config(padx=5, pady=5)
        
        self.leftSideFrame = tk.Frame(self, **SharedDiscoBot.frameConfig)
        self.rightSideFrame = tk.Frame(self, **SharedDiscoBot.frameConfig)
        
                
        self.topFrame = tk.Frame(self.leftSideFrame, **SharedDiscoBot.frameConfig)
        
        self.indicatorFrame = GUI.IndicatorFrame.IndicatorFrame(self.topFrame, self, self.controller)
        
        self.selectFrame = GUI.SelectFrame.SelectFrame(self.topFrame, self.controller)  
        
        self.voltageFrame = GUI.VoltageFrame.VoltageFrame(self.topFrame, self.controller)      
        
        self.armGraphicFrame = GUI.ArmGraphicFrame.ArmGraphicFrame(self.rightSideFrame, self.controller, self)
        self.sonarGraphicFrame = GUI.SonarGraphicFrame.SonarGraphicFrame(self.leftSideFrame, self.controller)
        self.directionFrame = GUI.DirectionFrame.DirectionFrame(self.sonarGraphicFrame, self.controller)
        
        self.videoButton = tk.Button(self.sonarGraphicFrame, text="Video", width=5, command=self.launchVideo)
        
        self.termFrame = GUI.TermFrame.TermFrame(self.leftSideFrame, self, self.controller) 
        self.servoPane = GUI.ServoPane.ServoPane(self.rightSideFrame, self, self.controller.armJoints)  
        
        #topFrame (part of leftSideFrame)
        self.indicatorFrame.pack(side=tk.LEFT, anchor=tk.NW)
        self.selectFrame.pack(side=tk.LEFT, anchor=tk.N)
        self.voltageFrame.pack(side=tk.LEFT, anchor=tk.N)
        
        self.directionFrame.pack(side=tk.LEFT)
        self.videoButton.pack(side=tk.LEFT)
        
        
        #leftSideFrame
        self.topFrame.pack(side=tk.TOP, anchor=tk.W)
        
        self.sonarGraphicFrame.pack(side=tk.TOP, anchor=tk.W) 
        
        self.termFrame.pack(side=tk.TOP)
        
        
        
        #rightSideFrame    
        
        self.armGraphicFrame.pack(side=tk.TOP, anchor=tk.N) 
        self.servoPane.pack(side=tk.TOP)
        
        self.leftSideFrame.pack(side=tk.LEFT, anchor=tk.N)
        self.rightSideFrame.pack(side=tk.LEFT, anchor=tk.N)     
                
        self.pack()
        
        self.controller.setRedirect(self.termFrame.redirect)
        
        return
    
    def getController(self):
        return self.controller
    
    def refresh(self):
        self.servoPane.updateData()
        self.indicatorFrame.check()
        self.armGraphicFrame.refresh()
        self.sonarGraphicFrame.refresh()
        self.directionFrame.display()
        self.selectFrame.refresh()
        self.voltageFrame.refresh()
        
        self.termFrame.controllerLabel.config(text=self.controller.getProperty('lastController'));
        if(self.controller.joy is not None and self.controller.joy.connected()):
#             self.termFrame.controllerLabel2.config(text=self.controller.joy.reading[0:42])
            self.termFrame.controllerLabel.config(fg=SharedDiscoBot.colors['green'])
        else:
            self.termFrame.controllerLabel.config(fg=SharedDiscoBot.colors['red'])            
        
        if self.videoOpen:
            self.vidWindow.refresh()
                
        self.indicatorFrame.comConnectButton.config(bg=self.controller.comms.getIndicatorState())      
        return
    
    def launchVideo(self):
        
        if not self.videoOpen:
            self.videoOpen = True
            self.vidWindow = GUI.VideoWindow.VideoWindow(self, self.controller, 0)
            return


