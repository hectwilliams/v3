"""
    Create simple XOR classification multilayer perception graph (neural network)
a
"""
import numpy as np 
import matplotlib.pyplot as plt 

def sigmoid (x: list | tuple) -> np.ndarray:
    """ compute logistic regression function"""
    return 1 /(1 + np.exp(-1*x))
def sigmoid_derivative (x: list | tuple) ->np.ndarray:
    """ compute logistic regression function"""
    invert_one_plus_exp = (1 + np.exp(-1*x))**-1
    return invert_one_plus_exp * (1 - invert_one_plus_exp)
def show_activation():
    x = np.linspace(-10, 10)
    y = sigmoid(x)
    y2 = sigmoid_derivative(x)
    plt.plot(x, y)
    plt.plot(x, y2, alpha=0.5)
    plt.show()
def heaviside(x):
    pos_indices = np.nonzero(x>0)
    neg_indices = np.nonzero(x<0)
    x[pos_indices[0], pos_indices[1]] = 1
    x[neg_indices[0], neg_indices[1]] = 0
l_rate = 0.1
rng = np.random.Generator(np.random.PCG64(42))
# setup neural network
input_size = 3 #  units -> x1 x2 b
hidden1_size = 3 # units -> h1 h2, b
output_size = 1 # units -> a
x_weights = rng.standard_normal(size=(hidden1_size-1, input_size))  # size (num_ of neuron units excluding bias neuron, num of inputs in layer)
h_weights = rng.standard_normal(size=(output_size, hidden1_size))
for i in range(10):
    x = np.array( [[1,1,1], [1,0,0], [1,0,1], [1,1,0], [1,0,0]  ] ,dtype=np.float32 )
    # label 
    y = np.array([0,0,1,1,0],dtype=np.float32)[:,None]
    # input/ weights
    h_ws = np.matmul(x, x_weights.T)
    h = sigmoid(h_ws)
    # hidden layer
    h = np.hstack((h, np.ones(shape=(h.shape[0],1) ))) # horiz append bias 
    a_ws = np.matmul(h, h_weights.T)
    a = (a_ws)
    #output later 
    cost = (a - y) ** 2
    avg_cost = np.mean(cost, axis=0)
    print(avg_cost)
    # backpropagation layer 2
    grad2 = 2 * a_ws * sigmoid_derivative(a_ws) * h
    grad2 = np.mean(grad2, axis=0)[:, None]
    h_weights_ = h_weights.T - l_rate*grad2
    # backpropagation layer 1 (unit 1)
    grad1 = 2 * a_ws * sigmoid_derivative(a_ws)* h_weights 
    l = x[:,None] * sigmoid_derivative(h_ws)[:,:, None]
    grad1 = grad1[:, None] * l
    grad1 =np.mean(grad1, axis=0)
    x_weights = x_weights - l_rate*grad1
print(h_weights)
print(x_weights)
# grad1 =  sigmoid_derivative(h_ws)
# * h_ws * sigmoid_derivative(h_ws)* x
# grad1 = np.mean(grad1, axis=0)[:, None]
# h_weights = h_weights - l_rate*grad2

