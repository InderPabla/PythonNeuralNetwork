from keras.models import Sequential
from keras.layers.core import Dense, Dropout, Activation
from keras.optimizers import SGD
from keras import backend as K
import numpy as np 
import math

'''
X = np.array([[0,0],[0,1],[1,0],[1,1]])
y = np.array([[0],[1],[1],[0]])

model = Sequential()
model.add(Dense(8, input_dim=2))
model.add(Activation('tanh'))
model.add(Dense(1))
model.add(Activation('tanh'))

sgd = SGD(lr=0.1)
model.compile(loss='mean_squared_error', optimizer=sgd)

model.fit(X, y, show_accuracy=True, batch_size=1, nb_epoch=1000)
print(model.predict_proba(X))
'''
"""
[[ 0.0033028 ]
 [ 0.99581173]
 [ 0.99530098]
 [ 0.00564186]]
"""


def my_init(shape, name=None):
    value = np.random.random(shape)
    return K.variable(value, name=name)
    
if __name__ == '__main__':
 
    train_answer = []
    with open("DrivingData\\car_traning_data_1.txt") as f:
        for line in f: 
            answer = []
            numbers_str = line.split()
            numbers_float = [float(x) for x in numbers_str] 
            train_answer.append(numbers_float)
    
    
    
    
       
    qus = []
    ans = []
    for m in range(0,300):
         
        file = 'DrivingData/'+str(m)+'.png'
        im = Image.open(file)
        data = list(im.getdata())
        k = 0
        #re_data = [[],[],[]] 
        re_data = []  

        red_row = []
        green_row = []
        blue_row = []
    
        for j in range(0,100):
            red = (data[k][0])
            green = (data[k][1])
            blue = (data[k][2])
    
            red_row.append(red)
            green_row.append(((green+red+blue)/3.0)/255.0)
            blue_row.append(blue)
    
            k = k + 1
            #re_data[0].append(red_row)
            #re_data[1].append(green_row)
            #re_data[2].append(blue_row)
            re_data.append(((green+red+blue)/3.0)/255.0)
        
        qus.append(re_data)
        ans.append(train_answer[m])
        
    qus = np.array(qus)
    ans = np.array(ans)


    model = Sequential()
    model.add(Dense(100, input_dim=100))
    model.add(Activation('tanh'))
    model.add(Dense(100))
    model.add(Activation('tanh'))
    model.add(Dense(100))
    model.add(Activation('tanh'))
    model.add(Dense(100))
    model.add(Activation('tanh'))
    model.add(Dense(100))
    model.add(Activation('tanh'))
    model.add(Dense(50))
    model.add(Activation('tanh'))
    model.add(Dense(50))
    model.add(Activation('tanh'))
    model.add(Dense(50))
    model.add(Activation('tanh'))
    model.add(Dense(10))
    model.add(Activation('tanh'))
    model.add(Dense(10))
    model.add(Activation('tanh'))
    model.add(Dense(2))
    model.add(Activation('tanh'))
    
    #sgd = SGD(lr=0.1)
    #model.compile(loss='mean_squared_error', optimizer=sgd)
    #hist = model.fit(qus, ans, nb_epoch=1000)
    
    opt = SGD(lr=0.1)
    model.compile(loss = "mean_squared_error", optimizer = opt)
    
    
    
    
    hist = model.fit(qus, ans, nb_epoch=1000)    
    
    pre = model.predict(qus)
    for i in range(0,300):
        prd = pre[i]*100
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
            
       
            
        print(ans[i]*100," ",prd)
    
    '''
    sgd = SGD(lr=0.1)
    model.compile(loss='mean_squared_error', optimizer=sgd)
    
    model.fit(qus, ans, show_accuracy=True, batch_size=1, nb_epoch=100)

    pre = model.predict_proba(qus)*100
    
    print(pre," ",ans)
    '''
    
    
    
    