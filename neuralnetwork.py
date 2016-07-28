import numpy as np

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
    def __init__ (self, layers, learn_rate, act, tip = 0):
        self.layers = layers
        self.learn_rate = learn_rate
        
        if act == 'tanh':
            self.activation = tanh
            self.activation_delta = tanh_delta
        elif act == 'sigm':
            self.activation = sigmoid
            self.activation_delta = sigmoid_delta

        self.weights = []
        
        if (tip == 0):
            for i in range(1, len(layers) - 1):
                r = 2*np.random.random((layers[i-1], layers[i] )) -1
                self.weights.append(r)
                
            r = 2*np.random.random( (layers[i], layers[i+1] )) -1
            
            
            self.weights.append(r)
        else:
            self.weights = layers
            
    #feed forward
    def feedforward(self, inputs):
       #inputs.append(1)
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
        #inputs.append(1)
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
    
    
    


    
   
            

