from keras.models import model_from_json
from keras.optimizers import SGD, RMSprop
from keras import backend as K
import numpy as np
import os.path


if __name__ == "__main__":
    file_name = "BCdata.asc"
    
    model_path = "cancer_model.json"
    weights_path = "cancer_model_weights.h5"
    weights_path2 = "cancer_model_weights2.h5"
    input_data = []
    output_data = []
    count = 0
    
    with open(file_name) as file:
        for line in file:  
            numbers_str = line.split() #split line data
            
            if(count >= 1):
                
                for i in range (0,len(numbers_str)):
                    if(numbers_str[i] == "NA"):
                        numbers_str[i] = 0        
                    elif(numbers_str[i] == "Ben"):
                        numbers_str[i] = 0
                    elif(numbers_str[i] == "Mal"):
                        numbers_str[i] = 1
                    else: 
                        numbers_str[i] = int(numbers_str[i])
                    
                        
                state = numbers_str[2]
                thickness = numbers_str[3]
                size = numbers_str[4]
                shape = numbers_str[5]            
                adhesion = numbers_str[6]  
                epi = numbers_str[7] 
                bare = numbers_str[8] 
                bland = numbers_str[9] 
                normal = numbers_str[10] 
                mitoses = numbers_str[11] 
                
                input_data.append([thickness, size, shape, adhesion, epi, bare, bland, normal, mitoses]) 
                output_data.append([state])
            
            count = count + 1
            
            
    count = count -1
      
    input_data = np.array(input_data) 
    output_data = np.array(output_data) 
    
    learning_rate = 0.006 #0.006
    decay_rate = 0.000001 #0.00001
    loss_function = "mean_squared_error"
    momen = 0.9
    nest = True
    train_mode = True
    epoch_save = 25
    
    json_file = open(model_path, 'r')
    loaded_model_json = json_file.read()
    json_file.close()  
    cancer_model = model_from_json(loaded_model_json)
    
    if (os.path.exists(weights_path)):
            cancer_model.load_weights(weights_path)
    
    opt = SGD(lr=learning_rate, decay= decay_rate, momentum=momen, nesterov=nest)  
    cancer_model.compile(loss = loss_function , optimizer = opt)
        
    if(train_mode):   
        for i in range(0,40):
            cancer_model.fit(input_data, output_data, nb_epoch=epoch_save,verbose = 2)
            cancer_model.save_weights(weights_path2)
            print("Save: ",i)
    else:
        predict = cancer_model.predict(input_data) * 100
        correct = 0.0
        for i in range(0,len(predict)):
            left = predict[i] - (output_data[i][0]*100.0)
            if(left<0):
                left = left * -1
                
            if(left<5):
                correct = correct + 1.0     
                print(int(predict[i])," ",int(output_data[i][0]*100),"")
            else:
                print(int(predict[i])," ",int(output_data[i][0]*100),"!!!")
            
        acc = (correct/float(len(predict))) * 100
        print(acc)
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    