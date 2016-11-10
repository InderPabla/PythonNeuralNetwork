
from keras.models import Sequential
from keras.layers.core import Dense, Dropout, Activation, Flatten, Merge
from keras.layers import Convolution2D, ZeroPadding2D, MaxPooling2D
import time

def custom_cancer_model():
    cancer_model = Sequential()
    
    cancer_model.add(Dense(1024, input_dim=9))
    cancer_model.add(Activation('sigmoid'))
    
    cancer_model.add(Dense(1024))
    cancer_model.add(Activation('sigmoid'))
    
    cancer_model.add(Dense(1024))
    cancer_model.add(Activation('sigmoid'))
    
    cancer_model.add(Dense(1024))
    cancer_model.add(Activation('sigmoid'))
    
    cancer_model.add(Dense(1024))
    cancer_model.add(Activation('sigmoid'))

    cancer_model.add(Dense(1))
    cancer_model.add(Activation('sigmoid'))  
    
    return cancer_model
    
def make_model(file):
    print("==================================================") 
    
    print("Creating Model At: ",file) 
    start_time = time.time()
    model = custom_cancer_model()    
    
    json_model = model.to_json()
    
    with open(file, "w") as json_file:
        json_file.write(json_model)
    
    end_time = time.time()
    total_time = end_time-start_time
    print("Model Created: ",total_time, " seconds")
    
    print("==================================================")
    

if __name__ == "__main__":   
    make_model("cancer_model.json")
    