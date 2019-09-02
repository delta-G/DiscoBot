

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
        self.controllerConnectButton = tk.Button(self, text="Control", command=self.propController)
        self.comConnectButton = tk.Button(self, text="Comms", command=self.propCommsInit)
        
        self.comCheck.pack(side=tk.TOP)
        self.retCheck.pack(side=tk.TOP)
        self.debCheck.pack(side=tk.TOP)
        self.controllerConnectButton.pack(side=tk.TOP)
        self.comConnectButton.pack(side=tk.TOP)
        
                
        return
    
    def getStates(self):
        
        return (self.showCommands.get(), self.showReturns.get(), self.showDebug.get())
    
    
    
            
    