import numpy as np
import math

"""
 ==================================
 Problem 3: Neural Network Basics
 ==================================
    Generates a neural network with the following architecture:
        Fully connected neural network.
        Input vector takes in two features.
        One hidden layer with three neurons whose activation function is ReLU.
        One output neuron whose activation function is the identity function.
"""


def rectified_linear_unit(x):
    """ Returns the ReLU of x, or the maximum between 0 and x."""
    # TODO
    return max(x,0)
def rectified_linear_unit_derivative(x):
    """ Returns the derivative of ReLU."""
    # TODO
    if x <= 0:
        return 0
    else:
        return 1
def output_layer_activation(x):
    """ Linear function, returns input as is. """
    return x

def output_layer_activation_derivative(x):
    """ Returns the derivative of a linear function: 1. """
    return 1

class NeuralNetwork():
    """
        Contains the following functions:
            -train: tunes parameters of the neural network based on error obtained from forward propagation.
            -predict: predicts the label of a feature vector based on the class's parameters.
            -train_neural_network: trains a neural network over all the data points for the specified number of epochs during initialization of the class.
            -test_neural_network: uses the parameters specified at the time in order to test that the neural network classifies the points given in testing_points within a margin of error.
    """


    def __init__(self):

        # DO NOT CHANGE PARAMETERS (Initialized to floats instead of ints)
        self.input_to_hidden_weights = np.matrix('1. 1.; 1. 1.; 1. 1.')
        self.hidden_to_output_weights = np.matrix('1. 1. 1.')
        self.biases = np.matrix('0.; 0.; 0.')
        self.learning_rate = .001
        self.epochs_to_train = 10
        self.training_points = [((2,1), 10), ((3,3), 21), ((4,5), 32), ((6, 6), 42)]
        self.testing_points = [(1,1), (2,2), (3,3), (5,5), (10,10)]

    def train(self, x1, x2, y):
        #RELU function takes in only a scaler value thus a conversion is needed to vectorize it
        vec_relu = np.vectorize(rectified_linear_unit)
        vec_relu_derivative = np.vectorize(rectified_linear_unit_derivative)

        # Forward propagation
        #input node
        input_values = np.matrix([[x1], [x2]])  # 2 by 1

        #z = w*x + b or edge between the kth node in the (i-1) layer to the jth node in the ith layer
        hidden_layer_weighted_input = self.input_to_hidden_weights * input_values + self.biases  # should be 3 by 1
        #𝜎(z_1)= a_1 or our activation function relu with input z
        hidden_layer_activation = vec_relu(hidden_layer_weighted_input)  # 3 by 1
        #edge from activation to output node
        output = self.hidden_to_output_weights * hidden_layer_activation  # 1 by 1
        #𝜎(z_2) = a
        activated_output = output_layer_activation(output)  # 1 by 1

        # Compute gradients
        #𝛿𝐿=∇𝑎𝐶 ⊙ 𝜎′(𝑧_2)
        output_layer_error = (activated_output - y) * output_layer_activation_derivative(output)  # 1 by 1
        #𝛿_𝐿−1=((𝑊_𝐿)𝛿_𝐿) ⊙ 𝜎′(𝑧_𝐿−1) the 1 node
        hidden_layer_error = np.multiply((np.transpose(self.hidden_to_output_weights) * output_layer_error),
                                             vec_relu_derivative(hidden_layer_weighted_input))  # 3 by 1
        #∂𝐶/∂𝑏𝑖𝑗=𝛿𝑖𝑗
        bias_gradients = hidden_layer_error
        #∂𝐶/∂𝑤𝑖 = 𝛿𝑖(𝑎_𝑖−1)𝑇
        hidden_to_output_weight_gradients = np.transpose(hidden_layer_activation * output_layer_error)  # [3 by 1] * [1 by 1] = [3 by 1]
        #𝛿𝐿−1 = ((𝑊_𝐿)*𝛿_𝐿)⊙ 𝜎′(𝑧_𝐿−1)
        input_to_hidden_weight_gradients = np.transpose(input_values * np.transpose(hidden_layer_error))  # = [2 by 1] * [1 by 3] = [2 by 3]

        # Use gradients to adjust weights and biases
        self.biases = self.biases - self.learning_rate * bias_gradients
        self.input_to_hidden_weights = self.input_to_hidden_weights - self.learning_rate * input_to_hidden_weight_gradients
        self.hidden_to_output_weights = self.hidden_to_output_weights - self.learning_rate * hidden_to_output_weight_gradients

    def predict(self, x1, x2):

        vec_relu = np.vectorize(rectified_linear_unit)

        input_values = np.matrix([[x1], [x2]])  # 2 by 1

        hidden_layer_weighted_input = self.input_to_hidden_weights * input_values + self.biases  # should be 3 by 1
        hidden_layer_activation = vec_relu(hidden_layer_weighted_input)  # 3 by 1

        output = self.hidden_to_output_weights * hidden_layer_activation  # 1 by 1
        activated_output = output_layer_activation(output)  # 1 by 1
        
        return activated_output.item()

    # Run this to train your neural network once you complete the train method
    def train_neural_network(self):

        for epoch in range(self.epochs_to_train):
            for x,y in self.training_points:
                self.train(x[0], x[1], y)

    # Run this to test your neural network implementation for correctness after it is trained
    def test_neural_network(self):

        for point in self.testing_points:
            print("Point,", point, "Prediction,", self.predict(point[0], point[1]))
            if abs(self.predict(point[0], point[1]) - 7*point[0]) < 0.1:
                print("Test Passed")
            else:
                print("Point ", point[0], point[1], " failed to be predicted correctly.")
                return

x = NeuralNetwork()

x.train_neural_network()

# UNCOMMENT THE LINE BELOW TO TEST YOUR NEURAL NETWORK
x.test_neural_network()
