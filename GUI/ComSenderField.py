

import Tkinter as tk

class ComSenderField(tk.Frame):
    
    def sendCommand(self):
        self.controller.outPutRunner(self.entry.get())
    
    def __init__(self, aParent, aController):
        
        self.parent = aParent
        self.controller = aController
        tk.Frame.__init__(self, self.parent)
        
        self.sendButton = tk.Button(self, text="Send", width=10, command=self.sendCommand)
        self.sendButton.pack(side=tk.RIGHT)
                
        self.entry = tk.Entry(self, width = 40)
        self.entry.pack(side=tk.LEFT, fill=tk.Y)
        
        return 
    
    
    
        
        