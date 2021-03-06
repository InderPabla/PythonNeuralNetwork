from keras.models import Sequential
from keras.layers.core import Dense, Dropout, Activation, Flatten, Merge
from keras.layers import Convolution2D, ZeroPadding2D, MaxPooling2D
from keras.optimizers import SGD
import keras.backend as K
from PIL import Image
import numpy as np 
import os.path
import keras as keras
#from .. import callbacks


class SGDLearningRateTracker(keras.callbacks.Callback):
    def on_epoch_end(self, epoch, logs={}):
        optimizer = self.model.optimizer
        lr = K.eval(optimizer.lr * (1. / (1. + optimizer.decay * optimizer.iterations)))
        print(lr)



'''
get image data, where each image is broken down into it's RGB components and 
each channel is stored seprately
'''
def get_image_data(count,folder,res_x,res_y):
    images = [] # all images will be put here
    
    # run through number of number of images to get
    for i in range(0,count):
        
        file_name = folder+str(i)+'.png' #create file name of get
        stream = Image.open(file_name) #open file  in stream
        
        raw_image_data = list(stream.getdata()) #convert image file to a list
        
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
          
        images.append(raw_RGB) # append broken down RGB array to images
        
    #convert images array to numpy type for theano compatibility   
    images = np.array(images,dtype = np.float32)    

    return images # return images

def get_raw_data(count, raw_file, raw_input_size, raw_output_size):
    raw_X = []
    raw_Y = []
    raw_count = 0
    
    with open(raw_file) as file:
        for line in file: 
            numbers_str = line.split()
            numbers_float = [float(x) for x in numbers_str] 

            X = []
            Y = []
            
            for i in range(0, raw_input_size):
                X.append(numbers_float[i])

            for i in range(raw_input_size, len(numbers_float)):
                Y.append(numbers_float[i])
            
            raw_X.append(X)
            raw_Y.append(Y)
            
            raw_count = raw_count + 1
            
            if raw_count == count:
                break;
                
    raw_X = np.array(raw_X, dtype = np.float32) 
    raw_Y = np.array(raw_Y, dtype = np.float32) 
    return raw_X, raw_Y
    

def create_model_1():
    '''
    image_model = Sequential()
    image_model.add(ZeroPadding2D((2, 2), batch_input_shape=(1, 3, 50, 50)))   
   
    #54x54 fed in due to zero padding
    image_model.add(Convolution2D(10, 5, 5, activation='relu', name='conv1_1'))
    image_model.add(ZeroPadding2D((2, 2)))
    image_model.add(Convolution2D(10, 5, 5, activation='relu', name='conv1_2'))
    
    image_model.add(MaxPooling2D((2, 2), strides=(2, 2))) #convert 50x50 to 25x25
        
    #25x25 fed in
    image_model.add(ZeroPadding2D((2, 2)))
    image_model.add(Convolution2D(20, 5, 5, activation='relu', name='conv2_1'))
    image_model.add(ZeroPadding2D((2, 2)))
    image_model.add(Convolution2D(20, 5, 5, activation='relu', name='conv2_2'))
    
    image_model.add(MaxPooling2D((5, 5), strides=(5, 5))) #convert 25x25 to 5x5
    
    #5x5 fed in
    image_model.add(ZeroPadding2D((2, 2)))
    image_model.add(Convolution2D(40, 5, 5, activation='relu', name='conv3_1'))
    image_model.add(ZeroPadding2D((2, 2)))
    image_model.add(Convolution2D(40, 5, 5, activation='relu', name='conv3_2'))
    
    image_model.add(Dropout(0.25))
    
    image_model.add(Flatten())
    
    print(image_model.output_shape)
    
    
    multi_layer_model = Sequential()  
    
    multi_layer_model.add(Dense(512, batch_input_shape=(1, 1)))
    multi_layer_model.add(Activation('tanh'))
    multi_layer_model.add(Dense(512))
    multi_layer_model.add(Activation('tanh'))
    
    print(multi_layer_model.output_shape)
    
    merged = Merge([image_model, multi_layer_model], mode='concat')

    final_model = Sequential()
    final_model.add(merged)
    final_model.add(Dense(1024))
    final_model.add(Activation('tanh'))
    
    final_model.add(Dense(1024))
    final_model.add(Activation('tanh'))
    
    final_model.add(Dense(1024))
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
      
    final_model.add(Dense(3))
    final_model.add(Activation('sigmoid'))  
    
    return final_model
    '''
    
    
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
    image_model.add(Convolution2D(40, 5, 5, activation='relu', name='conv3_1'))
    image_model.add(ZeroPadding2D((2, 2)))
    image_model.add(Convolution2D(32, 5, 5, activation='relu', name='conv3_2'))
    
    image_model.add(Dropout(0.25))
    
    image_model.add(Flatten())
    
    print(image_model.output_shape)
    
    
    multi_layer_model = Sequential()  
    
    multi_layer_model.add(Dense(512, batch_input_shape=(1, 1)))
    multi_layer_model.add(Activation('tanh'))
    multi_layer_model.add(Dense(512))
    multi_layer_model.add(Activation('tanh'))
    multi_layer_model.add(Dropout(0.25))
    
    print(multi_layer_model.output_shape)
    
    merged = Merge([image_model, multi_layer_model], mode='concat')

    final_model = Sequential()
    final_model.add(merged)
    final_model.add(Dense(512))
    final_model.add(Activation('tanh'))
    final_model.add(Dropout(0.25))
    
    final_model.add(Dense(512))
    final_model.add(Activation('tanh'))
    final_model.add(Dropout(0.25))
    
    final_model.add(Dense(512))
    final_model.add(Activation('tanh'))
    final_model.add(Dropout(0.25))
    
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
    
    final_model.add(Dense(3))
    final_model.add(Activation('sigmoid'))  
    
    return final_model
    
predict_mode = False
load_weights_file = "Data14/car_model_CNN_weights_realtime.h5"
save_weights_file = "Data14/car_model_CNN_weights_realtime.h5"

image_data_location_1 = "Data14/"
raw_data_file_1 = "Data14/raw_data.txt"

image_data_location_2 = "Data13/"
raw_data_file_2 = "Data13/raw_data.txt"

image_data_location_3 = "Data15/"
raw_data_file_3 = "Data15/raw_data.txt"

image_data_location_4 = "Data16/"
raw_data_file_4 = "Data16/raw_data.txt"

image_data_location_5 = "Data17/"
raw_data_file_5 = "Data17/raw_data.txt"

image_data_location_6 = "Data18/"
raw_data_file_6 = "Data18/raw_data.txt"

image_data_location_7 = "Data19/"
raw_data_file_7 = "Data19/raw_data.txt"

image_data_location_8 = "Data20/"
raw_data_file_8 = "Data20/raw_data.txt"

image_data_location_9 = "Data21/"
raw_data_file_9 = "Data21/raw_data.txt"

image_data_location_10 = "Data22/"
raw_data_file_10 = "Data22/raw_data.txt"

image_val_data_location_1 = "Data18/"
raw_val_data_file_1 = "Data18/raw_data.txt"

bactch_itteration_count = 100
epoch_count = 1
res_x = 50
res_y = 50
raw_input_size = 1
raw_output_size = 3

train_image_X_1 = get_image_data(1713,image_data_location_1,res_x,res_y)
train_raw_X_1, train_raw_Y_1 = get_raw_data(1713, raw_data_file_1, raw_input_size, raw_output_size)
print(len(train_raw_X_1)," ",len(train_raw_Y_1)," ",len(train_image_X_1))

train_image_X_2 = get_image_data(1713,image_data_location_2,res_x,res_y)
train_raw_X_2, train_raw_Y_2 = get_raw_data(1713, raw_data_file_2, raw_input_size, raw_output_size)

train_image_X_3 = get_image_data(573,image_data_location_3,res_x,res_y)
train_raw_X_3, train_raw_Y_3 = get_raw_data(573, raw_data_file_3, raw_input_size, raw_output_size)

train_image_X_4 = get_image_data(588,image_data_location_4,res_x,res_y)
train_raw_X_4, train_raw_Y_4 = get_raw_data(588, raw_data_file_4, raw_input_size, raw_output_size)

train_image_X_5 = get_image_data(620,image_data_location_5,res_x,res_y)
train_raw_X_5, train_raw_Y_5 = get_raw_data(620, raw_data_file_5, raw_input_size, raw_output_size)

train_image_X_6 = get_image_data(530,image_data_location_6,res_x,res_y)
train_raw_X_6, train_raw_Y_6 = get_raw_data(530, raw_data_file_6, raw_input_size, raw_output_size)

train_image_X_7 = get_image_data(695,image_data_location_7,res_x,res_y)
train_raw_X_7, train_raw_Y_7 = get_raw_data(695, raw_data_file_7, raw_input_size, raw_output_size)

train_image_X_8 = get_image_data(718,image_data_location_8,res_x,res_y)
train_raw_X_8, train_raw_Y_8 = get_raw_data(718, raw_data_file_8, raw_input_size, raw_output_size)

train_image_X_9 = get_image_data(648,image_data_location_9,res_x,res_y)
train_raw_X_9, train_raw_Y_9 = get_raw_data(648, raw_data_file_9, raw_input_size, raw_output_size)

train_image_X_10 = get_image_data(696,image_data_location_10,res_x,res_y)
train_raw_X_10, train_raw_Y_10 = get_raw_data(696, raw_data_file_10, raw_input_size, raw_output_size)

val_image_X_1 = get_image_data(530,image_val_data_location_1,res_x,res_y)
val_raw_X_1, val_raw_Y_1 = get_raw_data(530,raw_val_data_file_1, raw_input_size, raw_output_size)


model = create_model_1()

if(os.path.exists(load_weights_file)):
    print("already exsits")
    model.load_weights(load_weights_file) 
else:
    print("does not exist")
    
opt = SGD(lr=0.001, decay=0.000001, momentum=0.9, nesterov=True)
model.compile(loss = "mean_squared_error", optimizer = opt)

# THIS MODEL MIGHT BE HARDER THAN REAL SELF DRIVING CAR 
# TRY OUT 64 BIT FLOAT

if predict_mode == False:
    for i in range(0,bactch_itteration_count):
        for j in range(0,1):
            
            model.fit([np.array(train_image_X_1), np.array(train_raw_X_1)], np.array(train_raw_Y_1), nb_epoch=1,verbose = 2,callbacks=[SGDLearningRateTracker()]) 
            model.fit([np.array(train_image_X_2), np.array(train_raw_X_2)], np.array(train_raw_Y_2), nb_epoch=1,verbose = 2,callbacks=[SGDLearningRateTracker()])  
            model.fit([np.array(train_image_X_3), np.array(train_raw_X_3)], np.array(train_raw_Y_3), nb_epoch=1,verbose = 2,callbacks=[SGDLearningRateTracker()]) 
            model.fit([np.array(train_image_X_4), np.array(train_raw_X_4)], np.array(train_raw_Y_4), nb_epoch=1,verbose = 2,callbacks=[SGDLearningRateTracker()]) 
            model.fit([np.array(train_image_X_5), np.array(train_raw_X_5)], np.array(train_raw_Y_5), nb_epoch=1,verbose = 2,callbacks=[SGDLearningRateTracker()]) 
            model.fit([np.array(train_image_X_6), np.array(train_raw_X_6)], np.array(train_raw_Y_6), nb_epoch=1,verbose = 2,callbacks=[SGDLearningRateTracker()]) 
            
            model.fit([np.array(train_image_X_7), np.array(train_raw_X_7)], np.array(train_raw_Y_7), nb_epoch=1,verbose = 2,callbacks=[SGDLearningRateTracker()]) 
            model.fit([np.array(train_image_X_8), np.array(train_raw_X_8)], np.array(train_raw_Y_8), nb_epoch=1,verbose = 2,callbacks=[SGDLearningRateTracker()]) 
            model.fit([np.array(train_image_X_9), np.array(train_raw_X_9)], np.array(train_raw_Y_9), nb_epoch=1,verbose = 2,callbacks=[SGDLearningRateTracker()]) 
            model.fit([np.array(train_image_X_10), np.array(train_raw_X_10)], np.array(train_raw_Y_10), nb_epoch=1,verbose = 2,callbacks=[SGDLearningRateTracker()]) 
       
        model.save_weights(save_weights_file) 
        
        predict_answer = model.predict([np.array(val_image_X_1), np.array(val_raw_X_1)])
         
        for k in range(0,400):
            prediction = predict_answer[k]*100
            prediction[0] = int(prediction[0])
            prediction[1] = int(prediction[1])
            prediction[2] = int(prediction[2])
            
            real = val_raw_Y_1[k]*100
            real[0] = int(real[0])
            real[1] = int(real[1])
            real[2] = int(real[2])
            
            error = real - prediction
            error[0] = abs(error[0])
            error[1] = abs(error[1])
            error[2] = abs(error[2])
            
            real_answer = 0
            if(real[0] == 100):
                real_answer = 0
            if(real[1] == 100):
                real_answer = 1
            if(real[2] == 100):
                real_answer = 2  
                
            prediction_answer = 0
            max_num = 0;
            
            for m in range(len(prediction)):
                if prediction[m] > max_num:
                    max_num = prediction[m]
                    prediction_answer = m
            
            print(k," ",real," ",prediction," ",error," ",real_answer," ",prediction_answer)
        
        
        print("Itteration: ",i," - Model Saved")
else:
    predict_answer = model.predict([np.array(val_image_X_1), np.array(val_raw_X_1)])
    correct = 0.0
    for k in range(0,400):
        prediction = predict_answer[k]*100
        prediction[0] = int(prediction[0])
        prediction[1] = int(prediction[1])
        prediction[2] = int(prediction[2])
        
        real = val_raw_Y_1[k]*100
        real[0] = int(real[0])
        real[1] = int(real[1])
        real[2] = int(real[2])
        
        error = real - prediction
        error[0] = abs(error[0])
        error[1] = abs(error[1])
        error[2] = abs(error[2])
        
        real_answer = 0
        if(real[0] == 100):
            real_answer = 0
        if(real[1] == 100):
            real_answer = 1
        if(real[2] == 100):
            real_answer = 2  
            
        prediction_answer = 0
        max_num = 0;
        
        for m in range(len(prediction)):
            if prediction[m] > max_num:
                max_num = prediction[m]
                prediction_answer = m
        if real_answer == prediction_answer:
            correct = correct + 1
        print(k," ",real," ",prediction," ",error," ",real_answer," ",prediction_answer," ",((correct/400.0)*100.0))
