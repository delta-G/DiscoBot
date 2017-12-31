#  pyBot  --  The Python control software for my robot
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

import math


class DiscoBotServo:
    
    def __init__(self, name, initial, minimum, maximum):
        
        self.name = name
        self.minimum = minimum
        self.maximum = maximum
        self.minimumAngle = 0
        self.maximumAngle = math.pi
        self.target = initial
        self.position = initial
        self.incrementSpeed = 10
        
        return
    
    ### Takes angle in radians
    def angleToMicroseconds(self, aAngle):
        return ((aAngle / math.pi) * (self.maximum - self.minimum)) + self.minimum
    
    def scalePosition(self):
        if self.position > self.maximum:
            self.position = self.maximum
        elif self.position < self.minimum:
            self.position = self.minimum
        return
    
    def scaleTarget(self):
        if self.target > self.maximum:
            self.target = self.maximum
        elif self.target < self.minimum:
            self.target = self.minimum
        return
        
    def moveTo(self, posit):
        self.target = posit
        self.scaleTarget()
        return
    
    def moveToImmediate(self, posit):
        self.position = posit
        self.scalePosition()
        return
    
    def increase(self):
        self.position = self.position + 1
        self.scalePosition()
        return
    
    def decrease(self):
        self.position = self.position - 1
        self.scalePosition()
        return
    
    def increment(self, stickPosition):
        amt = self.incrementSpeed * stickPosition        
        self.moveToImmediate(int(self.position + amt))
        return
    
    