import NetLoader as NetLoader
import DataLoader as DataLoader




if __name__ == "__main__":
    model_path = "lane_driving_car_model.json"
    weights_path = "lane_driving_car_weights.h5"
    res_x = 50
    res_y = 50
    raw_input_size = 1
    raw_output_size = 3
    
    image_val_data_location_1 = "../Tests/AdvancedCarModel/Data18/"

    
    net = NetLoader.NetLoader(model_file=model_path,weights_file=weights_path)

    data = DataLoader.DataLoader([image_val_data_location_1], size_x = res_x,
                                 size_y=res_y, num_inputs=raw_input_size, 
                                 num_outputs=raw_output_size)
    
    input_element,output_element = data.get_set_elements_to_train(0)
    net.fit(input_element,output_element,verbose = 2)
    