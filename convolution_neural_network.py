import matplotlib
from PIL import Image

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

print("-Stating Test-")

question = []
answer = []
test_question = []
test_answer = []
for m in range(0,74):
    for n in range(0,10):
        file = 'TestData/'+str(m)+'_'+str(n)+'.png'
        im = Image.open(file)
        data = list(im.getdata())
        
        getQ = []
        
        k = 0
        for i in range(0,15):
            row = []
            for j in range(0,15):    
                if(data[k][0] == 0):
                   row.append(1)
                else:
                   row.append(0)
                k = k + 1
            getQ.append(row)
        
        getQ = [getQ]
        question.append(getQ)
        answer.append(n)

for m in range(74,75):
    for n in range(0,10):
        file = 'TestData/'+str(m)+'_'+str(n)+'.png'
        im = Image.open(file)
        data = list(im.getdata())
        
        getQ = []
        
        k = 0
        for i in range(0,15):
            row = []
            for j in range(0,15):    
                if(data[k][0] == 0):
                   row.append(1)
                else:
                   row.append(0)
                k = k + 1
            getQ.append(row)
        
        getQ = [getQ]
        test_question.append(getQ)
        test_answer.append(n)

question = np.array(question)
answer = np.array(answer)

test_question = np.array(test_question)
test_answer = np.array(test_answer)

net1 = NeuralNet(
    layers=[('input', layers.InputLayer),
            ('conv2d1', layers.Conv2DLayer),
            ('maxpool1', layers.MaxPool2DLayer),
            ('conv2d2', layers.Conv2DLayer),
            ('maxpool2', layers.MaxPool2DLayer),
            ('dropout1', layers.DropoutLayer),
            ('dense', layers.DenseLayer),
            ('dropout2', layers.DropoutLayer),
            ('output', layers.DenseLayer),
            ],
    # input layer
    input_shape=(None, 1, 15, 15),
    # layer conv2d1
    conv2d1_num_filters=30,
    conv2d1_filter_size=(3, 3),
    conv2d1_nonlinearity=lasagne.nonlinearities.rectify,
    conv2d1_W=lasagne.init.GlorotUniform(),  
    # layer maxpool1
    maxpool1_pool_size=(2, 2),    
    # layer conv2d2
    conv2d2_num_filters=30,
    conv2d2_filter_size=(3, 3),
    conv2d2_nonlinearity=lasagne.nonlinearities.rectify,
    # layer maxpool2
    maxpool2_pool_size=(2, 2),
    # dropout1
    dropout1_p=0.5,    
    # dense
    dense_num_units=100,
    dense_nonlinearity=lasagne.nonlinearities.rectify,    
    # dropout2
    dropout2_p=0.5,    
    # output
    output_nonlinearity=lasagne.nonlinearities.softmax,
    output_num_units=10,
    # optimization method params
    update=nesterov_momentum,
    update_learning_rate=0.01,
    update_momentum=0.9,
    max_epochs=2,
    verbose=1,
    )
 
print('Traning') 
nn = net1.fit(question,answer)

preds = net1.predict(test_question)
print (preds)

cm = confusion_matrix(test_answer, preds)
plt.matshow(cm)
plt.title('Confusion matrix')
plt.colorbar()
plt.ylabel('True label')
plt.xlabel('Predicted label')
plt.show()

visualize.plot_conv_weights(net1.layers_['conv2d1'])

print("doneee")
