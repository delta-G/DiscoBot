
import os
import time
import Tkinter as tk

import Controller.DiscoBotController

import GUI.DiscoBotGUI

root = tk.Tk()


controller = Controller.DiscoBotController.DiscoBotController()

gui = GUI.DiscoBotGUI.DiscoBotGUI(root, controller)

controller.setRedirect(gui.termFrame.redirect)

# def pyBotRunner():
#     
#     controller.runInterface()
#     gui.refresh()
#     root.after(1, pyBotRunner)
#     return


try:
#     #Valid connect may require joystick input to occur
#     print "Waiting for Joystick to connect"
#     while not controller.joy.connected():
#         time.sleep(0.10)
#         
        
    
    
#     root.after(1, pyBotRunner)
#     root.mainloop()
    
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
    


