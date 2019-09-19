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

class SelectFrame(tk.Frame):
    
#     def propCom(self):
#         if(self.showCommands.get() == 0):
#             self.controller.showCommands = False
#         else:
#             self.controller.showCommands = True
#             
#         return
#     
#     def propRet(self):
#         if(self.showReturns.get() == 0):
#             self.controller.showReturns = False
#         else:
#             self.controller.showReturns = True
#             
#         return
#     
#     def propDeb(self):
#         if(self.showDebug.get() == 0):
#             self.controller.showDebug = False
#         else:
#             self.controller.showDebug = True
#             
#         return
    
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
    
    
    
    
    def __init__(self, aParent, aController):
        
        self.parent = aParent
        self.controller = aController
        tk.Frame.__init__(self, self.parent)
        
        self.leftFrame = tk.Frame(self)
        self.leftFrame.pack(side=tk.LEFT)
        
        self.rightFrame = tk.Frame(self)
        self.rightFrame.pack(side=tk.LEFT)
        
        
#         self.showCommands = tk.IntVar()
#         self.showReturns = tk.IntVar()
#         self.showDebug = tk.IntVar()
        
        self.camPow = tk.IntVar()
        self.headPow = tk.IntVar()
        self.armPow = tk.IntVar()
        self.comPow = tk.IntVar()
        
#         self.comCheck = tk.Checkbutton(self.rightFrame, text="Commands", variable=self.showCommands, command=self.propCom)
#         self.retCheck = tk.Checkbutton(self.rightFrame, text="Return", variable=self.showReturns, command=self.propRet)
#         self.debCheck = tk.Checkbutton(self.rightFrame, text="Debug", variable=self.showDebug, command=self.propDeb)
        
        self.camPowCheck = tk.Checkbutton(self.leftFrame, text="Camera", variable=self.camPow, command=self.propCamPow)
        self.headPowCheck = tk.Checkbutton(self.leftFrame, text="Lights", variable=self.headPow, command=self.propHeadPow)
        self.armPowCheck = tk.Checkbutton(self.leftFrame, text="Arm-CPU", variable=self.armPow)        
        self.comPowCheck = tk.Checkbutton(self.leftFrame, text="Com-CPU", variable=self.comPow)
        
#         self.comCheck.pack(side=tk.TOP, anchor=tk.W)
#         self.retCheck.pack(side=tk.TOP, anchor=tk.W)
#         self.debCheck.pack(side=tk.TOP, anchor=tk.W)
        
        self.camPowCheck.pack(side=tk.TOP, anchor=tk.W)
        self.headPowCheck.pack(side=tk.TOP, anchor=tk.W)
        self.armPowCheck.pack(side=tk.TOP, anchor=tk.W)
        self.comPowCheck.pack(side=tk.TOP, anchor=tk.W)
        
                
        return
    
#     def getStates(self):
#         
#         return (self.showCommands.get(), self.showReturns.get(), self.showDebug.get())
    
    def update(self):
        
        self.camPow.set(self.controller.cameraPower)
        self.headPow.set(self.controller.headlightPower)
        self.armPow.set(self.controller.armPower)
        self.comPow.set(self.controller.comPower)
        
    
            
    