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

class CommandCheckButton(tk.Checkbutton):
    
    def checkCommand(self):
        if(self.checkVariable.get() == 0):
            self.controller.outPutRunner(self.offCommand)
        else:
            self.controller.outPutRunner(self.onCommand)
        return 
    
    
    def refresh(self):
        self.checkVariable.set(self.controller.getProperty(self.keyword))
        return 
            
    
    def __init__(self, aParent, aController, aText, aKeyword, aOffCommand, aOnCommand):
        
        self.parent = aParent
        self.controller = aController
        self.text = aText
        self.keyword = aKeyword
        self.onCommand = aOnCommand
        self.offCommand = aOffCommand
        self.checkVariable = tk.IntVar()
        tk.Checkbutton.__init__(self, self.parent, text=self.text, command=self.checkCommand, 
                                variable=self.checkVariable, anchor=tk.W, width=9, **SharedDiscoBot.checkboxConfig)
        
        return 
    
    