import numpy as np
version = [2]
np.savetxt("version.txt", version)
a = open("version.txt").read()
a = int(float(a))