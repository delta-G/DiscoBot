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
import sys
import glob
import serial

import SharedDiscoBot

class SelectFrame(tk.Frame):
    

    
    def propCamPow(self):
        if(self.camPow.get() == 0):
            self.controller.outPutRunner("<V0>")
        else:
            self.controller.outPutRunner("<V1>")
        return
    
    def propHeadPow(self):
        if(self.headPow.get() == 0):
            self.controller.outPutRunner("<H0>")
        else:
            self.controller.outPutRunner("<H1>")
        return
    
    def propArmServoPow(self):
        if(self.armServoPow.get() == 0):
            self.controller.outPutRunner("<A,Cp>")
        else:
            self.controller.outPutRunner("<A,CP>")
        return
            
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
        
        self.leftFrame = tk.Frame(self, **SharedDiscoBot.frameConfig)
        self.leftFrame.pack(side=tk.LEFT)
        
        self.rightFrame = tk.Frame(self, **SharedDiscoBot.frameConfig)
        self.rightFrame.pack(side=tk.LEFT)
        

        
        self.camPow = tk.IntVar()
        self.headPow = tk.IntVar()
        self.armPow = tk.IntVar()
        self.comPow = tk.IntVar()
        
        self.armServoPow = tk.IntVar()
        

        
        self.camPowCheck = tk.Checkbutton(self.leftFrame, text="Camera", variable=self.camPow, command=self.propCamPow, **SharedDiscoBot.checkboxConfig)
        self.headPowCheck = tk.Checkbutton(self.leftFrame, text="Lights", variable=self.headPow, command=self.propHeadPow, **SharedDiscoBot.checkboxConfig)
        self.armPowCheck = tk.Checkbutton(self.leftFrame, text="Arm-CPU", variable=self.armPow, **SharedDiscoBot.checkboxConfig)        
        self.comPowCheck = tk.Checkbutton(self.leftFrame, text="Com-CPU", variable=self.comPow, **SharedDiscoBot.checkboxConfig)
        self.armServoPowCheck = tk.Checkbutton(self.leftFrame, text="Arm-Servo", variable=self.armServoPow, command=self.propArmServoPow, **SharedDiscoBot.checkboxConfig)
        
        
        
        self.comPortSpinbox = tk.Spinbox(self.leftFrame, width=13, **SharedDiscoBot.spinboxConfig)
        self.getPortList()
        
        self.modeFrame = tk.Frame(self.leftFrame, **SharedDiscoBot.frameConfig)
        
        self.comModeSpinbox = tk.Spinbox(self.modeFrame, width=3, values=["0" , "1" , "2" , "3"], **SharedDiscoBot.spinboxConfig)
        self.comModeButton = tk.Button(self.modeFrame, text="LoRa-Mode", height=1, pady=0, padx=1, command=self.handleLoRaModeButton, **SharedDiscoBot.buttonConfig)

        self.camPowCheck.pack(side=tk.TOP, anchor=tk.W)
        self.headPowCheck.pack(side=tk.TOP, anchor=tk.W)
        self.armPowCheck.pack(side=tk.TOP, anchor=tk.W)
        self.armServoPowCheck.pack(side=tk.TOP, anchor=tk.W)
        self.comPowCheck.pack(side=tk.TOP, anchor=tk.W)
        self.comPortSpinbox.pack(side=tk.TOP, anchor=tk.W)
        
        self.modeFrame.pack(side=tk.TOP, anchor=tk.W)
        self.comModeSpinbox.pack(side=tk.LEFT, anchor=tk.W)
        self.comModeButton.pack(side=tk.LEFT, anchor=tk.W)      
        
                
        return
    

    def update(self):
        
        self.camPow.set(self.controller.cameraPower)
        self.headPow.set(self.controller.headlightPower)
        self.armPow.set(self.controller.armPower)
        self.comPow.set(self.controller.comPower)
        self.armServoPow.set(self.controller.armServoPower)
        
    def handleLoRaModeButton(self):
        
        self.controller.setLoRaMode(self.comModeSpinbox.get())
        
        return 
            
    