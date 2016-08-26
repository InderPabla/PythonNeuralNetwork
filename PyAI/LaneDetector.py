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

    image_val_data_location_1 = "LaneDetectionData/ImagesDataSet5/"
    

    net = NetLoader.NetLoader(model_file=model_path,weights_file=weights_path,learning_rate = 0.01,train_mode = True,epoch_save = 2)

    data = DataLoader.DataLoader([image_val_data_location_1], size_x = res_x,size_y=res_y, num_inputs=raw_input_size, num_outputs=raw_output_size)
                                 
    input_element,output_element = data.get_set_elements_to_train(0)
    input_element = input_element[0]
    
    for i in range(0,25):
        net.fit(input_element,output_element,verbose = 2)
    
    '''
    input_element,output_element = data.get_set_elements_to_train(0)
    net.fit(input_element,output_element,verbose = 2)
    pre = net.predict([np.array([raw_RGB]),np.array([real_data])])
    '''
    
   