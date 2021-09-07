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

class Gauge(tk.Frame):
    
    def __init__(self, aParent, aController, aLabel, aKeyword):
        self.parent = aParent
        self.controller = aController
        self.label = aLabel
        self.keyword = aKeyword
        self.minVolts = 2
        self.maxVolts = 8
        
        tk.Frame.__init__(self, self.parent)        
        
        self.nameLabel = tk.Label(self, text=aLabel, width=7, anchor=tk.W, **SharedDiscoBot.labelConfig)
        self.gaugeCanvas = tk.Canvas(self, width=50, height=15, bg='red', highlightthickness=1, bd=2)
        
        self.nameLabel.pack(side=tk.LEFT, anchor=tk.W)
        
        self.gaugeCanvas.pack(side=tk.LEFT, anchor=tk.W)
        
        return 
    
    def refresh(self):
        return


