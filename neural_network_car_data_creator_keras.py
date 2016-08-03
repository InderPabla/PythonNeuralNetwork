
import pyHook, pythoncom, sys

import threading, time

import matplotlib
from PIL import Image
from PIL import ImageGrab

import matplotlib.pyplot as plt
import matplotlib.cm as cm

from urllib.request import urlretrieve
import pickle
import os
import gzip

import numpy as np
import theano

import lasagne
from lasagne import layers
from lasagne.updates import nesterov_momentum

from nolearn.lasagne import NeuralNet
from nolearn.lasagne import visualize

from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix

start_id = 0
exit_id = 0
left_id = 0
right_id = 0


def run():
    hm = pyHook.HookManager()
    hm.KeyDown = OnKeyboardEventDown
    hm.KeyUp = OnKeyboardEventUp
    hm.HookKeyboard()
    pythoncom.PumpMessages()

def ActOnEventDown(event):
    global left_id
    global right_id
    global exit_id
    
    recent_id = event.KeyID

    if(recent_id == 80):
        exit_id = 1
    elif(recent_id == 65):
        left_id = 1
    elif(recent_id == 68):
        right_id = 1

def ActOnEventUp(event):
    global left_id
    global right_id
    
    recent_id = event.KeyID

    if(recent_id == 65):
        left_id = 0
    elif(recent_id == 68):
        right_id = 0

def OnKeyboardEventDown(event):
    threading.Thread(target=ActOnEventDown, args=(event,)).start()
    return True

def OnKeyboardEventUp(event):
    threading.Thread(target=ActOnEventUp, args=(event,)).start()
    return True

def runtime_data():
    text_file = open("DrivingData2\\car_traning_data_keras_1.txt", "w")
    image_file_set = 0
    run_state = True
    print("Starting: ")
    time.sleep(3)
    while run_state:
        time.sleep(0.01)
        
        global left_id
        global right_id
        global exit_id
        
        if(exit_id == 1):
            print("P Pressed - Exiting Thread")
            run_state = False
        else:
            print(image_file_set," --- ",left_id," ",right_id)
            im_name = "DrivingData2\\"+str(image_file_set)+".png"
            
            x = 8
            y = 53
            w = 614
            h = 462
            
            center_x = (w+x)/2
            center_y = (h+y)/2

            im=ImageGrab.grab(bbox=(center_x-100,center_y-100,center_x+100,center_y+100)) 
            im = im.resize((50,50))
            im.save(im_name)
            text_file.write(str(left_id)+" "+str(right_id)+"\n") 
            image_file_set = image_file_set + 1
                
    text_file.close()    
    os._exit()
    
    #os._exit()

#Main
if __name__ == '__main__':
    print("-Stating Test-")
    threading.Thread(target=runtime_data).start()
    run()
    
    



