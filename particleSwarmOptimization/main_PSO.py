import numpy as np
import pyswarms as ps
from cellbedform_PSO import CellBedform
from scipy.optimize import minimize
from scipy.optimize import differential_evolution
import os

# Problemas: 
# Contra que comparo
# Como el optimizer puede encontrar algo si la funcion me devuelve por cada step un corte en x, verifica cada step?
# Que corte elegimos, analiza todos? - Se analiza solo en uno
# Que parametros deberia optimizar?

#Requisitos:Parte 2:
# 1. Centrar una ventana de analisis entre experimental centrada para experimental y numerica 
# 2. ⁠definir que la númerica tenga los mismos datos 
# 3. ⁠generar funcion objetivo de optimización que compara diferencia de distancia en x e y del pico de la fft al cuadrado

# Para centrar se define una ventana central de la experimental en la que se define una longitud de datos.
# Identificando su centro, y cogiendo donde corta el eje x, a partir de esto

# Luego se toma eso y se hace lo mismo en experimental.

# A ambas ventas se saca la fft y los valores a comparar

#https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.differential_evolution.html#scipy.optimize.differential_evolution

file_path = os.path.join("ExperimentalData", "80thPass2ms.txt")
data_exp = np.loadtxt(file_path)
dx = len(data_exp)
print("AMOUNT DATA: ", dx)
dy = 40
y_cut = 20
steps = 101

# Objective function to minimize (quadratic function)
def objective_function(params):
    D_,Q_,L0_, b_ = params
    cb = CellBedform(grid=(dx, dy), D=D_, Q=Q_, L0=L0_, b=b_, y_cut=y_cut)
    y_cuts = cb.run(steps)
    print(y_cuts[1])
    diff = y_cuts[1] - data_exp[:, 1] 
    print(diff)
    print(np.sum(diff**2))
    return np.sum(diff**2)

# Initial guess for the parameters
params_initial = [0.1,0.8,2, 2]

# Call the optimizer
result = minimize(objective_function, params_initial, method='Nelder-Mead')

# The optimal parameters are stored in result.x
print(result)
print(result.x)

# Define the bounds for each parameter
# bounds = [(0, 10), (0, 10)]  # Example bounds, adjust as needed

# # Call the optimizer
# result = differential_evolution(objective_function, bounds)
# # The optimal parameters are stored in result.x
# print(result)
# print(result.x)

# Initialize the swarm
# num_particles = 10
# dimensions = 3
# options = {'c1': 0.5, 'c2': 0.3, 'w': 0.9}

# # Create a Particle Swarm Optimizer
# optimizer = ps.single.GlobalBestPSO(n_particles=num_particles, dimensions=dimensions, options=options)

# # Run the optimization
# best_position, _ = optimizer.optimize(objective_function, iters=100)

# # Display the result
# print("Best Position:", best_position)
# print("Objective Value at Best Position:", objective_function(best_position))


