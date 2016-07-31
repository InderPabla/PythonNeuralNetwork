import numpy as np
from PIL import Image
import neuralnetwork as nnet

           
##### Main Method #####

if __name__ == '__main__':
    layer = [100,100,100,50,50,50,10,10,2]
    nn = nnet.NeuralNetwork(layer,0.1,'sigm')
 
train_answer = []
with open("DrivingData\\car_traning_data_1.txt") as f:
    for line in f: 
        answer = []
        numbers_str = line.split()
        numbers_float = [float(x) for x in numbers_str] 
        train_answer.append(numbers_float)


   
qus = []
for m in range(0,300):
     
    file = 'DrivingData/'+str(m)+'.png'
    im = Image.open(file)
    data = list(im.getdata())
    k = 0
    #re_data = [[],[],[]] 
    re_data = []  
    for i in range(0,1):
        red_row = []
        green_row = []
        blue_row = []
    
        for j in range(0,100):
            red = (data[k][0])
            green = (data[k][1])
            blue = (data[k][2])
    
            red_row.append(red)
            green_row.append(((green+red+blue)/3.0)/255.0)
            blue_row.append(blue)
    
            k = k + 1
        #re_data[0].append(red_row)
        #re_data[1].append(green_row)
        #re_data[2].append(blue_row)
        re_data.append(green_row)
    
    qus.append(re_data)


for i in range(0,1000):
    print(i)
    for m in range(0,300):
        nn.feedtrain(qus[m],train_answer[m])



for m in range(0,300):
    pre = nn.feedforward(qus[m])

    err = [pre[0][0] - train_answer[m][0], pre[0][1] - train_answer[m][1]]
    if(err[0]<0):
        err[0] = err[0]*-1.0
    if(err[1]<0):
        err[1] = err[1]*-1.0
    
    print(pre[0]," ",train_answer[m]," ",err)

  


       

    
    


    
   
            


