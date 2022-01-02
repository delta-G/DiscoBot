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

class IndicatorButton(tk.Button):
    
    def onPress(self):
        if(self.controller.getProperty(self.keyword) == 0):
            self.controller.outPutRunner(self.onCommand)
        else:            
            self.controller.outPutRunner(self.offCommand)
        return 
    
    
    def refresh(self):
        if(self.controller.getProperty(self.keyword) == 1):
            self.config(**SharedDiscoBot.greenButton)
        else:
            self.config(**SharedDiscoBot.redButton)
        return
    
    
    def __init__(self, aParent, aController, aText, aKeyword, aOffCommand, aOnCommand):
        
        self.parent = aParent
        self.controller = aController
        self.text = aText
        self.keyword = aKeyword
        self.onCommand = aOnCommand
        self.offCommand = aOffCommand
        tk.Button.__init__(self, self.parent, text=self.text, command=self.onPress, padx=0, pady=0, anchor=tk.W, height=1, width=4, font=('Veranda', '10', 'bold'), **SharedDiscoBot.redButton)
        
        return 
    
    