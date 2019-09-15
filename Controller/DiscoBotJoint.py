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

class DiscoBotJoint:
    
    def __init__(self, aName, aLength, aOffset, aMinMicros, aMinAngle, aMaxMicros, aMaxAngle ):
        
        self.name = aName
        self.length = aLength
        self.offset = aOffset
        self.minAngle = aMinAngle
        self.minMicros = aMinMicros
        self.maxAngle = aMaxAngle
        self.maxMicros = aMaxMicros
        
        return 
    
    def microsToAngle(self, aMicros):
        
        ratio = 1.0 * (aMicros - self.minMicros) / (self.maxMicros - self.minMicros)
        
        return (ratio * (self.maxAngle - self.minAngle)) + self.minAngle;
        
        
    
    ###  get (x,y) coordinates for end of hypotenuse for a 
    ###  given angle (radians) set at 0,0
    
    def solveTriangle(self, aAngle, aLength):
        x = math.cos(aAngle) * aLength
        y = math.sin(aAngle) * aLength
        return (x,y)
    
    
    def findEndXYandApproach(self, aXYAtuple, aMicros, aRatio):
        
        endAngle = aXYAtuple[2] + self.microsToAngle(aMicros) - 1.5708
        
        xySolution = self.solveTriangle(endAngle, self.length * aRatio)
        
        if self.offset != 0:
            offsetSolution = self.solveTriangle(endAngle + 1.5708, self.offset * aRatio)
            newX = xySolution[0] + offsetSolution[0]
            newY = xySolution[1] + offsetSolution[1]
            xySolution = (newX, newY)
            
        reX = xySolution[0] + aXYAtuple[0]
        reY = xySolution[1] + aXYAtuple[1]
        reA = endAngle
        
        return (reX, reY, reA)
    


    