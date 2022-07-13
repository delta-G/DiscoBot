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

colors = {
            'red' : '#FF0000',
            'green' : '#00FF00',
            'yellow' : '#FFFF00',
            'highlight' : 'blue'
            }

defaultFont = "Veranda 12 bold"

canvasConfig = {'bg':'black', 'highlightthickness':1, 'highlightbackground':colors['highlight']}

labelConfig = {'bg':'black' , 'fg':'white', 'highlightthickness':1, 'highlightbackground':colors['highlight']}
highlightLabelConfig = {'bg':'black' , 'fg':'white', 'highlightthickness':1, 'highlightbackground':colors['highlight']}

entryConfig = {'bg':'black' , 'fg':'white', 'highlightbackground':colors['highlight'], 'insertbackground':'white', 'insertwidth':'2'}

textboxConfig = {'bg':'black' , 'fg':'white', 'highlightbackground':colors['highlight']}

buttonConfig = {'bg':'black' , 'fg':'white', 'highlightbackground':colors['highlight']}
redButton = {'bg':colors['red'] , 'fg':'black', 'highlightbackground':colors['highlight']}
greenButton = {'bg':colors['green'] , 'fg':'black', 'highlightbackground':colors['highlight']}

frameConfig = {'bg':'black'}
highlightFrameConfig = {'bg':'black', 'highlightthickness':1,  'highlightbackground':colors['highlight']}

checkboxConfig = {'bg':'black', 'fg':'white', 'highlightthickness':1,  'highlightbackground':colors['highlight'], 'selectcolor':colors['highlight']}

spinboxConfig = {'bg':'black', 'fg':'white', 'highlightthickness':1,  'highlightbackground':colors['highlight']}


errorText = {1:"Self Test Fail", 
                 10:"Bad Raw Input", 
                 11:"xpander SPI fail", 
                 12:"powerXpander SPI fail", 
                 13:"powerADC SPI fail",
                 19:"Fake Error Code",
                 101:"Arm Boot Timeout",
                 127:"Bad Error Code"
                 }


#####END