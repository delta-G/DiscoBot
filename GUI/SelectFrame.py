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
    
    def propComPow(self):
        if(self.comPow.get() == 0):
            self.controller.outPutRunner("<QR0>")
        else:
            self.controller.outPutRunner("<QR1>")
        return
    
    def propArmServoPow(self):
        if(self.armServoPow.get() == 0):
            self.controller.outPutRunner("<A,Cp>")
        else:
            self.controller.outPutRunner("<A,CP>")
        return
    
    def propArmPow(self):
        if(self.armPow.get() == 0):
            self.controller.outPutRunner("<QA0>")
        else:
            self.controller.outPutRunner("<QA1>")
        return
    
    def propMotorPow(self):
        if(self.motorPow.get() == 0):
            self.controller.outPutRunner("<QM0>")
        else:
            self.controller.outPutRunner("<QM1>")
        return
    
    def propMotorCont(self):
        if(self.motorContEnable.get() == 0):
            self.controller.outPutRunner("<Qm0>")
        else:
            self.controller.outPutRunner("<Qm1>")
        return
    
    def propV12Pow(self):
        if(self.v12Pow.get() == 0):
            self.controller.outPutRunner("<QV0>")
        else:
            self.controller.outPutRunner("<QV1>")
        return
    
    def propAuxPow(self):
        if(self.auxPow.get() == 0):
            self.controller.outPutRunner("<Qa0>")
        else:
            self.controller.outPutRunner("<Qa1>")
        return
    
    def propSonarPow(self):
        if(self.sonarPow.get() == 0):
            self.controller.outPutRunner("<QS0>")
        else:
            self.controller.outPutRunner("<QS1>")
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
        
        self.checkFrame = tk.Frame(self, **SharedDiscoBot.frameConfig)
        self.checkFrame.pack(side=tk.TOP)
        
        
        self.leftFrame = tk.Frame(self.checkFrame, **SharedDiscoBot.frameConfig)
        self.leftFrame.pack(side=tk.LEFT)
        
        self.rightFrame = tk.Frame(self.checkFrame, **SharedDiscoBot.frameConfig)
        self.rightFrame.pack(side=tk.LEFT)
        

        
        self.camPow = tk.IntVar()
        self.headPow = tk.IntVar()
        self.armPow = tk.IntVar()
        self.comPow = tk.IntVar()
        
        self.armServoPow = tk.IntVar()
        
        self.motorPow = tk.IntVar()
        self.motorContEnable = tk.IntVar()
        self.v12Pow = tk.IntVar()
        self.auxPow = tk.IntVar()
        self.sonarPow = tk.IntVar()
        
        

        
        self.camPowCheck = tk.Checkbutton(self.leftFrame, text="Camera", variable=self.camPow, command=self.propCamPow, anchor=tk.W, width=9, **SharedDiscoBot.checkboxConfig)
        self.headPowCheck = tk.Checkbutton(self.leftFrame, text="Lights", variable=self.headPow, command=self.propHeadPow, anchor=tk.W, width=9, **SharedDiscoBot.checkboxConfig)
        self.armPowCheck = tk.Checkbutton(self.leftFrame, text="Arm-CPU", variable=self.armPow, command=self.propArmPow, anchor=tk.W, width=9, **SharedDiscoBot.checkboxConfig)        
        self.comPowCheck = tk.Checkbutton(self.leftFrame, text="Com-CPU", variable=self.comPow, command=self.propComPow, anchor=tk.W, width=9, **SharedDiscoBot.checkboxConfig)
        self.armServoPowCheck = tk.Checkbutton(self.leftFrame, text="Arm-Servo", variable=self.armServoPow, command=self.propArmServoPow, anchor=tk.W, width=9, **SharedDiscoBot.checkboxConfig)
        
        self.motorPowCheck = tk.Checkbutton(self.rightFrame, text="Motors", variable=self.motorPow, command=self.propMotorPow, anchor=tk.W, width=9, **SharedDiscoBot.checkboxConfig)
        self.motorContEnableCheck = tk.Checkbutton(self.rightFrame, text="Controller", variable=self.motorContEnable, command=self.propMotorCont, anchor=tk.W, width=9, **SharedDiscoBot.checkboxConfig)
        self.v12PowCheck = tk.Checkbutton(self.rightFrame, text="12-Volt", variable=self.v12Pow, command=self.propV12Pow, anchor=tk.W, width=9, **SharedDiscoBot.checkboxConfig)
        self.auxPowCheck = tk.Checkbutton(self.rightFrame, text="Aux", variable=self.auxPow, command=self.propAuxPow, anchor=tk.W, width=9, **SharedDiscoBot.checkboxConfig)
        self.sonarPowCheck = tk.Checkbutton(self.rightFrame, text="Sonar", variable=self.sonarPow, command=self.propSonarPow, anchor=tk.W, width=9, **SharedDiscoBot.checkboxConfig)
        
        
        
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
        
        self.modeFrame.pack(side=tk.TOP, anchor=tk.W)
        self.comPortSpinbox.pack(side=tk.TOP, anchor=tk.W)
        self.comModeSpinbox.pack(side=tk.LEFT, anchor=tk.W)
        self.comModeButton.pack(side=tk.LEFT, anchor=tk.W)      
        
        self.motorPowCheck.pack(side=tk.TOP, anchor=tk.W)
        self.motorContEnableCheck.pack(side=tk.TOP, anchor=tk.W)
        self.v12PowCheck.pack(side=tk.TOP, anchor=tk.W)
        self.auxPowCheck.pack(side=tk.TOP, anchor=tk.W)
        self.sonarPowCheck.pack(side=tk.TOP, anchor=tk.W)
                
        return
    

    def update(self):
        
        self.camPow.set(self.controller.cameraPower)
        self.headPow.set(self.controller.headlightPower)
        self.armPow.set(self.controller.armPower)
        self.comPow.set(self.controller.comPower)
        self.armServoPow.set(self.controller.armServoPower)
        
        self.motorPow.set(self.controller.motorPower)
        self.motorContEnable.set(self.controller.motorContEnable)
        self.v12Pow.set(self.controller.v12Power)
        self.auxPow.set(self.controller.auxPower)
        self.sonarPow.set(self.controller.sonarPower)
        
        
    def handleLoRaModeButton(self):
        
        self.controller.setLoRaMode(self.comModeSpinbox.get())
        
        return 
            
    