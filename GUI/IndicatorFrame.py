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

import SharedDiscoBot
import tkinter as tk
import glob
import GUI.SelectFrame
import GUI.VoltageFrame

class IndicatorFrame(tk.Frame):
    
    def propController(self):   
        if (self.controller.joy == None) or (not self.controller.joy.connected()):
            self.controller.connectJoystick()
        else:
            self.controller.stopSendingController()
        return 
    
    def propCommsInit(self):
        if self.controller.comms.commsOn:
            self.controller.killConnection()
            self.clearPortList()
        else:
            selection = self.comPortSpinbox.get()
            if selection == "---Check---":
                self.getPortList()
            else:    
                self.controller.initComs(selection)
        
                    
        return
    
    
    def getPortList(self):
        self.portList = glob.glob('/dev/tty[AU]*')
        self.portList.append("---WiFi---")
        self.portList.append("---Check---")
        self.comPortSpinbox.config(values=self.portList)
        return
    
    def clearPortList(self):
        self.portList = ["---WiFi---"]
        self.portList.append("---Check---")     
        self.comPortSpinbox.config(values=self.portList)
        return
    
    def __init__(self, aParent, aGui, aController):
        self.parent = aParent
        tk.Frame.__init__(self, self.parent, **SharedDiscoBot.frameConfig)
        self.controller = aController
        self.gui = aGui
        
#         self.config(height=10, padx=5, pady=5)
        
#         self.ssidLabel = IndicatorLabel(self, text="SSID")
#         self.ssidLabel.pack(side=tk.LEFT)
        
        self.firstFrame = tk.Frame(self, **SharedDiscoBot.frameConfig)
#         self.firstFrame.config(padx=10, pady=10)
        
        self.firstFrame.pack(side = tk.LEFT)
        
        
        self.hbLabel = IndicatorLabel(self.firstFrame, text="HB")
        self.hbLabel.config(width=10)
        self.hbLabel.config(height=1)
        self.hbLabel.bind("<Double-Button-1>", self.hbLabelDoubleClickAction)                
        self.hbLabel.pack(side=tk.TOP)
        
#         self.bvLabel = IndicatorLabel(self.firstFrame, text="BAT")
#         self.bvLabel.config(width=10)        
#         self.bvLabel.config(height=1)
#         self.bvLabel.pack(side=tk.TOP)      
        
        self.baseSigLabel = IndicatorLabel(self.firstFrame, text="BASE 00 , -00")
#         self.baseSigLabel.config(font=(self.gui.defaultFont , 10))
        self.baseSigLabel.config(width=10)        
        self.baseSigLabel.config(height=1)
        self.baseSigLabel.pack(side=tk.TOP) 
        
        self.botSigLabel = IndicatorLabel(self.firstFrame, text="BOT")
        self.botSigLabel.config(width=10)        
        self.botSigLabel.config(height=1)
        self.botSigLabel.pack(side=tk.TOP) 
        
        self.connectButtonFrame = tk.Frame(self.firstFrame, **SharedDiscoBot.frameConfig)
        self.connectButtonFrame.pack(side = tk.TOP)
        
        self.controllerConnectButton = tk.Button(self.connectButtonFrame, text="Control", width = 5, command=self.propController)
        self.controllerConnectButton.config(**SharedDiscoBot.redButton)
        self.controllerConnectButton.pack(side = tk.LEFT)
        self.comConnectButton = tk.Button(self.connectButtonFrame, text="Comms", width = 5, command=self.propCommsInit)
        self.comConnectButton.config(**SharedDiscoBot.redButton)
        self.comConnectButton.pack(side=tk.LEFT)
        
        
        self.modeFrame = tk.Frame(self.firstFrame, **SharedDiscoBot.frameConfig)
        self.modeFrame.pack(side=tk.TOP)
        
        self.comPortSpinbox = tk.Spinbox(self.modeFrame, width=13, **SharedDiscoBot.spinboxConfig)
        self.getPortList()
        
        self.comModeSpinbox = tk.Spinbox(self.modeFrame, width=3, values=["0" , "1" , "2" , "3"], **SharedDiscoBot.spinboxConfig)
        self.comModeButton = tk.Button(self.modeFrame, text="LoRa-Mode", height=1, pady=0, padx=1, command=self.handleLoRaModeButton, **SharedDiscoBot.buttonConfig)
        
        self.comPortSpinbox.pack(side=tk.TOP, anchor=tk.W)
        self.comModeSpinbox.pack(side=tk.LEFT, anchor=tk.W)
        self.comModeButton.pack(side=tk.LEFT, anchor=tk.W) 
        
        
        
#         self.distLabel = IndicatorLabel(self.firstFrame, text="DST")
#         self.distLabel.config(width=10)        
#         self.distLabel.config(height=1)
#         self.distLabel.pack(side=tk.TOP)
        
        
#         self.rsLabel = IndicatorLabel(self, text="RSSI")
#         self.rsLabel.pack(side=tk.LEFT)

        self.voltageFrame = GUI.VoltageFrame.VoltageFrame(self, self.controller) 
        self.voltageFrame.pack(side=tk.LEFT, anchor=tk.N)
        
        self.selectFrame = GUI.SelectFrame.SelectFrame(self, self.controller)
        self.selectFrame.pack(side=tk.LEFT, anchor=tk.N)


        self.secondFrame = tk.Frame(self, **SharedDiscoBot.frameConfig)
        self.secondFrame.config(padx=5, pady=0)
        self.secondFrame.pack(side = tk.LEFT)

        self.motorParamFrame = tk.Frame(self.secondFrame, **SharedDiscoBot.frameConfig)
        
        self.motorParamFrame.pack(side = tk.TOP)
        
        self.ticFrame = LRPropertyFrame(self.motorParamFrame, self.controller, "T", 'MotorCount')
        self.ticFrame.pack(side = tk.TOP)
        self.pwmFrame = LRPropertyFrame(self.motorParamFrame, self.controller, "P", 'MotorOut')
        self.pwmFrame.pack(side = tk.TOP)
        self.spdFrame = LRPropertyFrame(self.motorParamFrame, self.controller, "S", 'MotorSpeed')
        self.spdFrame.pack(side = tk.TOP)
        
        self.throttleLabel = PropertyLabel(self.secondFrame, self.controller, 'THR', 'throttleLevel')
        self.throttleLabel.config(width=12, font=SharedDiscoBot.defaultFont, **SharedDiscoBot.highlightLabelConfig)
        self.throttleLabel.pack(side=tk.TOP)
        
        
        
        self.modeLabel = tk.Label(self.secondFrame, text='MODE', width=12, font=SharedDiscoBot.defaultFont, **SharedDiscoBot.highlightLabelConfig)
        self.modeLabel.pack(side=tk.TOP)
        
        self.videoButton = tk.Button(self.secondFrame, text="Video", width=5, command=self.gui.launchVideo)
        self.videoButton.pack(side=tk.TOP)
        
        return
    
    def check(self):
#         self.ssidLabel.config(text=" SSID \n" + str(self.controller.currentSSID))
        self.hbLabel.check(self.controller.rmbHeartbeatWarningLevel)
        self.hbLabel.config(text="HB - " + "{:.3f}".format(self.controller.turnAroundTime * 1000))
#         self.bvLabel.config(text="Bat" + str(self.controller.properties['batteryVoltage']))
#         numCells = 0
#         for i in range(6):
#             if (self.controller.properties['batteryVoltage'] > (i * 3.4)):
#                 numCells = i
#             else:
#                 break
#         if self.controller.properties['batteryVoltage'] < numCells * 3.55:
#             self.bvLabel.config(fg=SharedDiscoBot.colors['red'])
#         elif self.controller.properties['batteryVoltage'] < numCells * 3.85:
#             self.bvLabel.config(fg=SharedDiscoBot.colors['yellow'])
#         else: 
#             self.bvLabel.config(fg=SharedDiscoBot.colors['green'])

        
#         self.baseSigLabel.config(text="SNR - RSSI")
        if self.controller.comms.isWiFiMode():
            self.botSigLabel.config(text="WiFi Mode")
            self.baseSigLabel.config(text=f"RSSI: {self.controller.lastWifiRSSI: 3d}")
            self.comModeSpinbox.config(state='disabled')
            self.comModeButton.config(state='disabled')
        else:
            self.botSigLabel.config(text="Bot " + str(self.controller.lastBotSNR) + " , " + str(self.controller.lastBotRSSI))
            self.baseSigLabel.config(text="Base " + str(self.controller.lastBaseSNR) + " , " + str(self.controller.lastBaseRSSI))
            self.comModeSpinbox.config(state='normal')
            self.comModeButton.config(state='normal')
        
#         self.distLabel.config(text="d= " + str(self.controller.sonarDistance))
        
        
        self.voltageFrame.refresh()  
        self.selectFrame.refresh()       
        
        self.ticFrame.refresh()
        self.pwmFrame.refresh()
        self.spdFrame.refresh()
        
#         self.throttleLabel.config(text="THR: " + str(self.controller.throttleLevel))
        self.throttleLabel.refresh()
        
        self.modeLabel.config(text="Mode: " + self.controller.getProperty('driveMode'))
        
        if(self.controller.joy is not None) and (self.controller.joy.connected()):
            if(self.controller.sendingController):
                self.controllerConnectButton.config(bg=SharedDiscoBot.colors['green'])
            else:
                self.controllerConnectButton.config(bg=SharedDiscoBot.colors['yellow'])                
        else:            
            self.controllerConnectButton.config(bg=SharedDiscoBot.colors['red'])
        
        return
    
    def hbLabelDoubleClickAction(self, event):
        
        self.controller.connectToBot()
        
        return 
    
    def handleLoRaModeButton(self):
        
        self.controller.setLoRaMode(self.comModeSpinbox.get())
        
        return 

class IndicatorLabel(tk.Label):
    
    def __init__(self, aParent, text):
        
        self.parent = aParent
        tk.Label.__init__(self, self.parent, text=text)
        
        self.config(padx=5, pady=5, height=2, font=SharedDiscoBot.defaultFont, **SharedDiscoBot.highlightLabelConfig)
        
        return

    def check(self, aState):
        
        self.state = aState
        
        self.config(fg=self.state)            
        
        
        return


class PropertyLabel(tk.Label):
    
    def __init__(self, aParent, aController, aName, aKey):
        self.parent = aParent
        self.controller = aController
        self.name = aName
        self.key = aKey
        tk.Label.__init__(self, self.parent, text=self.name)        
        self.config(font=SharedDiscoBot.defaultFont, **SharedDiscoBot.highlightLabelConfig)
        
        return
    
    def refresh(self):
        self.config(text=self.name + ': ' + str(self.controller.getProperty(self.key)))
        return
        


class LRPropertyFrame(tk.Frame):
    
    def __init__(self, aParent, aController, aName, aPartKey):
        self.parent = aParent
        self.controller = aController
        self.name = aName
        self.partialKey = aPartKey
        tk.Frame.__init__(self, self.parent, **SharedDiscoBot.highlightFrameConfig)
        
        self.leftLabel = tk.Label(self, text='100', width=5, **SharedDiscoBot.labelConfig)
        self.nameLabel = tk.Label(self, text=(" -" +str(self.name) + "- "), font = SharedDiscoBot.defaultFont, **SharedDiscoBot.labelConfig)
        self.rightLabel = tk.Label(self, text='123', width=5, **SharedDiscoBot.labelConfig)
        
        self.leftLabel.pack(side=tk.LEFT)
        self.nameLabel.pack(side=tk.LEFT)
        self.rightLabel.pack(side=tk.LEFT)
        
        return 
    
    
    def refresh(self):
        self.leftLabel.config(text=str(self.controller.getProperty('left'+self.partialKey)))
        self.rightLabel.config(text=str(self.controller.getProperty('right'+self.partialKey)))
        
        return


       
    