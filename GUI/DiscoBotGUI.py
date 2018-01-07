import Tkinter as tk

import ServoPane
import TermFrame
import IndicatorFrame

class DiscoBotGUI(tk.Frame):
    
    def __init__(self, aParent, aController):
        
        self.parent = aParent
        tk.Frame.__init__(self, self.parent)
        self.controller = aController
        
        self.parent.config(padx=10, pady=10)
        
        self.servoPane = ServoPane.ServoPane(self, self.controller.armServos)        
        
        self.termFrame = TermFrame.TermFrame(self)        
        
        self.indicatorFrame = IndicatorFrame.IndicatorFrame(self, self.controller)
        
        
        self.indicatorFrame.pack(side=tk.TOP, anchor=tk.W)
        
        self.termFrame.pack(side=tk.LEFT)
        
        self.servoPane.pack(side=tk.TOP)
        
                
        self.pack()
        return
    
    
    def refresh(self):
        self.servoPane.updateData()
        self.indicatorFrame.check()
        


