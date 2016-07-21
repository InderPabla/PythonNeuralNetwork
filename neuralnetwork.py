import numpy as np

def sigmoid(x):
    return 1.0/(1.0 + np.exp(-x))

def sigmoid_delta(x):
    return sigmoid(x)*(1.0-sigmoid(x))

def tanh(x):
    return np.tanh(x)

def tanh_delta(x):
    return 1.0 - x**2


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

        a = [inputs]
        
        for l in range(len(self.weights)):
            dot_value = np.dot(a[l], self.weights[l])
            activation = self.activation(dot_value)
            a.append(activation)
    
        return a

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
        
##### Main Method #####

if __name__ == '__main__':

    nn = NeuralNetwork([2,2,1],0.2,'tanh')
    question = [[0,0],[0,1],[1,0],[1,1]]
    answer = [[1],[0],[0],[1]]

    for i in range(0,100):
        random = np.random.randint(4)
        nn.feedtrain(question[random],answer[random])
        
    for i in range(0,4):
        print(nn.feedforward(question[i]))
        
            

