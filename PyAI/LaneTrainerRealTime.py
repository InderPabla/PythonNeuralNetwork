import NetLoader as NetLoader
import DataLoader as DataLoader
import EasySocket as EasySocket
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
    model_path = "lane_driving_car_model.json"
    weights_path = "lane_driving_car_weights_2.h5"
    res_x = 50
    res_y = 50
    raw_input_size = 1
    raw_output_size = 3
    image_file = "../Tests/AdvancedCarModel/real_time.png"
    

    net = NetLoader.NetLoader(model_file=model_path,weights_file=weights_path,epoch_save = 100,learning_rate = 0.0001)

    data = DataLoader.DataLoader([], size_x = res_x,
                                 size_y=res_y, num_inputs=raw_input_size, 
                                 num_outputs=raw_output_size)

    
    socket = EasySocket.EasySocket(preset_unpack_types = ['fffff'])
    socket.connect()
    counter = 0
    
    print("STARTED")
    while True:

        get_data = np.array(socket.get_array_data(20,0))
        real_data = np.array([get_data[1]],dtype=np.float32)
        expected_output = np.array([get_data[2],get_data[3],get_data[4]],dtype=np.float32)
        
        raw_RGB = data.load_image(image_file)
        raw_RGB = np.array(raw_RGB,dtype = np.float32)
        
        
        train_images_X = []
        train_images_X.append(raw_RGB)
        train_images_X = np.array(train_images_X,dtype = np.float32)  
        
        train_raw_X = []
        train_raw_Y = []
        train_raw_X.append(real_data)
        train_raw_Y.append(expected_output)
        train_raw_X = np.array(train_raw_X, dtype = np.float32) 
        train_raw_Y = np.array(train_raw_Y, dtype = np.float32) 

        net.fit([np.array(train_images_X), np.array(train_raw_X)], np.array(train_raw_Y), epochs = 1, verbose = 0)
        message = str(0)

        socket.send_string_data(message)
    socket.close()
