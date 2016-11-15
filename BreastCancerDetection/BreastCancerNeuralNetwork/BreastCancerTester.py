from keras.models import model_from_json
import numpy as np
import os.path
import sys 

if __name__ == "__main__":
    file_name = "C:/Users/Pabla/Desktop/ImageAnalysis/PyAI/BCdata.asc"
    
    model_path = "C:/Users/Pabla/Desktop/ImageAnalysis/PyAI/cancer_model.json"
    weights_path = "C:/Users/Pabla/Desktop/ImageAnalysis/PyAI/cancer_model_weights.h5"
    
    #test_input_data = [[10,10,10,10,5,10,10,10,7]]
    
    test_input_data = [[int(sys.argv[1]),int(sys.argv[2]),int(sys.argv[3]),int(sys.argv[4]),int(sys.argv[5]),int(sys.argv[6]),int(sys.argv[7]),int(sys.argv[8]),int(sys.argv[9])]]
    
    test_input_data = np.array(test_input_data)
    
    json_file = open(model_path, 'r')
    loaded_model_json = json_file.read()
    json_file.close()  
    cancer_model = model_from_json(loaded_model_json)
    
    if (os.path.exists(weights_path)):
            cancer_model.load_weights(weights_path)
            predict = cancer_model.predict(test_input_data)
            if(predict[0][0]>predict[0][1]):
                print("0")
            else:
                print("1")
            
        
        
        
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    