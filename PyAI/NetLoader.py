from keras.models import model_from_json
from keras.optimizers import SGD

class NetLoader:
    
    def __init__(self, model_file = "", weights_file = "", learning_rate = 0.01, 
                 decay_rate = 0.000001, loss_function = "mean_squared_error", 
                 momentum= 0.9, nesterov=True, train_mode = True):
                     
        self.model_file = model_file
        self.weights_file = weights_file
        self.learning_rate= learning_rate
        self.decay_rate = decay_rate
        self.loss_function = loss_function
        self.momentum = momentum
        self.nesterov = nesterov
        self.train_mode = train_mode
        
        self.model = None
        self.optimizer = None
        
        if not model_file == "":
            self.load_model()
            
            if not weights_file  == "":
                self.load_weights()
        
        if self.train_mode == True:
            self.compile_model()
    
    def load_model(self):
        json_file = open(self.model_file, 'r')
        loaded_model_json = json_file.read()
        json_file.close()
        
        self.model = model_from_json(loaded_model_json)
        
    def load_weights(self):
        self.model.load_weights(self.weights_file)
    
    def compile_model(self):
        self.optimizer = SGD(lr=self.learning_rate, decay=self.decay_rate, 
                             momentum=self.momentum, nesterov=self.nesterov)
                             
        self.model.compile(loss = self.loss_function, 
                           optimizer = self.optimizer)
    
    def predict(self,inputs):
        prediction = self.model.predict(inputs)
        return prediction
    
    def fit(self,inputs,outputs,epochs = 1,verbose = 0):
        self.model.fit(inputs, outputs, nb_epoch=epochs,verbose = verbose)
    