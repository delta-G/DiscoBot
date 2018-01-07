

import Tkinter as tk

class IndicatorFrame(tk.Frame):
    
    
    def __init__(self, aParent, aController):
        self.parent = aParent
        tk.Frame.__init__(self, self.parent)
        self.controller = aController
        
        self.config(height=10, padx=5, pady=5)
        
        self.ssidLabel = IndicatorLabel(self, text="SSID")
        self.ssidLabel.pack(side=tk.LEFT)
        
        self.hbLabel = IndicatorLabel(self, text="RMB-HB")
        self.hbLabel.pack(side=tk.LEFT)
        
        self.bvLabel = IndicatorLabel(self, text="BAT")
        self.bvLabel.pack(side=tk.LEFT)      
        
        self.rsLabel = IndicatorLabel(self, text="RSSI")
        self.rsLabel.pack(side=tk.LEFT)
        
        
        return
    
    def check(self):
        self.ssidLabel.config(text=" SSID \n" + str(self.controller.currentSSID))
        self.hbLabel.check(self.controller.rmbHeartbeatWarningLevel)
        self.bvLabel.config(text=" RMB-Bat \n" + str(self.controller.rmbBatteryVoltage))
        self.rsLabel.config(text=" RMB-RSSI \n" + str(self.controller.currentRssi))
        return
    

class IndicatorLabel(tk.Label):
    
    def __init__(self, aParent, text):
        
        self.parent = aParent
        tk.Label.__init__(self, self.parent, text=text)
        
        self.config(padx=5, pady=5, height=2, font="Verdana 12 bold", bd=1, relief=tk.SUNKEN)
        
        return

    def check(self, aState):
        
        self.state = aState
        
        self.config(bg=self.state)            
        
        
        return
   