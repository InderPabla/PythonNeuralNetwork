from keras.models import Sequential
from keras.layers.core import Dense, Dropout, Activation, Flatten
from keras.layers import Convolution2D, ZeroPadding2D, MaxPooling2D
from keras import backend as K
import numpy as np
from scipy.misc import imsave
from PIL import Image

model = Sequential()
        
model.add(ZeroPadding2D((2, 2), batch_input_shape=(1, 3, 50, 50)))     
first_layer = model.layers[-1]
# this is a placeholder tensor that will contain our generated images
input_img = first_layer.input


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
model.add(Convolution2D(32, 5, 5,name='conv3_1'))
convout3 = Activation('relu')
model.add(convout3)
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


weights_path = 'DrivingData2/car_driving_conv_neural_kreas_model.h5'

model.load_weights(weights_path) 

print('Model loaded.')

layer_dict = dict([(layer.name, layer) for layer in model.layers])


layer_name = 'conv1_2'
filter_index = 3

# build a loss function that maximizes the activation
# of the nth filter of the layer considered
layer_output = layer_dict[layer_name].output
loss = K.mean(layer_output[:, filter_index, :, :])

# compute the gradient of the input picture wrt this loss
grads = K.gradients(loss, input_img)[0]

# normalization trick: we normalize the gradient
grads /= (K.sqrt(K.mean(K.square(grads))) + 1e-5)

# this function returns the loss and grads given the input picture
iterate = K.function([input_img], [loss, grads])






input_img_data = np.random.random((1, 3, 50, 50)) * 20 + 50.
# run gradient ascent for 20 steps
for i in range(20):
    loss_value, grads_value = iterate([input_img_data])
    input_img_data += grads_value * 20

def deprocess_image(x):
    # normalize tensor: center on 0., ensure std is 0.1
    x -= x.mean()
    x /= (x.std() + 1e-5)
    x *= 0.1

    # clip to [0, 1]
    x += 0.5
    x = np.clip(x, 0, 1)

    # convert to RGB array
    x *= 255
    x = x.transpose((1, 2, 0))
    x = np.clip(x, 0, 255).astype('uint8')
    return x

file_number = 0
for l in range(0,1):
    print(l)
    file_number = l
    file = 'DrivingData2/'+str(file_number)+'.png'
    im = Image.open(file)
    data = list(im.getdata())
    
    re_data = [[],[],[]]
    k = 0  
    for i in range(0,50):
        red_row = []
        green_row = []
        blue_row = []
    
        for j in range(0,50):
            red = data[k][0]/1.0
            green = data[k][1]/1.0
            blue = data[k][2]/1.0
    
            red_row.append(red)
            green_row.append(green)
            blue_row.append(blue)
    
            k = k + 1
        re_data[0].append(red_row)
        re_data[1].append(green_row)
        re_data[2].append(blue_row)
    
    re_data = np.array([re_data])
    
    for i in range(25):
        loss_value, grads_value = iterate([re_data])
        re_data += grads_value * 20
    
        
    #img = input_img_data[0]
    img = re_data[0]
        
    img = deprocess_image(img)
    imsave('DrivingData2/%s_filter_%d_%d.png' % (layer_name, filter_index, file_number), img)














