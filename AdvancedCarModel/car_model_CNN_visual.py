from keras.models import Sequential
from keras.layers.core import Dense, Dropout, Activation, Flatten, Merge
from keras.layers import Convolution2D, ZeroPadding2D, MaxPooling2D
from keras import backend as K
import numpy as np
from scipy.misc import imsave
from PIL import Image


def create_model_1():
    image_model = Sequential()
    image_model.add(ZeroPadding2D((2, 2), batch_input_shape=(1, 3, 50, 50)))   
    first_layer = image_model.layers[-1]
    input_img = first_layer.input
    
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
    
    return final_model,image_model,input_img


final_model,image_model,input_img = create_model_1()


weights_file = "Data11/car_model_CNN_weights.h5"

final_model.load_weights(weights_file) 

print('Model loaded.')

layer_dict = dict([(layer.name, layer) for layer in image_model.layers])
#2-2 4

layer_name = 'conv3_2'
filter_index = 0

for ac in range(0,1):
    filter_index = ac
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
    
    for l in range(0,400):
        print(l)
        file_number = l
        file = 'Data11/'+str(file_number)+'.png'
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
        imsave('Data11/%s_filter_%d_%d.png' % (layer_name, filter_index, file_number), img)














