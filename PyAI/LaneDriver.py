import NetLoader as NetLoader
import DataLoader as DataLoader
import EasySocket as EasySocket
import numpy as np


if __name__ == "__main__":
    model_path = "lane_driving_car_model.json"
    weights_path = "lane_driving_car_weights.h5"
    res_x = 50
    res_y = 50
    raw_input_size = 1
    raw_output_size = 3
    image_file = "../Tests/AdvancedCarModel/real_time.png"
    image_val_data_location_1 = "../Tests/AdvancedCarModel/Data18/"
    
    '''
    socket = EasySocket.EasySocket(preset_unpack_types = ['fff'])
    b = socket.get_array_data(1,0)
    print(np.array(b))
    '''
    
    net = NetLoader.NetLoader(model_file=model_path,weights_file=weights_path)

    data = DataLoader.DataLoader([image_val_data_location_1], size_x = res_x,
                                 size_y=res_y, num_inputs=raw_input_size, 
                                 num_outputs=raw_output_size)
    '''
    input_element,output_element = data.get_set_elements_to_train(0)
    net.fit(input_element,output_element,verbose = 2)
    '''
    
    socket = EasySocket.EasySocket(preset_unpack_types = ['ff'])
    socket.connect()
    while True:
        get_data = np.array(socket.get_array_data(8,0))
        real_data = np.array([get_data[1]],dtype=np.float32)
        raw_RGB = data.load_image(image_file)
        raw_RGB = np.array(raw_RGB,dtype = np.float32)
        pre = net.predict([np.array([raw_RGB]),np.array([real_data])])
        
        pre = pre[0]

         
        max_num = 0
        prediction_answer = 0
        for m in range(len(pre)):
            if pre[m] > max_num:
                max_num = pre[m]
                prediction_answer = m
        
        if(prediction_answer == 0): 
            prediction_answer = -1
        elif(prediction_answer == 1): 
            prediction_answer = 0
        else:
            prediction_answer = 1
           
        message = str(prediction_answer)
        
        socket.send_string_data(message)
    socket.close()
