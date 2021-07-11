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

import time

class DiscoBotLogger:
    
    def __init__(self):
        
        self.fileName = "/home/david/robot/DiscoBot/LogFiles/DiscoBot_" + str(time.time()) + "_LogFile.txt"
        self.logFile = None
        self.logOpen = False
        self.loggingLevel = 0
                
        return 
    
    def openLogFile(self, aLevel=1):
        try:
            self.logFile = open(self.fileName, "w")
            
        except Exception as ex:
            self.logOpen=False
            print("FILE ERROR::")
            print(ex)
            
        else:
            self.logFile.write("DiscoBot Log File Start:\n")
            self.logFile.write(str(time.time()))
            self.logFile.write('\n')
            self.loggingLevel = aLevel
            self.logOpen = True
        
        return 
    
    def closeLogFile(self):
        if self.logOpen:
            self.logOpen = False
            self.logFile.write("Closing Log")
            self.logFile.close()
        return 
    
    def logString(self, cs, level=0):
        if self.logOpen and level >= self.loggingLevel:
            self.logFile.write(str(time.time()))
            self.logFile.write(" :")
            self.logFile.write(str(level))
            self.logFile.write(": ")
            self.logFile.write(str(cs))
            self.logFile.write("\n")
        
        return 
    
    def logByteArray(self, aLabel, aByteArray, level=0):
        if self.logOpen and level >= self.loggingLevel:
            self.logFile.write(str(time.time()))
            self.logFile.write(" :")
            self.logFile.write(str(level))
            self.logFile.write(": ")
            self.logFile.write(str(aLabel))
            for val in aByteArray:
                self.logFile.write(hex(val))
                self.logFile.write(" ")
            self.logFile.write("\n")
        
        return 
    
    def setLoggingLevel(self, aLevel):
        self.loggingLevel = aLevel
        return
    
    
    
    
        
        
        
        