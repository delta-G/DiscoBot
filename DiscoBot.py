
import os
import time
import Tkinter as tk
import time

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

controller.setRedirect(gui.termFrame.redirect)


try:
    
    while (controller.runInterface()):
        gui.refresh()
        root.update_idletasks()
        root.update()
        time.sleep(0.001)
        


finally:
    #Always close out so that xboxdrv subprocess ends
    controller.killConnection()
    if logFile is not None:
        logFile.close()
    if controller.joy is not None:
        controller.joy.close()
    os.system('pkill -9 xboxdrv')
    
    print "Done."
    


