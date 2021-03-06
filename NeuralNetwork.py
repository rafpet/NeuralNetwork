class NeuralNetwork:
    
    def __init__(self, _num_inputs, _num_hidden, _num_outputs):
        
        self.input_nodes = _num_inputs
        self.hidden_nodes =_num_hidden
        self.output_nodes = _num_outputs
        
        self.weights_ih = Matrix(self.hidden_nodes,self.input_nodes)
        self.weights_ho = Matrix(self.output_nodes,self.hidden_nodes)
        
        self.weights_ih.randomise()
        self.weights_ho.randomise()
        
        self.bias_h = Matrix(self.hidden_nodes,1)
        self.bias_o = Matrix(self.output_nodes,1)
        
        self.bias_h.randomise()
        self.bias_o.randomise()
        
        self.learning_rate = .1
     
    def random(self):
    
        print "random function"
        
    def predict(self, _input_array):
        
        inputs = Matrix.from_array(_input_array)
        
        #layer 1
        hidden = Matrix.static_multiply(self.weights_ih,inputs)
        hidden.add(self.bias_h)
        
        hidden.map(sigmoid)
        
        #layer 2
        output = Matrix.static_multiply(self.weights_ho, hidden)
        output.add(self.bias_o)
        
        output.map(sigmoid)
        
        return output.to_array()
        
    def train(self, _input_array, _targets_array):
        
        #generating hidden outputs
        inputs = Matrix.from_array(_input_array)
        
        hidden = Matrix.static_multiply(self.weights_ih,inputs)
        hidden.add(self.bias_h)
        #activation function
        hidden.map(sigmoid)
        
        #generating output
        outputs = Matrix.static_multiply(self.weights_ho, hidden)
        outputs.add(self.bias_o)
        outputs.map(sigmoid)
        
        #Calculate errors
        #Error = Targets - Outputs
        targets = Matrix.from_array(_targets_array)
        output_errors = Matrix.subtract(targets, outputs)
        
        #outputs.show()
        #targets.show()
        #output_errors.show()
        
        gradients = Matrix.static_map(outputs,dsigmoid)
        gradients.scale(output_errors)
        gradients.scale(self.learning_rate)
        
        #calculate deltas
        hidden_t = Matrix.transpose(hidden)
        weights_ho_deltas = Matrix.static_multiply(gradients, hidden_t)
        #adjust the weights by deltas
        self.weights_ho.add(weights_ho_deltas)
        #adjust the bias by its deltas
        self.bias_o.add(gradients)
        
        #Calculate the hidden layer errors
        weights_ho_t = Matrix.transpose(self.weights_ho)
        hidden_errors = Matrix.static_multiply(weights_ho_t,output_errors)
        
        #calculate hidden gradient
        hidden_gradient = Matrix.static_map(hidden, dsigmoid)
        #hidden_gradient.show
        #hidden_errors.show()
        #print ""
        hidden_gradient.scale(hidden_errors)
        hidden_gradient.scale(self.learning_rate)
        
        #calculate input -> hidden deltas
        inputs_t = Matrix.transpose(inputs)
        #inputs_t.show()
        #hidden_gradient.show()
        #print ""
        weights_ih_deltas = Matrix.static_multiply(hidden_gradient, inputs_t)
        #adjust the bias by its deltas
        self.bias_h.add(hidden_gradient)
        
        self.weights_ih.add(weights_ih_deltas)
        
        
def sigmoid(x):
    return 1 / (1 + math.exp(-x))
    
def dsigmoid(y):
    #return sigmoid(x) * (1 - sigmoid(x))
    return y * (1 - y)
