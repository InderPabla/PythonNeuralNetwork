import NetLoader as NetLoader
import DataLoader as DataLoader
import numpy as np

def index_of_largest_element(array):
    large_index = 0
    large_element = array[0]
    for i in range(1,len(array)):
        if array[i]>large_element:
            large_element = array[i]
            large_index = i
    return large_index
        
if __name__ == "__main__":
    model_path = "lane_detection_model.json"
    weights_path = "lane_detection_weights.h5"
    res_x = 100
    res_y = 56
    raw_input_size = 0
    raw_output_size = 4

    image_val_data_location_1 = "LaneDetectionData/ImagesDataSet1/"
    image_val_data_location_2 = "LaneDetectionData/ImagesDataSet2/"
    image_val_data_location_3 = "LaneDetectionData/ImagesDataSet3/"
    output_file_1 = "output_1.txt"
    output_file_2 = "output_2.txt"
    output_file_3 = "output_3.txt"
    output_file_4 = "output_5.txt"
      
    net = NetLoader.NetLoader(model_file=model_path,weights_file=weights_path,
                              learning_rate = 0.0001,decay_rate=0.000001,
                              train_mode = True,epoch_save = 6,
                              optimizer = "SGD")

    data = DataLoader.DataLoader([image_val_data_location_3], size_x = res_x,
                                 size_y=res_y, num_inputs=raw_input_size, 
                                 num_outputs=raw_output_size)
                            
    input_element_3,output_element_3 = data.get_set_elements_to_train(0)
    input_element_3 = input_element_3[0]

    
    '''
    for i in range(0,25):
        #net.fit(input_element_1,output_element_1,verbose = 2)
        net.fit(input_element_3,output_element_3,verbose = 2)
    '''
    
    pre = net.predict(input_element_3)
    text_file = open(output_file_3, "w")
    
    for i in range(0,len(input_element_3)):
        out = pre[i]
        text_file.write(str(out[0])+" "+str(out[1])+" "+str(out[2])+" "+str(out[3])+"\n")
    text_file.close() 
    
    '''
    pre = net.predict(input_element_1)
    text_file = open(output_file_1, "w")
    
    for i in range(0,len(input_element_1)):
        out = pre[i]
        text_file.write(str(out[0])+" "+str(out[1])+" "+str(out[2])+" "+str(out[3])+"\n")
    text_file.close() 
    
    pre = net.predict(input_element_2)
    text_file = open(output_file_2, "w")
    
    for i in range(0,len(input_element_2)):
        out = pre[i]
        text_file.write(str(out[0])+" "+str(out[1])+" "+str(out[2])+" "+str(out[3])+"\n")
    text_file.close() 
    '''
    
    '''
    pre = net.predict(input_element_3)
    text_file = open(output_file_3, "w")
    
    for i in range(0,len(input_element_3)):
        out = pre[i]
        text_file.write(str(out[0])+" "+str(out[1])+" "+str(out[2])+" "+str(out[3])+" "+str(out[4])+" "+str(out[5])+" "+str(out[6])+" "+str(out[7])+"\n")
    text_file.close() 
    '''
    
    '''
    pre = net.predict(input_element_4)
    text_file = open(output_file_4, "w")
    
    for i in range(0,len(input_element_4)):
        out = pre[i]
        text_file.write(str(out[0])+" "+str(out[1])+" "+str(out[2])+" "+str(out[3])+" "+str(out[4])+" "+str(out[5])+" "+str(out[6])+" "+str(out[7])+"\n")
    text_file.close() 
    '''
    
    '''
    for i in range(0,len(input_element_1)):
        error = output_element_1[i]-pre[i]
        error = error*100
        print(np.array(error,dtype=np.int))
   ''' 
    
    
   