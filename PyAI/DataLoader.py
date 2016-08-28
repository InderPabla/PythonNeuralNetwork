from PIL import Image
import numpy as np 
import os.path

class DataLoader:
    
    def __init__(self, data_paths = [], raw_data_filename = "raw_data.txt", 
                 size_x = 0, size_y = 0, num_inputs = 0, num_outputs = 0):
        self.data_paths = data_paths
        self.raw_data_filename = raw_data_filename
        self.size_x = size_x
        self.size_y = size_y
        self.num_inputs = num_inputs
        self.num_outputs = num_outputs
        
        self.input_images_set = []
        self.input_reals_set = []
        self.output_reals_set = []

        if(len(self.data_paths)>0):
            self.load_all_data()
            
    def load_all_data(self, data_paths=[]):
        paths = None
        
        if(len(data_paths)>0):
            paths = data_paths
        else:
            paths = self.data_paths
        
        for i in range(0, len(paths)):
            in_image,in_real,out_real = self.load_data(paths[i])
            self.input_images_set.append(in_image)
            self.input_reals_set.append(in_real)
            self.output_reals_set.append(out_real)
    
    def load_data(self,path):
        in_image = []
        in_real = []
        out_real = []
        images_count = 0
        
        if(os.path.exists(path+self.raw_data_filename)):
            images_count = len(os.listdir(path)) - 1
        else:
            images_count = len(os.listdir(path))
        # run through number of number of images to get
        for i in range(0,images_count):
            
            file_path = path+str(i)+'.png' #create file name of get
            raw_RGB = self.load_image(file_path)
              
            in_image.append(raw_RGB) # append broken down RGB array to images
            
        #convert images array to numpy type for theano compatibility   
        in_image = np.array(in_image,dtype = np.float32)    
        
        raw_count = 0
        
        if(os.path.exists(path+self.raw_data_filename)):
            with open(path+self.raw_data_filename) as file:
                for line in file: 
                    numbers_str = line.split()
                    numbers_float = [float(x) for x in numbers_str] 
        
                    X = []
                    Y = []
                    
                    for i in range(0, self.num_inputs):
                        X.append(numbers_float[i])
        
                    for i in range(self.num_inputs, len(numbers_float)):
                        Y.append(numbers_float[i])
                    
                    in_real.append(X)
                    out_real.append(Y)
                    
                    raw_count = raw_count + 1
                    
                    if raw_count == images_count:
                        break;
                        
        in_real = np.array(in_real, dtype = np.float32) 
        out_real = np.array(out_real, dtype = np.float32) 
        
        return in_image,in_real,out_real
    
    def load_image(self,image_path):
        stream = Image.open(image_path) #open file  in stream
            
        raw_image_data = list(stream.getdata()) #convert image file to a list
        
        raw_RGB = [[],[],[]] 
        raw_count = 0
        
        # nested for loop for visual appeal, running (rex_x * rex_y) number of 
        #times
        for y in range(0,self.size_x):
            
            # extracting RGB, one row at a tile
            red_row = []
            green_row = []
            blue_row = []
        
            #run through rows
            for x in range(0,self.size_y):
                
                # get RGB values and scale them between 0.0 to 1.0
                red = (raw_image_data[raw_count][0]/255.0)
                green = (raw_image_data[raw_count][1]/255.0)
                blue = (raw_image_data[raw_count][2]/255.0)
                          
                # append RGB to rows
                red_row.append(red)
                green_row.append(green)
                blue_row.append(blue)
                

                #increment counter to move to the next data set of tuples
                raw_count = raw_count + 1 
            
            #append RGB rows to their corresponding location in raw RGB array
            raw_RGB[0].append(red_row)
            raw_RGB[1].append(green_row)
            raw_RGB[2].append(blue_row)
         
        return raw_RGB
         
    def get_set_elements_to_train(self,index):
        return [np.array(self.input_images_set[index]), 
                np.array(self.input_reals_set[index])], np.array(self.output_reals_set[index])
    
    def get_only_image_elements_to_train(self,index):
        return [np.array(self.input_images_set[index])]
                
    def get_set_elements_to_predict(self,index):
        return [np.array(self.input_images_set[index]), 
                np.array(self.input_reals_set[index])]
    
    def get_set_size(self):
        return len(self.input_images_set)               
    
        