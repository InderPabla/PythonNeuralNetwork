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
    model_path = "hand_detection_model_2.json"
    weights_path = "hand_detection_weights_2.h5"
    res_x = 50
    res_y = 50

    raw_input_size = 0
    raw_output_size = 5

    image_val_data_location_1 = "HandGestureData/Ack/"
    image_val_data_location_2 = "HandGestureData/Fist/"
    image_val_data_location_3 = "HandGestureData/Hand/"
    image_val_data_location_4 = "HandGestureData/One/"
    image_val_data_location_5 = "HandGestureData/Straight/"
    
    image_pre_data_location_1_1 = "HandGestureData/AckPre/"
    image_pre_data_location_2_1 = "HandGestureData/FistPre/"
    image_pre_data_location_3_1 = "HandGestureData/HandPre/"
    image_pre_data_location_4_1 = "HandGestureData/OnePre/"
    image_pre_data_location_5_1 = "HandGestureData/StraightPre/"
    
    image_pre_data_location_1_2 = "HandGestureData/AckPre2/"
    image_pre_data_location_2_2 = "HandGestureData/FistPre2/"
    image_pre_data_location_3_2 = "HandGestureData/HandPre2/"
    image_pre_data_location_4_2 = "HandGestureData/OnePre2/"
    image_pre_data_location_5_2 = "HandGestureData/StraightPre2/"
    
    net = NetLoader.NetLoader(model_file=model_path,weights_file=weights_path,learning_rate = 0.0006,decay_rate=0.00000001,create_file=True,epoch_save = 1)
   

    data_list_1 = [image_val_data_location_1,image_val_data_location_2,image_val_data_location_3,image_val_data_location_4,image_val_data_location_5,
                 image_pre_data_location_1_1,image_pre_data_location_2_1,image_pre_data_location_3_1,image_pre_data_location_4_1,image_pre_data_location_5_1]
        
    data_list_2 = [image_pre_data_location_1_2]
                 
    data = DataLoader.DataLoader(data_list_2, size_x = res_x,
                                 size_y=res_y, num_inputs=raw_input_size, 
                                 num_outputs=raw_output_size,black_white=True)
    
    

    #data.combine_data(random_sort= True)
    input_element_1, output_element_1 = data.get_set_elements_to_train(0)

    pre = net.predict(input_element_1[0])
    for i in range(0,len(pre)):
        pred = pre[i]*100
        
        print("Max Index: "+str(np.argmax(pred))+"  Output: "+str(int(pred[0]))+" "+str(int(pred[1]))+" "+str(int(pred[2]))+" "+str(int(pred[3]))+" "+str(int(pred[4])))
        
    #for i in range(0,15):
        #net.fit(input_element_1[0],output_element_1,verbose = 2)

    
