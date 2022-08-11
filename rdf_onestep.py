import numpy as np
from matplotlib import pyplot as plt
import os

os.chdir("C:\LAMMPS 64-bit 24Mar2022\Examples\iron")

x = []
y = []
with open("bulk.rdf") as f:
    lines = f.readlines()
    lines = lines[4:]
    for line in lines:
        x.append(float(line.split()[1]))
        y.append(float(line.split()[2]))
    
plt.figure()
plt.plot(x,y)
plt.show()