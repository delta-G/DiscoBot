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
    
    def propCom(self):
        if(self.showCommands.get() == 0):
            self.controller.showCommands = False
        else:
            self.controller.showCommands = True
            
        return
    
    def propRet(self):
        if(self.showReturns.get() == 0):
            self.controller.showReturns = False
        else:
            self.controller.showReturns = True
            
        return
    
    def propDeb(self):
        if(self.showDebug.get() == 0):
            self.controller.showDebug = False
        else:
            self.controller.showDebug = True
            
        return
    
    def propController(self):        
        self.controller.connectJoystick()    
        return 
    
    def propCommsInit(self):        
        self.controller.initComs()
        return
    
    
    
    def __init__(self, aParent, aController):
        
        self.parent = aParent
        self.controller = aController
        tk.Frame.__init__(self, self.parent)
        
        self.showCommands = tk.IntVar()
        self.showReturns = tk.IntVar()
        self.showDebug = tk.IntVar()
        
        self.comCheck = tk.Checkbutton(self, text="Commands", variable=self.showCommands, command=self.propCom)
        self.retCheck = tk.Checkbutton(self, text="Return", variable=self.showReturns, command=self.propRet)
        self.debCheck = tk.Checkbutton(self, text="Debug", variable=self.showDebug, command=self.propDeb)
        self.controllerConnectButton = tk.Button(self, text="Control", bg="red", command=self.propController)
        self.comConnectButton = tk.Button(self, text="Comms", bg="red", command=self.propCommsInit)
        
        self.comCheck.pack(side=tk.TOP)
        self.retCheck.pack(side=tk.TOP)
        self.debCheck.pack(side=tk.TOP)
        self.controllerConnectButton.pack(side=tk.TOP)
        self.comConnectButton.pack(side=tk.TOP)
        
                
        return
    
    def getStates(self):
        
        return (self.showCommands.get(), self.showReturns.get(), self.showDebug.get())
    
    
    
            
    