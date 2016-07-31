
from PIL import Image
from PIL import ImageGrab
#im=ImageGrab.grab(bbox=(10,30,620,425))


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
import theano.tensor as T

import lasagne
from lasagne import layers

from lasagne.updates import nesterov_momentum

from nolearn.lasagne import NeuralNet
from nolearn.lasagne import visualize

from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix


def multilabel_objective(predictions, targets):
    epsilon = np.float32(1.0e-6)
    one = np.float32(1.0)
    pred = T.clip(predictions, epsilon, one - epsilon)
    return -T.sum(targets * T.log(pred) + (one - targets) * T.log(one - pred), axis=1)
    
def squrcost(predictions, targets):
    return T.sum(((targets - predictions) ** 2)/2)

#Main
if __name__ == '__main__':
    print("-Stating Test-")
        
net1 = NeuralNet(
    layers=[('input', layers.InputLayer),
            
            ('dense1', layers.DenseLayer),

            ('dense2', layers.DenseLayer),

            ('dense3', layers.DenseLayer),

            ('output', layers.DenseLayer),
            ],
            
    # input layer
    input_shape=(None, 3),

    # dense
    dense1_num_units=3,
    dense1_nonlinearity=lasagne.nonlinearities.sigmoid,    
    #dense1_W= lasagne.init.GlorotUniform(), 

    # dense
    dense2_num_units=3,
    dense2_nonlinearity=lasagne.nonlinearities.sigmoid,    
    #dense2_W= lasagne.init.GlorotUniform(), 

     # dense
    dense3_num_units=3,
    dense3_nonlinearity=lasagne.nonlinearities.sigmoid,    
    #dense3_W= lasagne.init.GlorotUniform(), 

    # output
    output_nonlinearity=lasagne.nonlinearities.sigmoid,
    output_num_units=1,
   

    # optimization method params
    #update=nesterov_momentum,
    update_learning_rate=0.1,
    #update_momentum = 0.9,

    regression=True,
    max_epochs=10000,
    verbose=1,
    objective_loss_function=squrcost,
    #custom_score=("validation score", lambda x, y: np.mean(np.abs(x - y))),
    )

t = np.array([[0,0,0],[0,0,1],[0,1,0],[0,1,1],
              [1,0,0],[1,0,1],[1,1,0],[1,1,1],
              [0,0,0],[0,0,1],[0,1,0],[0,1,1],
              [1,0,0],[1,0,1],[1,1,0],[1,1,1]])

a = np.array([[0],[1],[1],[0],[1],[0],[0],[1],
              [0],[1],[1],[0],[1],[0],[0],[1]])

net1.fit(t,a)
pred = net1.predict(t)
print(pred*100)

#im=ImageGrab.grab(bbox=(255,147,355,247))
#im.show()  

#305, 197


#text_file = open("DrivingData\\car_traning_data_1.txt", "w")
#text_file.write("dafadf")
#text_file.close()