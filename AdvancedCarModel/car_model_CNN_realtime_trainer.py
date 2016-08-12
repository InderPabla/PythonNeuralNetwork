from keras.models import Sequential
from keras.layers.core import Dense, Dropout, Activation, Flatten, Merge
from keras.layers import Convolution2D, ZeroPadding2D, MaxPooling2D
from keras.optimizers import SGD
from PIL import Image
import numpy as np 
import os.path
import socket
import struct
import time

def create_model():
    image_model = Sequential()
    image_model.add(ZeroPadding2D((2, 2), batch_input_shape=(1, 3, 50, 50)))   
   
    #54x54 fed in due to zero padding
    image_model.add(Convolution2D(8, 5, 5, activation='relu', name='conv1_1'))
    image_model.add(ZeroPadding2D((2, 2)))
    image_model.add(Convolution2D(8, 5, 5, activation='relu', name='conv1_2'))
    
    image_model.add(MaxPooling2D((2, 2), strides=(2, 2))) #convert 50x50 to 25x25
        
    #25x25 fed in
    image_model.add(ZeroPadding2D((2, 2)))
    image_model.add(Convolution2D(16, 5, 5, activation='relu', name='conv2_1'))
    image_model.add(ZeroPadding2D((2, 2)))
    image_model.add(Convolution2D(16, 5, 5, activation='relu', name='conv2_2'))
    
    image_model.add(MaxPooling2D((5, 5), strides=(5, 5))) #convert 25x25 to 5x5
    
    #5x5 fed in
    image_model.add(ZeroPadding2D((2, 2)))
    image_model.add(Convolution2D(32, 5, 5, activation='relu', name='conv3_1'))
    image_model.add(ZeroPadding2D((2, 2)))
    image_model.add(Convolution2D(32, 5, 5, activation='relu', name='conv3_2'))
    
    image_model.add(Dropout(0.25))
    
    image_model.add(Flatten())
    
    print(image_model.output_shape)
    
    
    multi_layer_model = Sequential()  
    
    multi_layer_model.add(Dense(512, batch_input_shape=(1, 3)))
    multi_layer_model.add(Activation('tanh'))
    multi_layer_model.add(Dense(512))
    multi_layer_model.add(Activation('tanh'))
    
    print(multi_layer_model.output_shape)
    
    merged = Merge([image_model, multi_layer_model], mode='concat')

    final_model = Sequential()
    final_model.add(merged)
    final_model.add(Dense(512))
    final_model.add(Activation('tanh'))
    
    final_model.add(Dense(512))
    final_model.add(Activation('tanh'))
    
    final_model.add(Dense(512))
    final_model.add(Activation('tanh'))
    
    final_model.add(Dense(512))
    final_model.add(Activation('tanh'))
    
    final_model.add(Dense(512))
    final_model.add(Activation('tanh'))
    
    final_model.add(Dense(512))
    final_model.add(Activation('tanh'))
    
    final_model.add(Dense(512))
    final_model.add(Activation('tanh'))
    
    final_model.add(Dense(512))
    final_model.add(Activation('tanh'))
    
    final_model.add(Dense(2))
    final_model.add(Activation('tanh'))  
    
    return final_model

weights_file = "Data3/car_model_CNN_weights.h5"
image_file = "real_time.png"
epoch_count = 1
res_x = 50
res_y = 50
save_counter = 0

model = create_model()

if(os.path.exists(weights_file)):
    print("already exsits")
    model.load_weights(weights_file) 

opt = SGD(lr=0.1, decay=0.000001, momentum=0.9, nesterov=True)
model.compile(loss = "mean_squared_error", optimizer = opt)

 

clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientsocket.connect(('localhost', 12345))

while(True):
    expected_length = 20
    recieved_length = 0
    data = []
    
    while(recieved_length  < expected_length ):
        data = clientsocket.recv(20)
        recieved_length+= len(data)
        
    real_data = []   
    expected_output = []
    #print(len(data))
    if(len(data) == 20):
        a,b,c,d,e = struct.unpack('fffff', bytearray(bytes(data)))
        real_data = np.array([a,b,c],dtype=np.float32)
        expected_output = np.array([d,e],dtype=np.float32)
        #print(real_data)
        #print(expected_output)
        
    stream = Image.open(image_file)
    raw_image_data = list(stream.getdata())
    raw_RGB = [[],[],[]] 
    raw_count = 0
    
    # nested for loop for visual appeal, running (rex_x * rex_y) number of 
    #times
    for y in range(0,res_y):
        
        # extracting RGB, one row at a tile
        red_row = []
        green_row = []
        blue_row = []
    
        #run through rows
        for x in range(0,res_x):
            
            # get RGB values and scale them between 0.0 to 1.0
            red = (raw_image_data[raw_count][0]/255.0)
            green = (raw_image_data[raw_count][1]/255.0)
            blue = (raw_image_data[raw_count][2]/255.0)
                      
            # append RGB to rows
            red_row.append(red)
            green_row.append(green)
            blue_row.append(blue)
            
    
            #increment counter to move to the next data set of tuples
            raw_count = raw_count + 1 
        
        #append RGB rows to their corresponding location in raw RGB array
        raw_RGB[0].append(red_row)
        raw_RGB[1].append(green_row)
        raw_RGB[2].append(blue_row)
      
    train_images_X = []
    train_images_X.append(raw_RGB)
    train_images_X = np.array(train_images_X,dtype = np.float32)  
    
    train_raw_X = []
    train_raw_Y = []
    train_raw_X.append(real_data)
    train_raw_Y.append(expected_output)
    train_raw_X = np.array(train_raw_X, dtype = np.float32) 
    train_raw_Y = np.array(train_raw_Y, dtype = np.float32) 
    
    model.fit([np.array(train_images_X), np.array(train_raw_X)], np.array(train_raw_Y), nb_epoch=epoch_count,verbose = 0) 

    message = str(0.0)+" "+str(0.0)
    
    save_counter = save_counter+1
    print(save_counter)
    if save_counter == 100:
        model.save_weights(weights_file) 
        save_counter = 0
        print("Saved")
    
    clientsocket.send(message.encode())


