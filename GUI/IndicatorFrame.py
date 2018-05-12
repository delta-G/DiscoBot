

import Tkinter as tk
import ttk

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
        
        self.lmLabel = IndicatorLabel(self, text="LCnt")
        self.lmLabel.pack(side=tk.LEFT)
        
        self.rmLabel = IndicatorLabel(self, text="RCnt")
        self.rmLabel.pack(side=tk.LEFT)
        
        self.stickGaugeFrame = tk.Frame(self)
        
        
        
        self.leftStickGauge = ttk.Progressbar(self.stickGaugeFrame, orient="horizontal", length=200, mode="determinate")
        self.rightStickGauge = ttk.Progressbar(self.stickGaugeFrame, orient="horizontal", length=200, mode="determinate")
        self.leftStickGauge.pack(side=tk.TOP)
        self.rightStickGauge.pack(side=tk.TOP)
        
        self.stickGaugeFrame.pack(side=tk.LEFT)
        
        return
    
    def check(self):
        self.ssidLabel.config(text=" SSID \n" + str(self.controller.currentSSID))
        self.hbLabel.check(self.controller.rmbHeartbeatWarningLevel)
        self.bvLabel.config(text=" RMB-Bat \n" + str(self.controller.rmbBatteryVoltage))
        self.rsLabel.config(text=" RMB-RSSI \n" + str(self.controller.currentRssi))
        self.lmLabel.config(text=" LCnt  \n" + str(self.controller.leftMotorCount))
        self.rmLabel.config(text=" RCnt  \n" + str(self.controller.rightMotorCount))
        
        ltamt = self.controller.joy.leftY() + 1
        rtamt = self.controller.joy.rightY() + 1
        
        self.leftStickGauge["value"] = (ltamt /2) * 100
        self.rightStickGauge["value"] = (rtamt /2) * 100
        
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
   
   