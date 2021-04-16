import numpy as np
from scipy import linalg


vector = np.array([6.342134124 , 54.123124124])

print("Original: {}".format(vector))

unitario = vector / linalg.norm(vector)

print("Normalizado: {} , longitud: {}".format(unitario, linalg.norm(unitario)))


