

import Tkinter as tk


class ServoPane(tk.Frame):
    
    
    def __init__(self, aParent, servoList):
        
        self.parent = aParent
        tk.Frame.__init__(self, self.parent, padx=5, pady=5)
        
        self.labels = []
        
        count = 0
        
        for servo in servoList:
            tmp = OneServo(self, servo, count)
            self.labels.append(tmp)
            tmp.pack()       
            count += 1 
        
        return
    
    def updateData(self):
        
        for l in self.labels:
            l.updateData()        
        return
    

class OneServo(tk.Frame):
    
    def __init__(self, aParent, aServo, aNum):
        
        self.number = aNum
        self.parent = aParent
        tk.Frame.__init__(self, self.parent, bd=1, relief=tk.SUNKEN)
        
        self.servo=aServo
                
        self.servoLabel = tk.Label(self, text=str(self.servo.name)+' -- ', pady=5, width=12, font="Verdana 12")
        self.positionLabel = tk.Label(self, text=str(self.servo.position), pady=5, width=5, font="Verdana 12 bold")
        self.speedLabel = tk.Label(self, text=str(self.servo.position), pady=5, width=5, font="Verdana 12 bold")
        self.targetLabel = tk.Label(self, text=str(self.servo.position), pady=5, width=5, font="Verdana 12 bold")
        self.servoLabel.pack(side=tk.LEFT)
        self.positionLabel.pack(side=tk.LEFT)
        self.speedLabel.pack(side=tk.LEFT)     
        self.targetLabel.pack(side=tk.LEFT)  
        
        return
    
    
    def updateData(self):
        self.positionLabel.config(text=str(self.parent.parent.controller.servoInfo[self.number][0]))
        self.speedLabel.config(text=str(self.parent.parent.controller.servoInfo[self.number][1]))
        self.targetLabel.config(text=str(self.parent.parent.controller.servoInfo[self.number][2]))
        
        return
    
    
    
    
    
    
    
    



