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
import SharedDiscoBot


class VoltageFrame(tk.Frame):
    
    def __init__(self, aParent, aController):
        
        self.parent = aParent
        self.controller = aController
        tk.Frame.__init__(self, self.parent, **SharedDiscoBot.frameConfig)
        
        self.batVlabel = voltageLabel(self, self.controller, "Battery", 'batteryVoltage')
        self.motorVlabel = voltageLabel(self, self.controller, "Motor", 'motorVoltage')
        self.mainVlabel = voltageLabel(self, self.controller, "Main", 'mainVoltage')
        self.comVlabel = voltageLabel(self, self.controller, "Com", 'comVoltage')
        self.auxVlabel = voltageLabel(self, self.controller, "Aux", 'auxVoltage')
        self.v12Vlabel = voltageLabel(self, self.controller, "12-Volt", 'v12Voltage')
        
        self.batVlabel.pack(side=tk.TOP, anchor=tk.W)
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
        return 
    


class voltageLabel(tk.Frame):
    
    def __init__(self, aParent, aController, aText, aKey):
        self.parent = aParent
        self.controller = aController
        self.key = aKey
        tk.Frame.__init__(self, self.parent, **SharedDiscoBot.highlightFrameConfig)
        self.nameLabel = tk.Label(self, text=aText, width=7, anchor=tk.W, **SharedDiscoBot.labelConfig)
        self.valueLabel = tk.Label(self, text="void", **SharedDiscoBot.labelConfig)
        
        self.nameLabel.pack(side=tk.LEFT, anchor=tk.W)
        self.valueLabel.pack(side=tk.LEFT, anchor=tk.W)        
        
        return 
    
    def refresh(self):
        self.valueLabel.config(text='{0:>02.3f}'.format(self.controller.getProperty(self.key)))
        return
    

    