

import Tkinter as tk

class TermFrame(tk.Frame):
    
    def __init__(self, aParent):
        
        self.parent = aParent
        tk.Frame.__init__(self, self.parent)
        
        self.scrollbar = tk.Scrollbar(self)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.log = tk.Text(self, width=120, height=45, padx=5, pady=5, takefocus=0, yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.log.yview)
        self.log.pack()    
        
        self.autoscroll = tk.IntVar()
        asCheck = tk.Checkbutton(self, variable=self.autoscroll, text='Auto-Scroll')
        asCheck.select()
        self.ignoreCommand = tk.IntVar()
        icCheck = tk.Checkbutton(self, variable=self.ignoreCommand, text='Ignore-Commands')
        icCheck.select()
        asCheck.pack(side=tk.LEFT)
        icCheck.pack(side=tk.LEFT)
        
        return
    
    
    def redirect(self, aString):
        if self.ignoreCommand.get() == 1:
            if str(aString).startswith('COM-->'):
                return
        self.log.insert(tk.END, str(aString))
        if self.autoscroll.get() == 1:
            self.log.see(tk.END)
        
        return