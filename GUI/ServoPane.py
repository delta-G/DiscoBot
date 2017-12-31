

import Tkinter as tk


class ServoPane(tk.Frame):
    
    
    def __init__(self, aParent, servoList):
        
        self.parent = aParent
        tk.Frame.__init__(self, self.parent, padx=5, pady=5)
        
        self.labels = []
        
        for servo in servoList:
            tmp = OneServo(self, servo)
            self.labels.append(tmp)
            tmp.pack()        
        
        return
    
    def updateData(self):
        
        for l in self.labels:
            l.updateData()        
        return
    

class OneServo(tk.Frame):
    
    def __init__(self, aParent, aServo):
        
        self.parent = aParent
        tk.Frame.__init__(self, self.parent, bd=1, relief=tk.SUNKEN)
        
        self.servo=aServo
                
        self.servoLabel = tk.Label(self, text=str(self.servo.name)+' -- ', pady=5, width=12, font="Verdana 12")
        self.angleLabel = tk.Label(self, text=str(self.servo.position), pady=5, width=5, font="Verdana 12 bold")
        self.servoLabel.pack(side=tk.LEFT)
        self.angleLabel.pack(side=tk.LEFT)        
        
        return
    
    
    def updateData(self):
        self.angleLabel.config(text=str(self.servo.position))
        return
    
    
    
    
    
    
    
    



