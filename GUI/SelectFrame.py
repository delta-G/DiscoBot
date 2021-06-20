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
import sys
import glob
import serial

import SharedDiscoBot
import GUI.CommandCheckButton

class SelectFrame(tk.Frame):

            
    def getPortList(self):
        self.portList = glob.glob('/dev/tty[AU]*')
        self.portList.append("---Check---")
        self.comPortSpinbox.config(values=self.portList)
        return
    
    def clearPortList(self):
        self.portList = ["---Check---"]        
        self.comPortSpinbox.config(values=self.portList)
        return
    
    
    def __init__(self, aParent, aController):
        
        self.parent = aParent
        self.controller = aController
        tk.Frame.__init__(self, self.parent, **SharedDiscoBot.frameConfig)
        
        self.checkFrame = tk.Frame(self, **SharedDiscoBot.frameConfig)
        self.checkFrame.pack(side=tk.TOP)
        
        
        self.leftFrame = tk.Frame(self.checkFrame, **SharedDiscoBot.frameConfig)
        self.leftFrame.pack(side=tk.LEFT)
        
        self.rightFrame = tk.Frame(self.checkFrame, **SharedDiscoBot.frameConfig)
        self.rightFrame.pack(side=tk.LEFT)
        
        self.camPowCheck = GUI.CommandCheckButton.CommandCheckButton(self.leftFrame, self.controller, "Camera", 'cameraPower', "<V0>", "<V1>")
        self.headPowCheck = GUI.CommandCheckButton.CommandCheckButton(self.leftFrame, self.controller, "Lights", 'headlightPower', "<H0>", "<H1>")
        self.armPowCheck = GUI.CommandCheckButton.CommandCheckButton(self.leftFrame, self.controller, "Arm-CPU", 'armPower', "<QA0>", "<QA1>")
        self.comPowCheck = GUI.CommandCheckButton.CommandCheckButton(self.leftFrame, self.controller, "Com-CPU", 'comPower', "<QR0>", "<QR1>")
        self.armServoPowCheck = GUI.CommandCheckButton.CommandCheckButton(self.leftFrame, self.controller, "Arm-Servo", 'armServoPower', "<A,Cp>", "<A,CP>")
        
        self.motorPowCheck = GUI.CommandCheckButton.CommandCheckButton(self.rightFrame, self.controller, "Motors", 'motorPower', "<QM0>", "<QM1>")
        self.motorContEnableCheck = GUI.CommandCheckButton.CommandCheckButton(self.rightFrame, self.controller, "Motor-En", 'motorContEnable', "<Qm0>", "<Qm1>")
        self.v12PowCheck = GUI.CommandCheckButton.CommandCheckButton(self.rightFrame, self.controller, "12-Volt", 'v12Power', "<QV0>", "<QV1>")
        self.auxPowCheck = GUI.CommandCheckButton.CommandCheckButton(self.rightFrame, self.controller, "Aux", 'auxPower', "<Qa0>", "<Qa1>")
        self.sonarPowCheck = GUI.CommandCheckButton.CommandCheckButton(self.rightFrame, self.controller, "Sonar", 'sonarPower', "<QS0>", "<QS1>")
        
        
        
        self.modeFrame = tk.Frame(self, **SharedDiscoBot.frameConfig)
        
        self.comPortSpinbox = tk.Spinbox(self.modeFrame, width=13, **SharedDiscoBot.spinboxConfig)
        self.getPortList()
        
        self.comModeSpinbox = tk.Spinbox(self.modeFrame, width=3, values=["0" , "1" , "2" , "3"], **SharedDiscoBot.spinboxConfig)
        self.comModeButton = tk.Button(self.modeFrame, text="LoRa-Mode", height=1, pady=0, padx=1, command=self.handleLoRaModeButton, **SharedDiscoBot.buttonConfig)
        
        

        self.camPowCheck.pack(side=tk.TOP, anchor=tk.W)
        self.headPowCheck.pack(side=tk.TOP, anchor=tk.W)
        self.armPowCheck.pack(side=tk.TOP, anchor=tk.W)
        self.armServoPowCheck.pack(side=tk.TOP, anchor=tk.W)
        self.comPowCheck.pack(side=tk.TOP, anchor=tk.W)
        
        self.motorPowCheck.pack(side=tk.TOP, anchor=tk.W)
        self.motorContEnableCheck.pack(side=tk.TOP, anchor=tk.W)
        self.v12PowCheck.pack(side=tk.TOP, anchor=tk.W)
        self.auxPowCheck.pack(side=tk.TOP, anchor=tk.W)
        self.sonarPowCheck.pack(side=tk.TOP, anchor=tk.W)
        
        self.modeFrame.pack(side=tk.TOP, anchor=tk.W)
        self.comPortSpinbox.pack(side=tk.TOP, anchor=tk.W)
        self.comModeSpinbox.pack(side=tk.LEFT, anchor=tk.W)
        self.comModeButton.pack(side=tk.LEFT, anchor=tk.W)      
        
        
                
        return
    

    def refresh(self):
        
        self.camPowCheck.refresh()
        self.headPowCheck.refresh()
        self.armPowCheck.refresh()
        self.comPowCheck.refresh()
        self.armServoPowCheck.refresh()
        
        self.motorPowCheck.refresh()
        self.motorContEnableCheck.refresh()
        self.v12PowCheck.refresh()
        self.auxPowCheck.refresh()
        self.sonarPowCheck.refresh()
        
        
    def handleLoRaModeButton(self):
        
        self.controller.setLoRaMode(self.comModeSpinbox.get())
        
        return 
            
    