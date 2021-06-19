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

import math
import numpy as np

a1 = 240.0  # height of shoulder at rotation
a2 = 103.0  # length of upper arm
a3 = 97.0  # length of forearm
a4 = 165.0  #length of gripper
a5 = 31.0  # offset of gripper at pi/2 to length


def runInverse(x, y, z, a):
    
    
### Calculate the base angle
    # this one is the easy part.
    
    baseTheta = np.arctan(y/x)
    baseServo = baseTheta + (np.pi/2)
    
    
### Step 2 Calculate wrist position
    
    # for the first bit we will assume we are in a 2D frame and go from there
    # We will consider this the r-z frame where r is the distance projection in
    # the x-y plane.  Think the r in polar coordinates.
    # a should be defined as the angle of the gripper from the 
    # x-y plane  So 0 is horizontal and negative values are tip down
    # and positive values are tip up
    
    phi = a
    rdisp = (np.cos(phi) * a4) - (np.sin(phi) * a5)   ## Displacement in radial direction from wrist to tip
    zdisp = (np.sin(phi) * a4) + (np.cos(phi) * a5)   ## Displacement in the Z direction from wrist to tip
    
    
    
    rtip = np.sqrt((x*x)+(y*y))
    
    print "rdisp: ", rdisp
    print "zdisp: ", zdisp
    print "rtip: ", rtip
    
    rwrist = rtip - rdisp
    zwrist = z-zdisp
    
    print "rwrist: ", rwrist
    print "zwrist: ", zwrist
    
    
### Step 3 Calculate distance from wrist to base

    
    dwr = np.sqrt((rwrist*rwrist)+((zwrist-a1)*(zwrist-a1)))

### Step 4 Calculate elbow angle

    cosElbow = ((a2*a2) + (a3*a3) - (dwr*dwr)) / (2*a2*a3)
    
    print "cosElbow: ", cosElbow
    
    elbowTheta = np.arccos(cosElbow)
    elbowServo = elbowTheta - (np.pi/2)
    
### Step 5 Set Shoulder to get Z

    ### The angle up from shoulder to wrist (up from xy plane)
    t1 = np.arctan((zwrist-a1)/rwrist)

    ### and the inside angle of the triangle made by a2 and a3 and dw (rest of way to shoulder)
    ct2 = ((a2*a2) + (dwr*dwr) - (a3*a3)) / (2*a2*dwr)
    t2 = np.arccos(ct2)
    
    shoulderTheta = t1+t2
    shoulderServo = shoulderTheta
    
    print "t1: ", t1
    print "ct2: ", ct2
    print "t2: ", t2
    
### Step 6 Set wrist to get gripper angle

    # The angle that the forearm is sitting
    forang = shoulderTheta + elbowTheta - np.pi
    wristTheta = phi - forang + np.pi
    wristServo = wristTheta - (np.pi/2)
    
    print "forang: ", forang
    print "wristTheta: ", wristTheta
    
    
    
    print "Results:"
    print "Base: ",baseTheta
    print "Shoulder: ",shoulderTheta
    print "Elbow: ",elbowTheta
    print "Wrist: ",wristTheta
    
    print "Servos:"
    print "Base: ",baseServo
    print "Shoulder: ",shoulderServo
    print "Elbow: ",elbowServo
    print "Wrist: ",wristServo
    
    return



def findEndEffectorTip(theta1, theta2, theta3, theta4):
    
    ### Find the x coordinate
    s1 = math.sin(theta1)
    s2 = math.sin(theta2)
    s3 = math.sin(theta3)
    s4 = math.sin(theta4)    
    c1 = math.cos(theta1)
    c2 = math.cos(theta2)
    c3 = math.cos(theta3)
    c4 = math.cos(theta4)
    s2s3 = s2*s3
    c2c3 = c2*c3
    s2c3 = s2*c3
    c2s3 = c2*s3
    x4 = (a4*c4) - (a5*s4)
    y4 = (a4*s4) + (a5*c4)
    
    xCoord = s1 * ( ((s2s3-c2c3)*x4) + ((s2c3+c2s3)*y4) + (a3 * (s2c3 + c2s3)) + (a2 * c2))
    
    yCoord = (0-c1) * (((s2s3-c2c3)*x4) + ((s2c3+c2s3)*y4) + (a3*(s2c3+c2s3)) + (a2*c2))
    
    zCoord = ((0-c2s3-s2c3)*x4) + ((s2s3-c2c3)*y4) + (a3*(s2s3-c2c3)) + (a2*s2) + a1
    
    zproj = (c4*(0-c2s3-s2c3)) + (s4*(s2s3-c2c3))
    phi = np.arcsin(zproj)
    
    
    
    return (xCoord, yCoord, zCoord, phi)
