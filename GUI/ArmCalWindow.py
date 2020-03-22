#  DiscoBot  --  The Python control software for my robot
#     Copyright (C) 2016  David C.
# 
#     This program is free software: you can redistribute it and/or modify
#     it under the terms of the GNU General Public License as published by
#     the Free Software Foundation, either version 3 of the License, or
#     (at your option) any later version.
# 
#     This program is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#     GNU General Public License for more details.
# 
#     You should have received a copy of the GNU General Public License
#     along with this program.  If not, see <http://www.gnu.org/licenses/>.


import Tkinter as tk

class ArmCalibrationWindowClass(tk.Toplevel):
    
    def __init__(self, aParent, aController):
        
        self.controller = aController
        self.parent = aParent
        tk.Toplevel.__init__(self)
        self.resizable(0,0)
        self.protocol("WM_DELETE_WINDOW", self.onClose)
        self.calFrame = CalFrame(self, self.controller.armJoints)
        
        self.buttonFrame = tk.Frame(self)
        self.getCalButton = tk.Button(self.buttonFrame, text='Get Cal', command=self.getCalibrations)
        self.refreshButton = tk.Button(self.buttonFrame, text='Refresh', command=self.calFrame.updateData)
        
        self.getCalButton.pack(side=tk.LEFT)
        self.refreshButton.pack(side=tk.LEFT)
        
        self.buttonFrame.pack(side=tk.TOP)
        self.calFrame.pack(side=tk.TOP)
        return  
    
    
    def getCalibrations(self):
        self.controller.stopSendingController()
        self.controller.outPutRunner("<A,Rc>")
        return
    
    def onClose(self):
        self.destroy()
        self.parent.calibrationWindowActive = False
        return


        


class CalFrame(tk.Frame):
    
    def __init__(self, aParent, aJointList):
        
        self.parent = aParent
        self.jointList = aJointList
        tk.Frame.__init__(self, self.parent, padx=5, pady=5)
        
        self.labels = []
        
        count = 0
        
        for joint in self.jointList:
            tmp = OneServo(self, joint.name,  count)
            self.labels.append(tmp)
            tmp.pack()
            count += 1
        
#         self.updateData()
        return 
    
    def updateData(self):
        counter = 0
        for joint in self.jointList:
            self.labels[counter].minAngleLabel.config(text = "{0:.4f}".format(joint.minAngle))
            self.labels[counter].maxAngleLabel.config(text = "{0:.4f}".format(joint.maxAngle))
            self.labels[counter].minMicrosLabel.config(text = str(joint.minMicros))
            self.labels[counter].maxMicrosLabel.config(text = str(joint.maxMicros))
            counter += 1
        
        return 


class OneServo(tk.Frame):
    
    def __init__(self, aParent, aName, aNum):
        
        self.number = aNum
        self.parent = aParent
        self.name = aName
        
        tk.Frame.__init__(self, self.parent, bd=1, relief=tk.SUNKEN)
        
        self.nameLabel = tk.Label(self, text=str(self.name), pady=5, width=12, font="Veranda 12")
        self.minAngleLabel = tk.Label(self, text=str(0), pady=5, width=12, font="Veranda 12")
        self.maxAngleLabel = tk.Label(self, text=str(3.1416), pady=5, width=12, font="Veranda 12")
        self.minMicrosLabel = tk.Label(self, text=str(544), pady=5, width=12, font="Veranda 12")
        self.maxMicrosLabel = tk.Label(self, text=str(2400), pady=5, width=12, font="Veranda 12")
        
        
        self.nameLabel.pack(side=tk.LEFT)
        self.minAngleLabel.pack(side=tk.LEFT)
        self.maxAngleLabel.pack(side=tk.LEFT)
        self.minMicrosLabel.pack(side=tk.LEFT)
        self.maxMicrosLabel.pack(side=tk.LEFT)
        
        
        return  
    
    