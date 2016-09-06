import NetLoader as NetLoader
import DataLoader as DataLoader

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
    raw_output_size = 8
    predict_mode = True
    
    image_val_data_location_1 = "LaneDetectionData/ImagesDataSet6/"
    image_val_data_location_2 = "LaneDetectionData/ImagesDataSet7/"
    image_val_data_location_3 = "LaneDetectionData/ImagesDataSet8/"
    image_val_data_location_4 = "LaneDetectionData/ImagesDataSet9/"
    image_val_data_location_5 = "LaneDetectionData/ImagesDataSet10/"
    image_val_data_location_6 = "LaneDetectionData/ImagesDataSet11/"
    image_val_data_location_7 = "LaneDetectionData/ImagesDataSet12/"
    image_val_data_location_8 = "LaneDetectionData/ImagesDataSet13/"
    image_val_data_location_9 = "LaneDetectionData/ImagesDataSet14/"
    output_file_1 = "output_6.txt"
    output_file_2 = "output_7.txt"
    output_file_3 = "output_8.txt"
    output_file_4 = "output_9.txt"
    output_file_5 = "output_10.txt"
    output_file_6 = "output_11.txt"
    output_file_7 = "output_12.txt"
    output_file_8 = "output_13.txt"
    output_file_9 = "output_14.txt"
    
    net = NetLoader.NetLoader(model_file=model_path,weights_file=weights_path,
                              learning_rate = 0.055,decay_rate=0.000001,
                              train_mode = True,epoch_save = 2,
                              optimizer = "SGD")
                              
    '''
    data = DataLoader.DataLoader([image_val_data_location_9], size_x = res_x,
                                 size_y=res_y, num_inputs=raw_input_size, 
                                  num_outputs=raw_output_size)
    
                                  
    input_element_1 = data.get_only_image_elements_to_train(0)
    input_element_1 = input_element_1[0]
    pre = net.predict(input_element_1)
    text_file = open(output_file_9, "w")
    
    for i in range(0,len(input_element_1)):
        out = pre[i]
        text_file.write(str(out[0])+" "+str(out[1])+" "+str(out[2])+" "+str(out[3])+" "+str(out[4])+" "+str(out[5])+" "+str(out[6])+" "+str(out[7])+"\n")
    text_file.close() 
    '''
    
                              
    data = DataLoader.DataLoader([image_val_data_location_1,image_val_data_location_2,
                                  image_val_data_location_3,image_val_data_location_4,
                                  image_val_data_location_5,image_val_data_location_6,
                                  image_val_data_location_7,image_val_data_location_8], 
                                  size_x = res_x, size_y=res_y, num_inputs=raw_input_size, 
                                  num_outputs=raw_output_size)
    
    if(predict_mode == False):
        data.combine_data(True)
        input_element_1,output_element_1 = data.get_set_elements_to_train(0)
        input_element_1 = input_element_1[0]
        
        for i in range(0,100):
            net.fit(input_element_1,output_element_1,verbose = 2)   
    else:
        input_element_1,output_element_1 = data.get_set_elements_to_train(0)
        input_element_1 = input_element_1[0]
        input_element_2,output_element_2 = data.get_set_elements_to_train(1)
        input_element_2 = input_element_2[0]
        input_element_3,output_element_3 = data.get_set_elements_to_train(2)
        input_element_3 = input_element_3[0]
        input_element_4,output_element_4 = data.get_set_elements_to_train(3)
        input_element_4 = input_element_4[0]
        input_element_5,output_element_5 = data.get_set_elements_to_train(4)
        input_element_5 = input_element_5[0]
        input_element_6,output_element_6 = data.get_set_elements_to_train(5)
        input_element_6 = input_element_6[0]
        input_element_7,output_element_7 = data.get_set_elements_to_train(6)
        input_element_7 = input_element_7[0]
        input_element_8,output_element_8 = data.get_set_elements_to_train(7)
        input_element_8 = input_element_8[0]
        
        pre = net.predict(input_element_1)
        text_file = open(output_file_1, "w")
        for i in range(0,len(input_element_1)):
            out = pre[i]
            text_file.write(str(out[0])+" "+str(out[1])+" "+str(out[2])+" "+str(out[3])+" "+str(out[4])+" "+str(out[5])+" "+str(out[6])+" "+str(out[7])+"\n")
        text_file.close() 
        
        pre = net.predict(input_element_2)
        text_file = open(output_file_2, "w")
        for i in range(0,len(input_element_2)):
            out = pre[i]
            text_file.write(str(out[0])+" "+str(out[1])+" "+str(out[2])+" "+str(out[3])+" "+str(out[4])+" "+str(out[5])+" "+str(out[6])+" "+str(out[7])+"\n")
        text_file.close() 
        
        pre = net.predict(input_element_3)
        text_file = open(output_file_3, "w")
        for i in range(0,len(input_element_3)):
            out = pre[i]
            text_file.write(str(out[0])+" "+str(out[1])+" "+str(out[2])+" "+str(out[3])+" "+str(out[4])+" "+str(out[5])+" "+str(out[6])+" "+str(out[7])+"\n")
        text_file.close() 
        
        pre = net.predict(input_element_4)
        text_file = open(output_file_4, "w")
        for i in range(0,len(input_element_4)):
            out = pre[i]
            text_file.write(str(out[0])+" "+str(out[1])+" "+str(out[2])+" "+str(out[3])+" "+str(out[4])+" "+str(out[5])+" "+str(out[6])+" "+str(out[7])+"\n")
        text_file.close() 
        
        pre = net.predict(input_element_5)
        text_file = open(output_file_5, "w")
        for i in range(0,len(input_element_5)):
            out = pre[i]
            text_file.write(str(out[0])+" "+str(out[1])+" "+str(out[2])+" "+str(out[3])+" "+str(out[4])+" "+str(out[5])+" "+str(out[6])+" "+str(out[7])+"\n")
        text_file.close() 
        
        pre = net.predict(input_element_6)
        text_file = open(output_file_6, "w")
        for i in range(0,len(input_element_6)):
            out = pre[i]
            text_file.write(str(out[0])+" "+str(out[1])+" "+str(out[2])+" "+str(out[3])+" "+str(out[4])+" "+str(out[5])+" "+str(out[6])+" "+str(out[7])+"\n")
        text_file.close() 
        
        pre = net.predict(input_element_7)
        text_file = open(output_file_7, "w")
        for i in range(0,len(input_element_7)):
            out = pre[i]
            text_file.write(str(out[0])+" "+str(out[1])+" "+str(out[2])+" "+str(out[3])+" "+str(out[4])+" "+str(out[5])+" "+str(out[6])+" "+str(out[7])+"\n")
        text_file.close() 
        
        pre = net.predict(input_element_8)
        text_file = open(output_file_8, "w")
        for i in range(0,len(input_element_8)):
            out = pre[i]
            text_file.write(str(out[0])+" "+str(out[1])+" "+str(out[2])+" "+str(out[3])+" "+str(out[4])+" "+str(out[5])+" "+str(out[6])+" "+str(out[7])+"\n")
        text_file.close() 
     
    
    
   