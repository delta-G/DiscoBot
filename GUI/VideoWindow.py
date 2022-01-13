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
        self.protocol("WM_DELETE_WINDOW", self.onClose)
        
        self.mainFrame = tk.Frame(self, **SharedDiscoBot.frameConfig)
        self.vidFrame = tk.Frame(self.mainFrame, pady=30, padx=10, **SharedDiscoBot.frameConfig)
        self.buttonFrame = tk.Frame(self.mainFrame, **SharedDiscoBot.frameConfig)
        
        self.cap = Vidcap(self.vidSource)
        self.recording = False 
        self.vidOut = None 
        self.lastFrame = None
        
        self.canvas = tk.Canvas(self.vidFrame, width=self.cap.width, height=self.cap.height, **SharedDiscoBot.canvasConfig)
        self.canvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        
        self.snapButton = tk.Button(self.buttonFrame, text="Snap", width=5, command=self.snapshot, **SharedDiscoBot.buttonConfig)
        self.snapButton.pack(side=tk.LEFT)
        
        self.recordButton = tk.Button(self.buttonFrame, text="Record", width=7, **SharedDiscoBot.buttonConfig)
        self.recordButton.config(command=self.toggleRecording)
        self.recordButton.pack(side=tk.LEFT)
        
        self.mainFrame.pack(fill=tk.BOTH, expand=True)
        
        self.buttonFrame.pack(side=tk.BOTTOM, anchor=tk.S)
        self.vidFrame.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)
        
        return
    
    def snapshot(self):
        ret, frame = self.cap.getFrame()   
        if ret:
            stamp=int(time.time())
            filename="/home/david/robot/001caps/snap"+str(stamp)+".jpg" 
            cv2.imwrite(filename, frame)
        else:
            print("NO FRAME FOR SNAPSHOT!")        
        return 
    
    def toggleRecording(self):
        
        if self.recording:
            self.vidOut.release()
            self.recording = False
            self.recordButton.config(text="Record")
        else:
            size = (int(self.cap.vid.get(3)), int(self.cap.vid.get(4)))
            stamp=int(time.time())
            filename="/home/david/robot/001caps/snap"+str(stamp)+".mp4" 
            self.recording = True
            self.vidOut = cv2.VideoWriter(filename, cv2.VideoWriter_fourcc(*'mp4v'), 29.97, size)            
            self.recordButton.config(text="Stop")
        return 
    
    
    def refresh(self):
        ret, frame = self.cap.getFrame()
        if ret:
            
            imgw = frame.shape[1]
            imgh = frame.shape[0]
            imgr = imgw / imgh
            
            ##  The 22 and 62 are from the padding on the x and y sides.  Need to get rid of magic numbers. 
            winw = self.vidFrame.winfo_width() - 22
            winh = self.vidFrame.winfo_height() - 62
            winr = winw / winh
            
            neww = imgw
            newh = imgh            
            
            ## if ratio is too small then width is constraining.  If ratio is too large then height is small and constraining
            if(winr < imgr):
                neww = winw
                newh = winw/imgr
            elif(winr > imgr):
                newh = winh
                neww = winh*imgr
            
            newsize = (int(neww), int(newh))            
            reFrame = cv2.resize(frame, newsize)           
            
            self.image = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(cv2.cvtColor(reFrame, cv2.COLOR_BGR2RGB)))
            self.canvas.create_image(winw/2,winh/2,image=self.image, anchor=tk.CENTER)
            self.lastFrame = reFrame
            
            if self.recording:
                self.vidOut.write(frame)
        return
    
    def onClose(self):
        self.parent.videoOpen = False
        self.cap.release()
        if self.vidOut != None:
            self.vidOut.release()
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
                return (ret, frame)
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
        
        
    


