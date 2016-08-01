
from keras.models import Sequential
from keras.layers.core import Dense, Dropout, Activation, Flatten
from keras.layers import Convolution2D, ZeroPadding2D, MaxPooling2D
from keras import backend as K
from PIL import Image
from PIL import ImageGrab
import numpy as np 
import math

import ctypes
from ctypes import wintypes
import time

user32 = ctypes.WinDLL('user32', use_last_error=True)

INPUT_MOUSE    = 0
INPUT_KEYBOARD = 1
INPUT_HARDWARE = 2

KEYEVENTF_EXTENDEDKEY = 0x0001
KEYEVENTF_KEYUP       = 0x0002
KEYEVENTF_UNICODE     = 0x0004
KEYEVENTF_SCANCODE    = 0x0008

MAPVK_VK_TO_VSC = 0

# msdn.microsoft.com/en-us/library/dd375731
VK_TAB  = 0x09
VK_MENU = 0x12
KEY_W = 0x57
KEY_A = 0x41
KEY_D = 0x44

# C struct definitions

wintypes.ULONG_PTR = wintypes.WPARAM

class MOUSEINPUT(ctypes.Structure):
    _fields_ = (("dx",          wintypes.LONG),
                ("dy",          wintypes.LONG),
                ("mouseData",   wintypes.DWORD),
                ("dwFlags",     wintypes.DWORD),
                ("time",        wintypes.DWORD),
                ("dwExtraInfo", wintypes.ULONG_PTR))

class KEYBDINPUT(ctypes.Structure):
    _fields_ = (("wVk",         wintypes.WORD),
                ("wScan",       wintypes.WORD),
                ("dwFlags",     wintypes.DWORD),
                ("time",        wintypes.DWORD),
                ("dwExtraInfo", wintypes.ULONG_PTR))

    def __init__(self, *args, **kwds):
        super(KEYBDINPUT, self).__init__(*args, **kwds)
        # some programs use the scan code even if KEYEVENTF_SCANCODE
        # isn't set in dwFflags, so attempt to map the correct code.
        if not self.dwFlags & KEYEVENTF_UNICODE:
            self.wScan = user32.MapVirtualKeyExW(self.wVk,
                                                 MAPVK_VK_TO_VSC, 0)

class HARDWAREINPUT(ctypes.Structure):
    _fields_ = (("uMsg",    wintypes.DWORD),
                ("wParamL", wintypes.WORD),
                ("wParamH", wintypes.WORD))

class INPUT(ctypes.Structure):
    class _INPUT(ctypes.Union):
        _fields_ = (("ki", KEYBDINPUT),
                    ("mi", MOUSEINPUT),
                    ("hi", HARDWAREINPUT))
    _anonymous_ = ("_input",)
    _fields_ = (("type",   wintypes.DWORD),
                ("_input", _INPUT))

LPINPUT = ctypes.POINTER(INPUT)

def _check_count(result, func, args):
    if result == 0:
        raise ctypes.WinError(ctypes.get_last_error())
    return args

user32.SendInput.errcheck = _check_count
user32.SendInput.argtypes = (wintypes.UINT, # nInputs
                             LPINPUT,       # pInputs
                             ctypes.c_int)  # cbSize

# Functions

def PressKey(hexKeyCode):
    x = INPUT(type=INPUT_KEYBOARD,
              ki=KEYBDINPUT(wVk=hexKeyCode))
    user32.SendInput(1, ctypes.byref(x), ctypes.sizeof(x))

def ReleaseKey(hexKeyCode):
    x = INPUT(type=INPUT_KEYBOARD,
              ki=KEYBDINPUT(wVk=hexKeyCode,
                            dwFlags=KEYEVENTF_KEYUP))
    user32.SendInput(1, ctypes.byref(x), ctypes.sizeof(x))

def AltTab():
    """Press Alt+Tab and hold Alt key for 2 seconds
    in order to see the overlay.
    """
    PressKey(VK_MENU)   # Alt
    PressKey(VK_TAB)    # Tab
    ReleaseKey(VK_TAB)  # Tab~
    time.sleep(2)
    ReleaseKey(VK_MENU) # Alt~


time.sleep(3)

model_state = 1
    
if model_state == 0:
    model = Sequential()
    model.add(ZeroPadding2D((2, 2), batch_input_shape=(1, 3, 100, 100)))
    
    #100x100 fed in
    model.add(Convolution2D(8, 5, 5, activation='relu', name='conv1_1'))
    model.add(ZeroPadding2D((2, 2)))
    model.add(Convolution2D(8, 5, 5, activation='relu', name='conv1_2'))
    
    model.add(MaxPooling2D((2, 2), strides=(2, 2))) #convert 100x100 to 50x50
    
    #50x50 fed in
    model.add(Convolution2D(16, 5, 5, activation='relu', name='conv2_1'))
    model.add(ZeroPadding2D((2, 2)))
    model.add(Convolution2D(16, 5, 5, activation='relu', name='conv2_2'))
    
    model.add(MaxPooling2D((2, 2), strides=(2, 2))) #convert 50x50 to 25x25   
    
    #25x25 fed in
    model.add(Convolution2D(32, 5, 5, activation='relu', name='conv3_1'))
    model.add(ZeroPadding2D((2, 2)))
    model.add(Convolution2D(32, 5, 5, activation='relu', name='conv3_2'))
    
    model.add(MaxPooling2D((5, 5), strides=(5, 5))) #convert 25x25 to 5x5
     
    model.add(Dropout(0.25))
    
    model.add(Flatten())
    
    model.add(Dense(512))
    model.add(Activation('tanh'))
    
    model.add(Dense(100))
    model.add(Activation('tanh'))
    
    model.add(Dense(100))
    model.add(Activation('tanh'))
    
    model.add(Dense(2))
    model.add(Activation('sigmoid')) 
    
    model.load_weights("DrivingData/car_driving_conv_neural_model.h5") 
    
elif model_state == 1:
    model = Sequential()
        
    model.add(ZeroPadding2D((0, 0), batch_input_shape=(1, 3, 100, 100)))
    
    model.add(MaxPooling2D((2, 2), strides=(2, 2)))
    
    #100x100 fed in
    model.add(ZeroPadding2D((2, 2)))
    model.add(Convolution2D(8, 5, 5, activation='relu', name='conv1_1'))
    model.add(ZeroPadding2D((2, 2)))
    model.add(Convolution2D(8, 5, 5, activation='relu', name='conv1_2'))

    model.add(MaxPooling2D((2, 2), strides=(2, 2))) #convert 100x100 to 50x50
    
    #50x50 fed in
    model.add(ZeroPadding2D((2, 2)))
    model.add(Convolution2D(16, 5, 5, activation='relu', name='conv2_1'))
    model.add(ZeroPadding2D((2, 2)))
    model.add(Convolution2D(16, 5, 5, activation='relu', name='conv2_2'))
    
    model.add(MaxPooling2D((5, 5), strides=(5, 5)))
    
    #25x25 fed in
    model.add(ZeroPadding2D((2, 2)))
    model.add(Convolution2D(32, 5, 5, activation='relu', name='conv3_1'))
    model.add(ZeroPadding2D((2, 2)))
    model.add(Convolution2D(32, 5, 5, activation='relu', name='conv3_2'))


    model.add(Dropout(0.25))
    
    model.add(Flatten())
    
    model.add(Dense(512))
    model.add(Activation('tanh'))
    
    model.add(Dense(100))
    model.add(Activation('tanh'))
    
    model.add(Dense(100))
    model.add(Activation('tanh'))
    
    model.add(Dense(100))
    model.add(Activation('tanh'))
    
    model.add(Dense(100))
    model.add(Activation('tanh'))
    
    model.add(Dense(100))
    model.add(Activation('tanh'))
    
    model.add(Dense(100))
    model.add(Activation('tanh'))
    
    model.add(Dense(2))
    model.add(Activation('sigmoid'))  
    
    model.load_weights("DrivingData/car_driving_conv_neural_model_2.h5") 
        
while True:
    im = ImageGrab.grab(bbox=[255,147,355,247])
    data = list(im.getdata())
    k = 0
    re_data = [[],[],[]]
     
    for i in range(0,100):
        red_row = []
        green_row = []
        blue_row = []

        for j in range(0,100):
            red = (data[k][0]/255.0)
            green = (data[k][1]/255.0)
            blue = (data[k][2]/255.0)

            red_row.append(red)
            green_row.append(green)
            blue_row.append(blue)

            k = k + 1
        re_data[0].append(red_row)
        re_data[1].append(green_row)
        re_data[2].append(blue_row)
    
    re_data = np.array([re_data])
    pre = model.predict(re_data)
    
    
    prd = pre[0]*100
    prd[0] = int(prd[0])
    prd[1] = int(prd[1])
    if(prd[0]>85):
        prd[0] = 100
    else:
        prd[0] = 0
        
    if(prd[1]>85):
        prd[1] = 100
    else:
        prd[1] = 0
    
    print(prd)
    
    
    if(prd[0] ==0 and prd[1]==0):
        ReleaseKey(KEY_A)  
        ReleaseKey(KEY_D)
    elif(prd[0]==100):
        PressKey(KEY_A) 
        ReleaseKey(KEY_D)
    elif(prd[1]==100):
         PressKey(KEY_D) 
         ReleaseKey(KEY_A)
      
    #time.sleep(0.01)
