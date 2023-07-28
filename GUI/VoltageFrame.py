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


import tkinter as tk
import SharedDiscoBot
# import GUI.Gauge as Gauge


class VoltageFrame(tk.Frame):
    
    def __init__(self, aParent, aController):
        
        self.parent = aParent
        self.controller = aController
        tk.Frame.__init__(self, self.parent, **SharedDiscoBot.frameConfig)
        
        self.batVlabel = voltageLabel(self, self.controller, "Bat", 'batteryVoltage')
        self.motorVlabel = voltageLabel(self, self.controller, "Mot", 'motorVoltage')
        self.mainVlabel = voltageLabel(self, self.controller, "Main", 'mainVoltage')
        self.comVlabel = voltageLabel(self, self.controller, "Com", 'comVoltage')
        self.auxVlabel = voltageLabel(self, self.controller, "Aux", 'auxVoltage')
        self.v12Vlabel = voltageLabel(self, self.controller, "12V", 'v12Voltage')
        self.currentSensorLabel = voltageLabel(self, self.controller, "Amps", 'currentSensor')
        
#         widerth = 100
#         self.batVlabel = Gauge.Gauge(self, self.controller, "Battery", 'batteryVoltage', aWidth = widerth, aMinval=0.0, aMaxval=20.0, aLowRed=3.0, aLowYellow=6.0, aHighYellow=14.0, aHighRed=17.0)
#         self.motorVlabel = Gauge.Gauge(self, self.controller, "Motor", 'motorVoltage', aWidth = widerth, aMinval=6.0, aMaxval=12.0, aLowRed=7.0, aLowYellow=7.5, aHighYellow=10.5, aHighRed=11.0)
#         self.mainVlabel = Gauge.Gauge(self, self.controller, "Main", 'mainVoltage', aWidth = widerth, aMinval=4.0, aMaxval=6.5, aLowRed=4.8, aLowYellow=5.0, aHighYellow=5.3, aHighRed=5.5)
#         self.comVlabel = Gauge.Gauge(self, self.controller, "Com", 'comVoltage', aWidth = widerth, aMinval=4.0, aMaxval=6.5, aLowRed=4.8, aLowYellow=5.0, aHighYellow=5.3, aHighRed=5.5)
#         self.auxVlabel = Gauge.Gauge(self, self.controller, "Aux", 'auxVoltage', aWidth = widerth, aMinval=4.0, aMaxval=6.5, aLowRed=4.8, aLowYellow=5.0, aHighYellow=5.3, aHighRed=5.5)
#         self.v12Vlabel = Gauge.Gauge(self, self.controller, "12-Volt", 'v12Voltage', aWidth = widerth, aMinval=10.0, aMaxval=14.7, aLowRed=11.2, aLowYellow=12.0, aHighYellow=12.7, aHighRed=13.5)
        
        self.batVlabel.pack(side=tk.TOP, anchor=tk.W)        
        self.currentSensorLabel.pack(side=tk.TOP, anchor=tk.W)
        self.motorVlabel.pack(side=tk.TOP, anchor=tk.W)
        self.mainVlabel.pack(side=tk.TOP, anchor=tk.W)
        self.comVlabel.pack(side=tk.TOP, anchor=tk.W)
        self.auxVlabel.pack(side=tk.TOP, anchor=tk.W)
        self.v12Vlabel.pack(side=tk.TOP, anchor=tk.W)
        
        return 
    
    def refresh(self):
        self.batVlabel.refresh()
        self.motorVlabel.refresh()
        self.mainVlabel.refresh()
        self.comVlabel.refresh()
        self.auxVlabel.refresh()
        self.v12Vlabel.refresh()
        self.currentSensorLabel.refresh()
        return 
    


class voltageLabel(tk.Frame):
    
    def __init__(self, aParent, aController, aText, aKey):
        self.parent = aParent
        self.controller = aController
        self.key = aKey
        tk.Frame.__init__(self, self.parent, **SharedDiscoBot.highlightFrameConfig)
        self.nameLabel = tk.Label(self, text=aText, width=4, anchor=tk.W, **SharedDiscoBot.labelConfig)
        self.valueLabel = tk.Label(self, width=5, text="void", **SharedDiscoBot.labelConfig)
        
        self.nameLabel.pack(side=tk.LEFT, anchor=tk.W)
        self.valueLabel.pack(side=tk.LEFT, anchor=tk.W)        
        
        return 
    
    def refresh(self):
        self.valueLabel.config(text='{0:>02.2f}'.format(self.controller.getProperty(self.key)))
        return
    

    