import NeuralNet as nNet 
import numpy as np
#entradas simuladas pos x,y distancia con el tubo 3 entradas 1 salida
nn = nNet.NeuralNetwork([3,2,1],activation="tanh")

X = np.array([250,250,40])

print(nn.predict(X))

