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


import os
import time
import Tkinter as tk

import Controller.DiscoBotController

import GUI.DiscoBotGUI

logFile = None
# logFile = open("robotLogFile.txt", "w")
#   
# logFile.write("DiscoBot Log File Start:\n")
# logFile.write(str(time.time()))
# logFile.write('\n')


root = tk.Tk()

controller = Controller.DiscoBotController.DiscoBotController(None, logFile)

gui = GUI.DiscoBotGUI.DiscoBotGUI(root, controller)


try:
    
    while (controller.runInterface()):
        gui.refresh()
        root.update_idletasks()
        root.update()
        time.sleep(0.001)
        


finally:
    #Always close out so that xboxdrv subprocess ends
    if controller.comms.commsOn:
        controller.killConnection()
    if logFile is not None:
        logFile.close()
    if controller.joy is not None:
        controller.joy.close()
    os.system('pkill -9 xboxdrv')
    
    print "Done."
    


