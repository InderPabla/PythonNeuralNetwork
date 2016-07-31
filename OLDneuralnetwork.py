import numpy as np
from PIL import Image
import neuralnetwork as nnet

           
##### Main Method #####

if __name__ == '__main__':
    layer = [225,225,225,225,112,112,112,50,50,50,10,10,10]
    nn = nnet.NeuralNetwork(layer,0.1,'sigm')

    dataCollective = []
    for i in range(0,75):
       
       for j in range(0,10):
           random_file = 'TestData/'+str(i)+'_'+str(j)+'.png'
           im = Image.open(random_file)
           data = list(im.getdata())

           question = []
            
           answer = [0,0,0,0,0,0,0,0,0,0]
           answer[j] = 1
            
           for j in range(0,225):
               if(data[j][0] == 0):
                   question.append(1)
               else:
                   question.append(0)
           
           data = []        
           data.append(question)
           data.append(answer)
           dataCollective.append(data)

    setNumber = 0
    totalDataCount = len(dataCollective)
    for i in range(0,150000):
        if(i%100 == 0):
            print(i)
        
        #randSet = np.random.randint(len(dataCollective))
        
        question = dataCollective[setNumber][0]
        answer  = dataCollective[setNumber][1]
        nn.feedtrain(question,answer)
        setNumber = setNumber +1
        
        if(setNumber == totalDataCount):
            setNumber = 0
        
    '''          
    for i in range(0,100000):
        if(i%100 == 0):
            print(i)
            question = []
            
            answer = [0,0,0,0,0,0,0,0,0,0]
            answer[filenumber] = 1
            
            for j in range(0,225):
                if(data[j][0] == 0):
                    question.append(1)
                else:
                    question.append(0)
                    
        for x in range(0,1):
            randSet = np.random.randint(51)
            filenumber = np.random.randint(10)

            random_file = 'TestData/'+str(randSet)+'_'+str(filenumber)+'.png'
            im = Image.open(random_file)
            data = list(im.getdata())
            
            question = []
            
            answer = [0,0,0,0,0,0,0,0,0,0]
            answer[filenumber] = 1
            
            for j in range(0,225):
                if(data[j][0] == 0):
                    question.append(1)
                else:
                    question.append(0)
            
            nn.feedtrain(question,answer)

            
        
        filenumber = filenumber+1
        if filenumber == 10:
            filenumber = 0
    '''

    for i in range(0,10):
        for sets in range(0,75):
            file = 'TestData/'+str(sets)+'_'+str(i)+'.png'
            im = Image.open(file)
            data = list(im.getdata())
            question = []
            for j in range(0,225):
                if(data[j][0] == 0):
                    question.append(1)
                else:
                    question.append(0)

            ret = list(map(int,100*nn.feedforward(question)))
                
            whatItThought = 0
            whatItThoughtIndex = 0
                
            for k in range(0,10):
                if(ret[k]>whatItThought):
                    whatItThought = ret[k]
                    whatItThoughtIndex = k
                  
            print(i,": ",whatItThoughtIndex)
        print("=====================")
       
    weights = nn.getweights()
    text_file = open("neuralnetwork_number_recognition_5.txt", "w")
    text_file.write(str(len(layer))+'\n')
    
    for i in range(0,len(layer)):
        text_file.write(str(layer[i])+'\n')
        
    for i in range(0,len(weights)):
        w1 = weights[i]
        #print('--------------')
        for j in range(0,len(w1)):
            w2 = w1[j]
            #print('==============')
            for k in range(0,len(w2)):
                w3 = w2[k]
                text_file.write(str(w3)+'\n')

    text_file.close()
    
    
    '''
    details = []
    weights = []
    with open("neuralnetwork_number_recognition.txt") as f:
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
    
       
    print(layer)
    
    for i in range(0,len(layer)-1):
        firstlayer = layer[i]
        secondlayer = layer[i+1]
        arrayOutter = []
        #print("====================")
        for j in range(0,firstlayer):
            #print("@@@@@@@@@@@@@@@@@")
            arrayInner = []
            for k in range(0,secondlayer):    
                #print(details[nextIndex])
                arrayInner.append(details[nextIndex])
                nextIndex = nextIndex + 1
            arrayOutter.append(arrayInner)
        weights.append(arrayOutter)

    
    #print(weights)
    nn = NeuralNetwork(weights,0.2,'sigm',1)
    #print(nn.feedforward([5,2,-3]))
    

    file = 'TestData/'+str(25)+'_'+str(5)+'.png'
    im = Image.open(file)
    data = list(im.getdata())
    question = []
    for j in range(0,225):
        if(data[j][0] == 0):
            question.append(1)
        else:
            question.append(0)

    ret = list(map(int,100*nn.feedforward(question)))
    print(ret)
    '''
    
    #print(details)
    #XOR_TEST()
    #MAJORITY_TEST()
    
    
    


    
   
            

