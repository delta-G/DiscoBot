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
import ComSenderField

class TermFrame(tk.Frame):
    
    
    def propCom(self):
        if(self.showCommands.get() == 0):
            self.controller.showCommands = False
        else:
            self.controller.showCommands = True
            
        return
    
    def propRet(self):
        if(self.showReturns.get() == 0):
            self.controller.showReturns = False
        else:
            self.controller.showReturns = True
            
        return
    
    def propDeb(self):
        if(self.showDebug.get() == 0):
            self.controller.showDebug = False
        else:
            self.controller.showDebug = True
            
        return
    
    
    
    def __init__(self, aParent):
        
        self.parent = aParent
        tk.Frame.__init__(self, self.parent)
        
        
        self.logFrame = tk.Frame(self)
        self.checkFrame = tk.Frame(self)
        
        self.scrollbar = tk.Scrollbar(self.logFrame)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.autoscroll = tk.IntVar()
        self.showCommands = tk.IntVar()
        self.showReturns = tk.IntVar()
        self.showDebug = tk.IntVar()
        
        asCheck = tk.Checkbutton(self.checkFrame, variable=self.autoscroll, text='Auto-Scroll   ')
        asCheck.select()
        self.comCheck = tk.Checkbutton(self.checkFrame, text="Commands   ", variable=self.showCommands, command=self.propCom)
        self.retCheck = tk.Checkbutton(self.checkFrame, text="Return   ", variable=self.showReturns, command=self.propRet)
        self.debCheck = tk.Checkbutton(self.checkFrame, text="Debug   ", variable=self.showDebug, command=self.propDeb)
        
        asCheck.pack(side=tk.LEFT, anchor=tk.W)
        self.comCheck.pack(side=tk.LEFT, anchor=tk.W)
        self.retCheck.pack(side=tk.LEFT, anchor=tk.W)
        self.debCheck.pack(side=tk.LEFT, anchor=tk.W)
        
        self.comsend = ComSenderField.ComSenderField(self, self.parent.controller)
        self.comsend.pack(side=tk.TOP)
        
        self.log = tk.Text(self.logFrame, width=60, height=20, padx=5, pady=5, takefocus=0, yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.log.yview)
        self.log.pack()    
        
        self.logFrame.pack(side=tk.TOP)
        self.checkFrame.pack(side=tk.TOP, anchor=tk.W)
        
        return
    
    
    def redirect(self, aString):
        self.log.insert(tk.END, str(aString))
        if self.autoscroll.get() == 1:
            self.log.see(tk.END)        
        return