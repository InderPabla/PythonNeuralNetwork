from keras.models import Sequential
from keras.layers.core import Dense, Dropout, Activation, Flatten
from keras.layers import Convolution2D, ZeroPadding2D, MaxPooling2D
from keras.optimizers import SGD
from keras import backend as K
from PIL import Image
import numpy as np 
import math
import os.path
from matplotlib.pyplot import imshow
from nolearn.lasagne import visualize

def my_init(shape, name=None):
    value = np.random.random(shape)
    return K.variable(value, name=name)
    
if __name__ == '__main__':
    
    train_answer = []
    with open("DrivingData2\\car_traning_data_keras_1.txt") as f:
        for line in f: 
            answer = []
            numbers_str = line.split()
            numbers_float = [float(x) for x in numbers_str] 
            train_answer.append(numbers_float)
        
    train_answer = np.array(train_answer)
    
    qus = []
    ans = []
    for m in range(0,400):
        file = 'DrivingData2/'+str(m)+'.png'
        im = Image.open(file)
        data = list(im.getdata())
        k = 0
        re_data = [[],[],[]]
         
        for i in range(0,50):
            red_row = []
            green_row = []
            blue_row = []
    
            for j in range(0,50):
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
    
        qus.append(re_data)
        ans.append(train_answer[m])
        
    qus = np.array(qus)   
    ans = np.array(ans)
    
    
    model_state = 2
    
    if model_state == 0:
        model = Sequential()
        model.add(ZeroPadding2D((2, 2), batch_input_shape=(1, 3, 100, 100)))
        
        #100x100 fed in
        model.add(Convolution2D(8, 5, 5,  name='conv1_1'))
        convout1 = Activation('relu')
        model.add(convout1)
        
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
        
        #Set SGD
        opt = SGD(lr=0.0000001, decay=0.0, momentum=0.0, nesterov=False)
        model.compile(loss = "mean_squared_error", optimizer = opt)
        
        if(os.path.exists("DrivingData/car_driving_conv_neural_model.h5")):
            print("already exsits")
            model.load_weights("DrivingData/car_driving_conv_neural_model.h5") 
    
        '''
        for i in range (0,1000):
            rand_in = np.random.randint(0,300)
            model.fit(np.array([qus[rand_in]]), np.array([ans[rand_in]]), nb_epoch=1,verbose = 2) 
            
        '''
        model.fit(qus,ans, nb_epoch=50,verbose = 2) 
        
        pre = model.predict(qus)
        for i in range(0,len(qus)):
            prd = pre[i]*100
            prd[0] = int(prd[0])
            prd[1] = int(prd[1]) 
            
            print(i," ",ans[i]*100," ",prd)
        
        
        model.save_weights("DrivingData/car_driving_conv_neural_model.h5") 
        
        print("Finished")
    
    
    elif model_state == 1:
        model = Sequential()
        
        model.add(ZeroPadding2D((0, 0), batch_input_shape=(1, 3, 100, 100)))
        
        model.add(MaxPooling2D((2, 2), strides=(2, 2)))
        
        #100x100 fed in
        model.add(ZeroPadding2D((2, 2)))
        model.add(Convolution2D(8, 5, 5,  name='conv1_1'))
        convout1 = Activation('relu')
        model.add(convout1)
        
        model.add(ZeroPadding2D((2, 2)))
        model.add(Convolution2D(8, 5, 5, name='conv1_2'))
        convout2 = Activation('relu')
        model.add(convout2)
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
        model.add(Convolution2D(32, 5, 5, name='conv3_2'))
        convout3 = Activation('relu')
        model.add(convout3)

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
        
        
        inpic = np.array(qus[108])
        dt = convout1.activation(inpic)
        print ("________")
        imshow(dt[0])
        imshow(dt[1])
        imshow(dt[2])
        
        ''' 
        opt = SGD(lr=0.1, decay=0.0001, momentum=0.9, nesterov=True)
        model.compile(loss = "mean_squared_error", optimizer = opt)
        
        model.fit(qus,ans, nb_epoch=100,verbose = 2) 
        
        pre = model.predict(qus)
        for i in range(0,len(qus)):
            prd = pre[i]*100
            prd[0] = int(prd[0])
            prd[1] = int(prd[1]) 
            
            print(i," ",ans[i]*100," ",prd)
        
        model.save_weights("DrivingData/car_driving_conv_neural_model_2.h5") 
        ''' 
    elif model_state == 2:
        model = Sequential()
        
        model.add(ZeroPadding2D((2, 2), batch_input_shape=(1, 3, 50, 50)))     
        
        #50x50 fed in
        model.add(Convolution2D(8, 5, 5, name='conv1_1'))
        convout1 = Activation('relu')
        model.add(convout1)
        model.add(ZeroPadding2D((2, 2)))
        model.add(Convolution2D(8, 5, 5, activation='relu', name='conv1_2'))
        
        model.add(MaxPooling2D((2, 2), strides=(2, 2))) #convert 50x50 to 25x25
        
        #25x25 fed in
        model.add(ZeroPadding2D((2, 2)))
        model.add(Convolution2D(16, 5, 5, activation='relu', name='conv2_1'))
        model.add(ZeroPadding2D((2, 2)))
        model.add(Convolution2D(16, 5, 5, activation='relu', name='conv2_2'))
        
        model.add(MaxPooling2D((5, 5), strides=(5, 5))) #convert 25x25 to 5x5
        
        #25x25 fed in
        model.add(ZeroPadding2D((2, 2)))
        model.add(Convolution2D(32, 5, 5, activation='relu', name='conv3_1'))
        model.add(ZeroPadding2D((2, 2)))
        model.add(Convolution2D(32, 5, 5, activation='relu', name='conv3_2'))

        model.add(Dropout(0.25))
        
        model.add(Flatten())
               
        model.add(Dense(512))
        model.add(Activation('tanh'))
        
        model.add(Dense(512))
        model.add(Activation('tanh'))
        
        model.add(Dense(512))
        model.add(Activation('tanh'))
        
        model.add(Dense(512))
        model.add(Activation('tanh'))
        
        model.add(Dense(512))
        model.add(Activation('tanh'))
        
        model.add(Dense(512))
        model.add(Activation('tanh'))
        
        model.add(Dense(512))
        model.add(Activation('tanh'))
        
        model.add(Dense(512))
        model.add(Activation('tanh'))
        
        model.add(Dense(2))
        model.add(Activation('tanh'))  
    
        if(os.path.exists("DrivingData2/car_driving_conv_neural_kreas_model.h5")):
            print("already exsits")
            model.load_weights("DrivingData2/car_driving_conv_neural_kreas_model.h5") 
    
        d = convout1(np.array(qus[200]))
        imshow(d[0])
        imshow(d[1])
        imshow(d[2])
        
        d = convout1(np.array(qus[250]))
        
        imshow(d[0])
        
        opt = SGD(lr=0.001, decay=0.000001, momentum=0.9, nesterov=True)
        model.compile(loss = "mean_squared_error", optimizer = opt)
        
        '''
        for i in range(0,100):
            model.fit(qus,ans, nb_epoch=10,verbose = 2) 
            model.save_weights("DrivingData2/car_driving_conv_neural_kreas_model.h5") 
        '''
        '''
        #print model predictions
        pre = model.predict(qus)
        for i in range(0,len(qus)):
            prd = pre[i]*100
            prd[0] = int(prd[0])
            prd[1] = int(prd[1]) 
            
            print(i," ",ans[i]*100," ",prd)
        '''
    
    
    
    
    
    
    
    
    
    
    
    