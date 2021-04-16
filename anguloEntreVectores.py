import numpy as np

v0 = [0, 4]     # correspondería a la orientacion del coche
v1 = [4, 0]     # vector objetivo(con respecto a la pos del coche)

# vector = np.array(p1) - np.array(p2)

angle = np.math.atan2(np.linalg.det([v0,v1]),np.dot(v0,v1))

print(angle)