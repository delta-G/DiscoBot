

import Tkinter as tk

class IndicatorFrame(tk.Frame):
    
    
    def __init__(self, aParent, aController):
        self.parent = aParent
        tk.Frame.__init__(self, self.parent)
        self.controller = aController
        
        self.config(height=10, padx=5, pady=5)
        
#         self.ssidLabel = IndicatorLabel(self, text="SSID")
#         self.ssidLabel.pack(side=tk.LEFT)
        
        self.firstFrame = tk.Frame(self)
        
        self.firstFrame.pack(side = tk.LEFT)
        
        
        self.hbLabel = IndicatorLabel(self.firstFrame, text="HB")
        self.hbLabel.pack(side=tk.TOP)
        
        self.bvLabel = IndicatorLabel(self.firstFrame, text="BAT")
        self.bvLabel.pack(side=tk.TOP)      
        
#         self.rsLabel = IndicatorLabel(self, text="RSSI")
#         self.rsLabel.pack(side=tk.LEFT)


        self.ticFrame = tk.Frame(self)
        
        self.ticFrame.pack(side = tk.LEFT)

        self.ltLabel = IndicatorLabel(self.ticFrame, text="LTic")
        self.ltLabel.pack(side=tk.TOP)
        
        self.rtLabel = IndicatorLabel(self.ticFrame, text="RTic")
        self.rtLabel.pack(side=tk.TOP)
        
        
        self.pwmFrame = tk.Frame(self)
        
        self.pwmFrame.pack(side = tk.LEFT)
        
        
        self.lmLabel = IndicatorLabel(self.pwmFrame, text="LOut")
        self.lmLabel.pack(side=tk.TOP)
        
        self.rmLabel = IndicatorLabel(self.pwmFrame, text="ROut")
        self.rmLabel.pack(side=tk.TOP)
        
        
        self.speedFrame = tk.Frame(self)
        
        self.speedFrame.pack(side = tk.LEFT)
        
        
        self.lspdLabel = IndicatorLabel(self.speedFrame, text="LSpd")
        self.lspdLabel.pack(side=tk.TOP)
        
        self.rspdLabel = IndicatorLabel(self.speedFrame, text="LSpd")
        self.rspdLabel.pack(side=tk.TOP)
        
#         self.stickGaugeFrame = tk.Frame(self)
#         
#         
#         
#         self.leftStickGauge = ttk.Progressbar(self.stickGaugeFrame, orient="horizontal", length=200, mode="determinate")
#         self.rightStickGauge = ttk.Progressbar(self.stickGaugeFrame, orient="horizontal", length=200, mode="determinate")
#         self.leftStickGauge.pack(side=tk.TOP)
#         self.rightStickGauge.pack(side=tk.TOP)
#         
#         self.stickGaugeFrame.pack(side=tk.LEFT)
        
        return
    
    def check(self):
#         self.ssidLabel.config(text=" SSID \n" + str(self.controller.currentSSID))
        self.hbLabel.check(self.controller.rmbHeartbeatWarningLevel)
        self.hbLabel.config(text="HB - " + str(self.controller.lastBotSNR) + " , " + str(self.controller.lastBotRSSI) + "\n" + "{:.3f}".format(self.controller.turnAroundTime * 1000))
        self.bvLabel.config(text="RMB-Bat" + str(self.controller.rmbBatteryVoltage)+ "\n" + self.controller.getDriveModeFromStatusByte())
        if self.controller.rmbBatteryVoltage < 6.5:
            self.bvLabel.config(bg="Red")
        elif self.controller.rmbBatteryVoltage < 7.4:
            self.bvLabel.config(bg="Yellow")
        else: 
            self.bvLabel.config(bg="Green")
#         self.rsLabel.config(text=" RMB-RSSI \n" + str(self.controller.currentRssi))

        self.ltLabel.config(text=" LTic \n" + str(self.controller.leftMotorCount))
        self.rtLabel.config(text=" RTic \n" + str(self.controller.rightMotorCount))


        self.lmLabel.config(text=" LPwm \n" + str(self.controller.leftMotorOut))
        self.rmLabel.config(text=" RPwm \n" + str(self.controller.rightMotorOut))
        
        self.lspdLabel.config(text=" LSpd \n" + str(self.controller.leftMotorSpeed))
        self.rspdLabel.config(text=" RSpd \n" + str(self.controller.rightMotorSpeed))
        
#         ltamt = self.controller.joy.leftY() + 1
#         rtamt = self.controller.joy.rightY() + 1
#         
#         self.leftStickGauge["value"] = (ltamt /2) * 100
#         self.rightStickGauge["value"] = (rtamt /2) * 100
        
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
   
   