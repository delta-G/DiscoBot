

import Tkinter as tk
import ComSenderField

class TermFrame(tk.Frame):
    
    def __init__(self, aParent):
        
        self.parent = aParent
        tk.Frame.__init__(self, self.parent)
        
        self.scrollbar = tk.Scrollbar(self)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.autoscroll = tk.IntVar()
        asCheck = tk.Checkbutton(self.parent.seletFrame, variable=self.autoscroll, text='Auto-Scroll')
        asCheck.select()
        
        asCheck.pack(side=tk.TOP)
        
        self.comsend = ComSenderField.ComSenderField(self, self.parent.controller)
        self.comsend.pack(side=tk.TOP)
        
        self.log = tk.Text(self, width=60, height=20, padx=5, pady=5, takefocus=0, yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.log.yview)
        self.log.pack()    
        
        
        
        return
    
    
    def redirect(self, aString):
        self.log.insert(tk.END, str(aString))
        if self.autoscroll.get() == 1:
            self.log.see(tk.END)        
        return