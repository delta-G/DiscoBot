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
        tk.Frame.__init__(self, self.parent)
        
        self.leftFrame = tk.Frame(self)
        self.leftFrame.pack(side=tk.LEFT)
        
        self.rightFrame = tk.Frame(self)
        self.rightFrame.pack(side=tk.LEFT)
        

        
        self.camPow = tk.IntVar()
        self.headPow = tk.IntVar()
        self.armPow = tk.IntVar()
        self.comPow = tk.IntVar()
        
        self.armServoPow = tk.IntVar()
        

        
        self.camPowCheck = tk.Checkbutton(self.leftFrame, text="Camera", variable=self.camPow, command=self.propCamPow)
        self.headPowCheck = tk.Checkbutton(self.leftFrame, text="Lights", variable=self.headPow, command=self.propHeadPow)
        self.armPowCheck = tk.Checkbutton(self.leftFrame, text="Arm-CPU", variable=self.armPow)        
        self.comPowCheck = tk.Checkbutton(self.leftFrame, text="Com-CPU", variable=self.comPow)
        self.armServoPowCheck = tk.Checkbutton(self.leftFrame, text="Arm-Servo", variable=self.armServoPow, command=self.propArmServoPow)
        
        
        
        self.comPortSpinbox = tk.Spinbox(self.leftFrame, width=13)
        self.getPortList()
        
#         self.comPortCombobox = ttk.Combobox(self.leftFrame, values=["COM1" , "COM2"])

        self.camPowCheck.pack(side=tk.TOP, anchor=tk.W)
        self.headPowCheck.pack(side=tk.TOP, anchor=tk.W)
        self.armPowCheck.pack(side=tk.TOP, anchor=tk.W)
        self.armServoPowCheck.pack(side=tk.TOP, anchor=tk.W)
        self.comPowCheck.pack(side=tk.TOP, anchor=tk.W)
        self.comPortSpinbox.pack(side=tk.TOP, anchor=tk.W)
        
                
        return
    

    def update(self):
        
        self.camPow.set(self.controller.cameraPower)
        self.headPow.set(self.controller.headlightPower)
        self.armPow.set(self.controller.armPower)
        self.comPow.set(self.controller.comPower)
        self.armServoPow.set(self.controller.armServoPower)
        
    
            
    