import numpy as np
import neuralnetwork as nnet
from PIL import ImageGrab
from PIL import Image
import socket
import struct, pickle

##### Main Method #####
if __name__ == '__main__':
    
    details = []
    weights = []

    #get neural network details from net file
    with open("neuralnetwork_number_recognition_5.txt") as f:
        for line in f:  
            numbers_str = line.split()
            numbers_float = [float(x) for x in numbers_str] 
            details.append(numbers_float[0])
        
    numberOfLayers = int(details[0])
    layer = []
    nextIndex = 1
    for i in range(1,numberOfLayers+1):
        layer.append(int(details[i]))
        nextIndex = nextIndex +1
    
       
    print('Layer Structure: ',layer)
    
    for i in range(0,len(layer)-1):
        firstlayer = layer[i]
        secondlayer = layer[i+1]
        arrayOutter = []
        for j in range(0,firstlayer):
            arrayInner = []
            for k in range(0,secondlayer):    
                arrayInner.append(details[nextIndex])
                nextIndex = nextIndex + 1
            arrayOutter.append(arrayInner)
        weights.append(arrayOutter)

    nn = nnet.NeuralNetwork(weights,0.2,'sigm',1)

    s = socket.socket()         # Create a socket object
    host = socket.gethostname() # Get local machine name
    port = 12345                # Reserve a port for your service.
    s.bind((host, port))        # Bind to the port

    s.listen(5)
    
    c, addr = s.accept()     # Establish connection with client.
    
    while (True):
       

        data = c.recv(225) 

        inputs = []
        for ch in data:
            inputs.append(ch)

        ret = list(map(int,100*nn.feedforward(inputs)))
 
        whatItThought = 0
        whatItThoughtIndex = 0
            
        for k in range(0,10):
            if(ret[k]>whatItThought):
                whatItThought = ret[k]
                whatItThoughtIndex = k
              
        print('Packet Sent: ',ret)

        p = struct.pack('i'* len(ret), *ret)
        c.send(p)
        #print (p)
        #data_string = pickle.dumps(ret)
        #c.send(data_string)
        
    c.close()       

    #print(details)
    #XOR_TEST()
    #MAJORITY_TEST()

    
   
            

