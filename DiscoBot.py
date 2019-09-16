
import os
import time
import Tkinter as tk

import Controller.DiscoBotController

import GUI.DiscoBotGUI

root = tk.Tk()


controller = Controller.DiscoBotController.DiscoBotController()

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
    if controller.joyConnected:
        controller.joy.close()
    os.system('pkill -9 xboxdrv')
    
    print "Done."
    


