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

class ComSenderField(tk.Frame):
    
    def sendCommand(self):
        self.controller.outPutRunner(self.entry.get())
    
    def __init__(self, aParent, aController):
        
        self.parent = aParent
        self.controller = aController
        tk.Frame.__init__(self, self.parent)
        
        self.sendButton = tk.Button(self, text="Send", width=10, command=self.sendCommand, **SharedDiscoBot.buttonConfig)
        self.sendButton.pack(side=tk.RIGHT)
                
        self.entry = tk.Entry(self, width = 40, **SharedDiscoBot.entryConfig)
        self.entry.pack(side=tk.LEFT, fill=tk.Y)
        
        return 
    
    
    
        
        