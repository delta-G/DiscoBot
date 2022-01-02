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
import GUI.IndicatorButton

class SelectFrame(tk.Frame):   
    
    
    def __init__(self, aParent, aController):
        
        self.parent = aParent
        self.controller = aController
        tk.Frame.__init__(self, self.parent, **SharedDiscoBot.frameConfig)
        
        self.checkFrame = tk.Frame(self, **SharedDiscoBot.frameConfig)
        self.checkFrame.pack(side=tk.TOP)
        
        
        self.leftFrame = tk.Frame(self.checkFrame, **SharedDiscoBot.frameConfig)
        self.leftFrame.pack(side=tk.LEFT)
        
        self.rightFrame = tk.Frame(self.checkFrame, **SharedDiscoBot.frameConfig)
        self.rightFrame.pack(side=tk.LEFT)
        
        self.camPowCheck = GUI.IndicatorButton.IndicatorButton(self.leftFrame, self.controller, "Cam", 'cameraPower', "<V0>", "<V1>")
        self.headPowCheck = GUI.IndicatorButton.IndicatorButton(self.leftFrame, self.controller, "Lite", 'headlightPower', "<H0>", "<H1>")
        self.armPowCheck = GUI.IndicatorButton.IndicatorButton(self.leftFrame, self.controller, "Arm", 'armPower', "<QA0>", "<QA1>")
        self.comPowCheck = GUI.IndicatorButton.IndicatorButton(self.leftFrame, self.controller, "Com", 'comPower', "<QR0>", "<QR1>")
        self.armServoPowCheck = GUI.IndicatorButton.IndicatorButton(self.leftFrame, self.controller, "ASe", 'armServoPower', "<A,Cp>", "<A,CP>")
        
        self.motorPowCheck = GUI.IndicatorButton.IndicatorButton(self.rightFrame, self.controller, "Mot", 'motorPower', "<QM0>", "<QM1>")
        self.motorContEnableCheck = GUI.IndicatorButton.IndicatorButton(self.rightFrame, self.controller, "MEn", 'motorContEnable', "<Qm0>", "<Qm1>")
        self.v12PowCheck = GUI.IndicatorButton.IndicatorButton(self.rightFrame, self.controller, "12V", 'v12Power', "<QV0>", "<QV1>")
        self.auxPowCheck = GUI.IndicatorButton.IndicatorButton(self.rightFrame, self.controller, "Aux", 'auxPower', "<Qa0>", "<Qa1>")
        self.sonarPowCheck = GUI.IndicatorButton.IndicatorButton(self.rightFrame, self.controller, "Son", 'sonarPower', "<QS0>", "<QS1>")
        
        
        
        
        

        self.camPowCheck.pack(side=tk.TOP, anchor=tk.W)
        self.headPowCheck.pack(side=tk.TOP, anchor=tk.W)
        self.armPowCheck.pack(side=tk.TOP, anchor=tk.W)
        self.armServoPowCheck.pack(side=tk.TOP, anchor=tk.W)
        self.comPowCheck.pack(side=tk.TOP, anchor=tk.W)
        
        self.motorPowCheck.pack(side=tk.TOP, anchor=tk.W)
        self.motorContEnableCheck.pack(side=tk.TOP, anchor=tk.W)
        self.v12PowCheck.pack(side=tk.TOP, anchor=tk.W)
        self.auxPowCheck.pack(side=tk.TOP, anchor=tk.W)
        self.sonarPowCheck.pack(side=tk.TOP, anchor=tk.W)
        
             
        
        
                
        return
    

    def refresh(self):
        
        self.camPowCheck.refresh()
        self.headPowCheck.refresh()
        self.armPowCheck.refresh()
        self.comPowCheck.refresh()
        self.armServoPowCheck.refresh()
        
        self.motorPowCheck.refresh()
        self.motorContEnableCheck.refresh()
        self.v12PowCheck.refresh()
        self.auxPowCheck.refresh()
        self.sonarPowCheck.refresh()
        
        
    
            
    