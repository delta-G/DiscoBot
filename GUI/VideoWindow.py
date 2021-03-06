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


import tkinter as tk
import PIL.Image, PIL.ImageTk
import SharedDiscoBot
import cv2
import time

class VideoWindow(tk.Toplevel):
    
    def __init__(self, aParent, aController, aVidSource=0):
        
        self.controller = aController
        self.parent = aParent
        self.vidSource = aVidSource
        tk.Toplevel.__init__(self, width=200, height=200, **SharedDiscoBot.highlightFrameConfig)
#         self.resizable(0,0)
        self.protocol("WM_DELETE_WINDOW", self.onClose)
        
        self.mainFrame = tk.Frame(self, **SharedDiscoBot.frameConfig)
        self.vidFrame = tk.Frame(self.mainFrame, pady=30, padx=10, **SharedDiscoBot.frameConfig)
        self.buttonFrame = tk.Frame(self.mainFrame, **SharedDiscoBot.frameConfig)
        
        self.cap = Vidcap(self.vidSource)
        
        self.canvas = tk.Canvas(self.vidFrame, width=self.cap.width, height=self.cap.height, **SharedDiscoBot.canvasConfig)
        self.canvas.pack(side=tk.TOP)
        
        self.snapButton = tk.Button(self.buttonFrame, text="Snap", width=5, command=self.snapshot, **SharedDiscoBot.buttonConfig)
        self.snapButton.pack(side=tk.LEFT)
        
        self.mainFrame.pack()
        
        self.vidFrame.pack(side=tk.TOP)
        self.buttonFrame.pack(side=tk.TOP)
        
        return
    
    def snapshot(self):
        ret, frame = self.cap.getFrame()   
        if ret:
            stamp=int(time.time())
            filename="/home/david/robot/001caps/snap"+str(stamp)+".jpg" 
            cv2.imwrite(filename, cv2.cvtColor(frame, cv2.COLOR_RGB2BGR))
        else:
            print("NO FRAME FOR SNAPSHOT!")        
        return 
    
    
    def refresh(self):
        ret, frame = self.cap.getFrame()
        if ret:
            self.image = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(frame))
            self.canvas.create_image(0,0,image=self.image, anchor=tk.NW)
    
    def onClose(self):
        self.parent.videoOpen = False
        self.cap.release()
        self.destroy()
        
    
#     def __del__(self):
#         self.parent.videoOpen = False
#         self.cap.release()
#         return 
    
    
    
    
    
    
class Vidcap():
    def __init__(self, vidSource=0):
        self.vid = cv2.VideoCapture(vidSource)
        
        if not self.vid.isOpened():
            print("VIDEO FAILED TO OPEN")
            
        self.width = self.vid.get(cv2.CAP_PROP_FRAME_WIDTH)
        self.height = self.vid.get(cv2.CAP_PROP_FRAME_HEIGHT)
        
        return 
    
    def getFrame(self):
        if self.vid.isOpened():
            ret, frame = self.vid.read()
            if ret:
                return (ret, cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            else:
                return (ret, None)
        else:
            return (False, None)
    
    def snapshot(self, aFilename):
        ret, frame = self.getFrame()
        
        if ret:
            cv2.imwrite(aFilename, cv2.cvtColor(frame, cv2.COLOR_RGB2BGR))
        else:
            print("NO FRAME FOR SNAPSHOT!")
                
        return 
    
    def release(self):
        if self.vid.isOpened():            
            self.vid.release()
            return 
        
        
        
###  TODO:  See https://stackoverflow.com/questions/14140495/how-to-capture-a-video-and-audio-in-python-from-a-camera-or-webcam
###  for more on finishing the recorder and adding audio to it with ffmpeg
        
# class VideoRecorder():
#     
#     def __init__(self, aVidSource=0):
#         
#         self.open = True
#         self.vidSource = aVidSource
#         self.fps=6
#         self.fourcc="MJPG"
#         self.frameSize=(640,480)
#         self.vidFile="/home/david/robot/VideoTemp/videofile.avi"
#         self.vidcap=Vidcap(0)
#         self.vidWrite=cv2.VideoWriter_fourcc(*self.fourcc)
#         self.vidOut=cv2.VideoWriter(self.vidFile, self.vidWrite, self.fps, self.frameSize)
#         self.frameCount=1
#         
#         return 
#     
#     def record(self):
#         
#         return 
#     
        
        
    


