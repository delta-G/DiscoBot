

import Tkinter as tk

class IndicatorFrame(tk.Frame):
    
    
    def __init__(self, aParent, aController):
        self.parent = aParent
        tk.Frame.__init__(self, self.parent)
        self.controller = aController
        
        self.config(height=10, padx=5, pady=5)
        
        self.hbLabel = IndicatorLabel(self, text="RMB-HB")
        self.hbLabel.pack(side=tk.LEFT)
        
        
        return
    
    def check(self):
        self.hbLabel.check(self.controller.rmbHeartbeatWarningLevel)
        return
    

class IndicatorLabel(tk.Label):
    
    def __init__(self, aParent, text):
        
        self.parent = aParent
        tk.Label.__init__(self, self.parent, text=text)
        
        self.config(padx=5, pady=5, height=2, font="Verdana 12 bold")
        
        return

    def check(self, aState):
        
        self.state = aState
        
        self.config(bg=self.state)            
        
        
        return
   