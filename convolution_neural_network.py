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

def squrcost(predictions, targets):
    return T.sum(((targets - predictions) ** 2)/2)
    
#Main
if __name__ == '__main__':
    print("-Stating Test-")
        
net1 = NeuralNet(
    layers=[('input', layers.InputLayer),
            
            ('conv2d1', layers.Conv2DLayer),

            ('conv2d2', layers.Conv2DLayer),
            
            ('maxpool1', layers.MaxPool2DLayer),
            
            ('conv2d3', layers.Conv2DLayer),

            ('conv2d4', layers.Conv2DLayer),

            ('maxpool2', layers.MaxPool2DLayer),
           
            ('dropout1', layers.DropoutLayer),

            ('dense1', layers.DenseLayer),

            ('dropout2', layers.DropoutLayer),

            ('dropout3', layers.DropoutLayer),

            ('dropout4', layers.DropoutLayer),

            ('output', layers.DenseLayer),
            ],
            
    # input layer
    input_shape=(None, 3, 100, 100),

    # layer conv2d1
    conv2d1_num_filters=10,
    conv2d1_filter_size=(25, 25),
    conv2d1_nonlinearity=lasagne.nonlinearities.sigmoid,
    conv2d1_W=lasagne.init.GlorotUniform(),    
 
    # layer conv2d2
    conv2d2_num_filters=20,
    conv2d2_filter_size=(10, 10),
    conv2d2_nonlinearity=lasagne.nonlinearities.sigmoid,
    conv2d2_W=lasagne.init.GlorotUniform(), 
    
    maxpool1_pool_size=(5, 5),    
    
    # layer conv2d3
    conv2d3_num_filters=40,
    conv2d3_filter_size=(5, 5),
    conv2d3_nonlinearity=lasagne.nonlinearities.sigmoid,
    conv2d3_W=lasagne.init.GlorotUniform(), 

    # layer conv2d4
    conv2d4_num_filters=80,
    conv2d4_filter_size=(3, 3),
    conv2d4_nonlinearity=lasagne.nonlinearities.sigmoid,
    conv2d4_W=lasagne.init.GlorotUniform(), 

    maxpool2_pool_size=(2, 2),    

    # dropout1
    dropout1_p=0.5,    

    # dense
    dense1_num_units=500,
    dense1_nonlinearity=lasagne.nonlinearities.sigmoid,    
    dense1_W= lasagne.init.GlorotUniform(), 

    # dropout2
    dropout2_p=0.5,
    
    # dropout3
    dropout3_p=0.5, 
    
    # dropout4
    dropout4_p=0.5, 
    
    # output
    output_nonlinearity=lasagne.nonlinearities.sigmoid,
    output_num_units=2,
   

    # optimization method params
    update=nesterov_momentum,
    update_learning_rate=0.00001,
    update_momentum=0.9,
    
    regression=True,
    max_epochs=1,
    verbose=1,
    eval_size=0.0,
    #objective_loss_function=squrcost,
    )


train_answer = []
with open("DrivingData\\car_traning_data_1.txt") as f:
    for line in f: 
        answer = []
        numbers_str = line.split()
        numbers_float = [float(x) for x in numbers_str] 
        train_answer.append(numbers_float)
        '''
        index = 0
        if(numbers_float[0] == 0 and numbers_float[1] == 0):
            index = 0
        elif(numbers_float[0] == 1):
            index = 1
        elif(numbers_float[1] == 1):
            index = 2
        train_answer.append(index)
        '''
        
train_answer = np.array(train_answer)


ans = [train_answer[95],train_answer[96],train_answer[97],train_answer[98],
       train_answer[106],train_answer[107],train_answer[108],train_answer[109]]
ans = np.array(ans)

qus = []
for m in range(95,110):
    if(not((m == 99) or (m == 100) or (m == 101) or (m == 102) or (m == 103) or (m == 104) or (m == 105))):
        file = 'DrivingData/'+str(m)+'.png'
        im = Image.open(file)
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
            #re_data.append(green_row)
    
        qus.append(re_data)
    
qus = np.array(qus)   

nn = net1.fit(qus,ans)

preds = net1.predict(qus)
print (m," ",preds)
print (m," ",ans)
