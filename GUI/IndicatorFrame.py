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

class IndicatorFrame(tk.Frame):
    
    def propController(self):        
        self.controller.connectJoystick()    
        return 
    
    def propCommsInit(self):        
        self.controller.initComs()
        return
    
    
    def __init__(self, aParent, aGui, aController):
        self.parent = aParent
        tk.Frame.__init__(self, self.parent)
        self.controller = aController
        self.gui = aGui
        
        self.config(height=10, padx=5, pady=5)
        
#         self.ssidLabel = IndicatorLabel(self, text="SSID")
#         self.ssidLabel.pack(side=tk.LEFT)
        
        self.firstFrame = tk.Frame(self)
        self.firstFrame.config(padx=10, pady=10)
        
        self.firstFrame.pack(side = tk.LEFT)
        
        
        self.hbLabel = IndicatorLabel(self.firstFrame, text="HB")
        self.hbLabel.config(width=10)
        self.hbLabel.config(height=1)        
        self.hbLabel.pack(side=tk.TOP)
        
        self.bvLabel = IndicatorLabel(self.firstFrame, text="BAT")
        self.bvLabel.config(width=10)        
        self.bvLabel.config(height=1)
        self.bvLabel.pack(side=tk.TOP)      
        
        self.baseSigLabel = IndicatorLabel(self.firstFrame, text="BASE 00 , -00")
#         self.baseSigLabel.config(font=(self.gui.defaultFont , 10))
        self.baseSigLabel.config(width=10)        
        self.baseSigLabel.config(height=1)
        self.baseSigLabel.pack(side=tk.TOP) 
        
        self.botSigLabel = IndicatorLabel(self.firstFrame, text="BOT")
        self.botSigLabel.config(width=10)        
        self.botSigLabel.config(height=1)
        self.botSigLabel.pack(side=tk.TOP) 
        
#         self.rsLabel = IndicatorLabel(self, text="RSSI")
#         self.rsLabel.pack(side=tk.LEFT)

        self.secondFrame = tk.Frame(self)
        self.secondFrame.config(padx=10, pady=10)
        self.secondFrame.pack(side = tk.LEFT)

        self.motorParamFrame = tk.Frame(self.secondFrame)
        
        self.motorParamFrame.pack(side = tk.TOP)
        
        self.ticFrame = MotorParamFrame(self.motorParamFrame, "T")
        self.ticFrame.pack(side = tk.TOP)
        self.pwmFrame = MotorParamFrame(self.motorParamFrame, "P")
        self.pwmFrame.pack(side = tk.TOP)
        self.spdFrame = MotorParamFrame(self.motorParamFrame, "S")
        self.spdFrame.pack(side = tk.TOP)
        
        self.connectButtonFrame = tk.Frame(self.secondFrame)
        self.connectButtonFrame.pack(side = tk.TOP)
        
        self.controllerConnectButton = tk.Button(self.connectButtonFrame, text="Control", width = 5, bg="red", command=self.propController)
        self.controllerConnectButton.pack(side = tk.LEFT)
        self.comConnectButton = tk.Button(self.connectButtonFrame, text="Comms", width = 5, bg="red", command=self.propCommsInit)
        self.comConnectButton.pack(side=tk.LEFT)
        
        self.modeLabel = tk.Label(self.secondFrame, text='MODE', width=12, font="Verdana 12 bold", bd=1, relief=tk.SUNKEN)
        self.modeLabel.pack(side=tk.TOP)

#         self.ltLabel = IndicatorLabel(self.ticFrame, text="LTic")
#         self.ltLabel.pack(side=tk.TOP)
#         
#         self.rtLabel = IndicatorLabel(self.ticFrame, text="RTic")
#         self.rtLabel.pack(side=tk.TOP)
#         
#         
#         self.pwmFrame = tk.Frame(self)
#         
#         self.pwmFrame.pack(side = tk.LEFT)
#         
#         
#         self.lmLabel = IndicatorLabel(self.pwmFrame, text="LOut")
#         self.lmLabel.pack(side=tk.TOP)
#         
#         self.rmLabel = IndicatorLabel(self.pwmFrame, text="ROut")
#         self.rmLabel.pack(side=tk.TOP)
#         
#         
#         self.speedFrame = tk.Frame(self)
#         
#         self.speedFrame.pack(side = tk.LEFT)
#         
#         
#         self.lspdLabel = IndicatorLabel(self.speedFrame, text="LSpd")
#         self.lspdLabel.pack(side=tk.TOP)
#         
#         self.rspdLabel = IndicatorLabel(self.speedFrame, text="LSpd")
#         self.rspdLabel.pack(side=tk.TOP)
        
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
        self.hbLabel.check(self.gui.colors[self.controller.rmbHeartbeatWarningLevel])
        self.hbLabel.config(text="HB - " + "{:.3f}".format(self.controller.turnAroundTime * 1000))
        self.bvLabel.config(text="Bat" + str(self.controller.rmbBatteryVoltage))
        if self.controller.rmbBatteryVoltage < 6.5:
            self.bvLabel.config(bg=self.gui.colors['red'])
        elif self.controller.rmbBatteryVoltage < 7.4:
            self.bvLabel.config(bg=self.gui.colors['yellow'])
        else: 
            self.bvLabel.config(bg=self.gui.colors['green'])
#         self.rsLabel.config(text=" RMB-RSSI \n" + str(self.controller.currentRssi))

        
#         self.baseSigLabel.config(text="SNR - RSSI")
        self.botSigLabel.config(text="Bot " + str(self.controller.lastBotSNR) + " , " + str(self.controller.lastBotRSSI))
        
        self.ticFrame.update(self.controller.leftMotorCount, self.controller.rightMotorCount)
        self.pwmFrame.update(self.controller.leftMotorOut, self.controller.rightMotorOut)
        self.spdFrame.update(self.controller.leftMotorSpeed, self.controller.rightMotorSpeed)
        
        self.modeLabel.config(text="Mode: " + self.controller.driveMode)


        
#         self.ltLabel.config(text=" LTic \n" + str(self.controller.leftMotorCount))
#         self.rtLabel.config(text=" RTic \n" + str(self.controller.rightMotorCount))
# 
# 
#         self.lmLabel.config(text=" LPwm \n" + str(self.controller.leftMotorOut))
#         self.rmLabel.config(text=" RPwm \n" + str(self.controller.rightMotorOut))
#         
#         self.lspdLabel.config(text=" LSpd \n" + str(self.controller.leftMotorSpeed))
#         self.rspdLabel.config(text=" RSpd \n" + str(self.controller.rightMotorSpeed))
        
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
   
   

class MotorParamFrame(tk.Frame):
    
    def __init__(self, aParent, aName):
        self.parent = aParent
        self.name = aName
        tk.Frame.__init__(self, self.parent, bd=1, relief=tk.SUNKEN)
        
        self.leftLabel = tk.Label(self, text='100', width=5)
        self.nameLabel = tk.Label(self, text=(" -" +str(self.name) + "- "), font = "veranda 12 bold")
        self.rightLabel = tk.Label(self, text='123', width=5)
        
        self.leftLabel.pack(side=tk.LEFT)
        self.nameLabel.pack(side=tk.LEFT)
        self.rightLabel.pack(side=tk.LEFT)
        
        return 
    
    
    def update(self, aLeftNumber, aRightNumber):
        self.leftLabel.config(text=str(aLeftNumber))
        self.rightLabel.config(text=str(aRightNumber))
        
        return
        
    