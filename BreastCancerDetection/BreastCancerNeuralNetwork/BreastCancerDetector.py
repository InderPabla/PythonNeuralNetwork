from keras.models import model_from_json
from keras.optimizers import SGD
import numpy as np
import os.path


if __name__ == "__main__":
    file_name = "BCdata.asc"
    
    model_path = "cancer_model.json"
    weights_path = "cancer_model_weights.h5"
    prediction_path = "prediction.txt"
    
    all_input_data = []
    all_output_data = []
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
                
                all_input_data.append([thickness, size, shape, adhesion, epi, bare, bland, normal, mitoses]) 
                
                if state == 0:
                    all_output_data.append([1,0])
                else :
                    all_output_data.append([0,1])
            
            count = count + 1
            
            
    count = count -1
    
    partition = 0.5
    train_input_data = []
    test_input_data = []
    train_output_data = []
    test_output_data = []
    
    for i in range(0,int(len(all_input_data)*partition)):
        train_input_data.append(all_input_data[i])  
        train_output_data.append(all_output_data[i])
        
    for i in range(int(len(all_input_data)*partition),len(all_input_data)):
        test_input_data.append(all_input_data[i])  
        test_output_data.append(all_output_data[i])  
      
      
    all_input_data = np.array(all_input_data)    
    test_input_data = np.array(test_input_data)
    train_input_data = np.array(train_input_data)   
     
    all_output_data = np.array(all_output_data) 
    test_output_data = np.array(test_output_data) 
    train_output_data = np.array(train_output_data) 
    
    
    
    learning_rate = 0.06 #0.06
    decay_rate = 0.000001 #0.00001
    loss_function = "mean_squared_error"
    momen = 0.9
    nest = True
    train_mode = False
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
            cancer_model.fit(train_input_data, train_output_data, nb_epoch=epoch_save,verbose = 2)
            cancer_model.save_weights(weights_path)
            print("Save: ",i)
    else:
        
        #file = open(prediction_path, 'w')
        predict = cancer_model.predict(all_input_data)
        correct = 0.0
        error = 0.0
        for i in range(0,len(predict)):
            hasEmptyField = False
            correctAnswer = False
            expected_out = all_output_data[i]
            real_out = predict[i]
            
            if(expected_out[0]>expected_out[1] and real_out[0]>real_out[1] ):
                correct = correct + 1.0
                correctAnswer = True
            elif(expected_out[0]<expected_out[1] and real_out[0]<real_out[1]):
                correct = correct + 1.0
                correctAnswer = True
            error = error + (abs(expected_out[0]-real_out[0]) + abs(expected_out[1]-real_out[1]))/2.0
            
            expected_out = expected_out*100
            expected_out[0] = int(expected_out[0])
            expected_out[1] = int(expected_out[1])
            
            real_out = real_out*100
            real_out[0] = int(real_out[0])
            real_out[1] = int(real_out[1])

            for j in range(0,9):
                if(all_input_data[i][j] == 0):
                    hasEmptyField = True
                    break
                
            infoOut = ""
            trainedOn = "0"
            if hasEmptyField == False:
                infoOut = infoOut+" good"
            else:
                 infoOut = infoOut+" BAD"
                
            if correctAnswer == False:
                infoOut = infoOut+" WRONG"
            else:
                 infoOut = infoOut+" correct"
                 
            print(i," ",expected_out," ",real_out,infoOut)
            
            if(i<len(predict)*partition):
                trainedOn = "1"
                            
            #if(i <len(predict) -1):
                #file.write(trainedOn+" "+str(all_input_data[i][0])+" "+ str(all_input_data[i][1])+" "+ str(all_input_data[i][2])+" "+ str(all_input_data[i][3])+" "+ str(all_input_data[i][4])+" "+ str(all_input_data[i][5])+" "+ str(all_input_data[i][6])+" "+ str(all_input_data[i][7])+" "+ str(all_input_data[i][8])+" "+ str(all_output_data[i][0])+" "+ str(all_output_data[i][1])+" "+ str(predict[i][0])+" "+ str(predict[i][1])+"\n");   
           # else:
                #file.write(trainedOn+" "+str(all_input_data[i][0])+" "+ str(all_input_data[i][1])+" "+ str(all_input_data[i][2])+" "+ str(all_input_data[i][3])+" "+ str(all_input_data[i][4])+" "+ str(all_input_data[i][5])+" "+ str(all_input_data[i][6])+" "+ str(all_input_data[i][7])+" "+ str(all_input_data[i][8])+" "+ str(all_output_data[i][0])+" "+ str(all_output_data[i][1])+" "+ str(predict[i][0])+" "+ str(predict[i][1]));   
        #file.close();        
        
        acc = (correct/float(len(all_input_data))) * 100
        error = error/float(len(all_input_data)) * 100
        print(acc," ",error)      
       
        
        
        '''
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
        '''
        
        '''
        def my_shuffle(array):
            random.shuffle(array)
            return array
        
        or
        
        random.shuffle(array)
        '''
        
        
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    