import numpy as np
from PIL import Image

#Neural network learns XOR
def XOR_TEST(): 
    nn = NeuralNetwork([3,3,3,1],0.2,'tanh')
    
    question = [[0,0,0],[0,0,1],[0,1,0],[0,1,1],[1,0,0],[1,0,1],[1,1,0],[1,1,1]]
    answer = [[0],[1],[1],[0],[1],[0],[0],[1]]

    for i in range(0,5000):
        random = np.random.randint(len(answer))
        
        questionToCopy = question[random]
        questionCopied = []
        
        for x in range(0,len(questionToCopy)):
            questionCopied.append(questionToCopy[x])

        nn.feedtrain(questionCopied,answer[random])
        
    for i in range(0,len(answer)):
        print(nn.feedforward(question[i]))

#Neural network learns majority function.
#If there are more 1's output 1 else output 0
def MAJORITY_TEST():
    nn = NeuralNetwork([9,5,5,1],0.2,'tanh')
    
    for i in range(0,5000):
        newQuestion = []
        nums1 = 0
        nums0 = 0
        ans = []
        for y in range (0,9):
            z = np.random.randint(2)
            newQuestion.append(z)
            if z == 0:
                nums0 = nums0+1
            else:
                nums1 = nums1+1
        if(nums1>nums0):
            ans.append(1)
        else:
            ans.append(0)

        nn.feedtrain(newQuestion,ans)

    for i in range(0,10):
        newQuestion = []
        nums1 = 0
        nums0 = 0
        ans = []
        for y in range (0,9):
            z = np.random.randint(2)
            newQuestion.append(z)
            if z == 0:
                nums0 = nums0+1
            else:
                nums1 = nums1+1
        if(nums1>nums0):
            ans.append(1)
        else:
            ans.append(0)
        
        print("Question: ",newQuestion)
        print("Expected: ",ans)
        print("Real: ",nn.feedforward(newQuestion))

#Sigmoid activation of a given value
def sigmoid(x):
    return 1.0/(1.0 + np.exp(-x))

#Change is the sigmoid activation given a activated value
def sigmoid_delta(x):
    return x*(1.0-x)

#Hyperbolic tangent activation of a given value
def tanh(x):
    return np.tanh(x)

#Change is the hyperbolic tangent activation given a activated value
def tanh_delta(x):
    return 1.0 - x**2

#Neural network class which provides feed forward and back propagation traning of network
class NeuralNetwork:

    #constructor
    def __init__ (self, layers, learn_rate, act):
        self.layers = layers
        self.learn_rate = learn_rate
        
        if act == 'tanh':
            self.activation = tanh
            self.activation_delta = tanh_delta
        elif act == 'sigm':
            self.activation = sigmoid
            self.activation_delta = sigmoid_delta

        self.weights = []
        
        for i in range(1, len(layers) - 1):
            r = 2*np.random.random((layers[i-1] + 1, layers[i] + 1)) -1
            self.weights.append(r)
            
        r = 2*np.random.random( (layers[i] + 1, layers[i+1])) -1

        self.weights.append(r)

    
    #feed forward
    def feedforward(self, inputs):
        inputs.append(1)
        result = []
        a = [inputs]
        
        for l in range(len(self.weights)):
            dot_value = np.dot(a[l], self.weights[l])
            activation = self.activation(dot_value)
            a.append(activation)
            result.append(activation)
            
        return result[len(result)-1]

    #back propagation traning 
    def feedtrain(self, inputs, expected):
        inputs.append(1)
        a = [inputs]
        
        for l in range(len(self.weights)):
            dot_value = np.dot(a[l], self.weights[l])
            activation = self.activation(dot_value)
            a.append(activation)
            
        error = expected - a[-1]
        
        deltas = [error * self.activation_delta(a[-1])]

        for l in range(len(a) - 2, 0, -1): 
                deltas.append(deltas[-1].dot(self.weights[l].T)*self.activation_delta(a[l]))

        deltas.reverse()

        for i in range(len(self.weights)):
                layer = np.atleast_2d(a[i])
                delta = np.atleast_2d(deltas[i])
                self.weights[i] += self.learn_rate * layer.T.dot(delta)
    
    #return weights        
    def getweights(self):
        return self.weights
            
           
##### Main Method #####

if __name__ == '__main__':
    
    #nn = NeuralNetwork([225,225,112,56,25,10,10],0.2,'sigm')
    nn = NeuralNetwork([225,112,56,25,10],0.2,'sigm')
    filenumber = 0
    
    for i in range(0,50):
        
        if(i%100 == 0):
            print(i)

        for x in range(0,10):
            randSet = np.random.randint(30)
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
        
    for i in range(0,10):
        for sets in range(0,31):
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
        
    weights = nn.getweights
    #print(weights)
    #print(len(weights))
    #print(len(weights[0]))
    print(str(len(weights[0][0])))
    #XOR_TEST()
    #MAJORITY_TEST()
    
    
    


    
   
            

