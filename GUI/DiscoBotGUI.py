import Tkinter as tk

import ServoPane
import TermFrame
import IndicatorFrame
import SelectFrame

class DiscoBotGUI(tk.Frame):
    
    def __init__(self, aParent, aController):
        
        self.parent = aParent
        tk.Frame.__init__(self, self.parent)
        self.controller = aController
        
        self.parent.config(padx=10, pady=10)
        
        self.topFrame = tk.Frame(self)
        
        self.servoPane = ServoPane.ServoPane(self, self.controller.armServos)        
        
               
        
        self.indicatorFrame = IndicatorFrame.IndicatorFrame(self.topFrame, self.controller)
        
        self.seletFrame = SelectFrame.SelectFrame(self.topFrame, self.controller)
        
        self.termFrame = TermFrame.TermFrame(self) 
        
        
        self.indicatorFrame.pack(side=tk.LEFT, anchor=tk.W)
        self.seletFrame.pack(side=tk.LEFT)
        self.topFrame.pack(side=tk.TOP, anchor=tk.W)
        
        self.termFrame.pack(side=tk.LEFT)
        
        self.servoPane.pack(side=tk.TOP)
        
        
        
                
        self.pack()
        return
    
    
    def refresh(self):
        self.servoPane.updateData()
        self.indicatorFrame.check()
        if(self.controller.joyConnected):
            self.seletFrame.controllerConnectButton.config(bg="green")
        else:            
            self.seletFrame.controllerConnectButton.config(bg="red")
                
        if(self.controller.commsOn):
            self.seletFrame.comConnectButton.config(bg="green")
        else:            
            self.seletFrame.comConnectButton.config(bg="red")
        
        
        return


