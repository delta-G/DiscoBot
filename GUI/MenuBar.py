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
#     along with this program.  If not, see <http://www.gnu.org/licenses/


import SharedDiscoBot

import tkinter as tk



class MenuBar(tk.Menu):
    
    def __init__(self, aParent, aController):
        self.parent = aParent
        self.controller = aController
        tk.Menu.__init__(self, self.parent, **SharedDiscoBot.menuConfig)
        
############ FILE  #########
        self.filemenu = tk.Menu(self, tearoff=0, **SharedDiscoBot.menuConfig)
        self.filemenu.add_command(label="Say Ni", command=(lambda :print("Ni")))
        self.filemenu.add_command(label="Laugh", command=(lambda :print("HaHa")))
        self.filemenu.add_separator()
        self.filemenu.add_command(label="Exit", command=(lambda :self.controller.endDiscoBot()))
        
        self.add_cascade(label="DiscoBot", menu=self.filemenu)
        
############ RMB COMMANDS
        espCommands = {"Git Hash":"<EG>"}
        self.espmenu = tk.Menu(self, tearoff=0, **SharedDiscoBot.menuConfig)
        for k,v in espCommands.items():
            self.espmenu.add_command(label=k, command=(lambda v=v:self.controller.outPutRunner(v)))
        
        self.add_cascade(label="Comms", menu=self.espmenu)
        
        
############ RMB COMMANDS
        rmbCommands = {"Git Hash":"<R,G>", "Echo123":"<R,E,123>", "Echo456":"<R,E,456>", "Echo789":"<R,E,789>"}
        self.rmbmenu = tk.Menu(self, tearoff=0, **SharedDiscoBot.menuConfig)
        # self.rmbmenu.add_command(label="Git Hash", command=(lambda :self.controller.outPutRunner("<R,G>")))
        for k,v in rmbCommands.items():
            self.rmbmenu.add_command(label=k, command=(lambda v=v:self.controller.outPutRunner(v)))
        
        self.add_cascade(label="MainBrain", menu=self.rmbmenu)

############ ARM COMMANDS
        armCommands = {"Git Hash":"<A,RG>", "Park Arm":"<A,CQ>", "STOP":"<A,CX>"}
        self.armmenu = tk.Menu(self, tearoff=0, **SharedDiscoBot.menuConfig)
        for k,v in armCommands.items():
            self.armmenu.add_command(label=k, command=(lambda v=v:self.controller.outPutRunner(v)))
        
        self.add_cascade(label="Arm", menu=self.armmenu)
        
############ SONAR COMMANDS
        sonCommands = {"Start Sweeping":"<U,C1>", "Stop Sweeping":"<U,C0>", "Park":"<U,Z>"}
        self.sonmenu = tk.Menu(self, tearoff=0, **SharedDiscoBot.menuConfig)
        for k,v in sonCommands.items():
            self.sonmenu.add_command(label=k, command=(lambda v=v:self.controller.outPutRunner(v)))
        
        self.add_cascade(label="Sonar", menu=self.sonmenu)
        
        
        return 
    
    