import numpy as np
import matplotlib.pyplot as plt
import os

n1 = [3, 300]
n2 = [7, 700]

for i in range(0,2):
    os.chdir("/home/jjq4271/pgnpmf/%i%i" % (n1[i], n2[i]))
    l = os.listdir()
        
    lamp = []

    for f in l:
        if f[-6:] == 'lammps':
            lamp.append(f)
        
    lam = [" "]*len(lamp)

    for l in lamp:
        lam[int(l[6:-7]) - 1] = l

    density = []

    for n in lam:
        #iter.append(int(n[6:-7]))
        with open(n) as f:
            lines = f.readlines()[::-1]
            for line in lines:
                try:
                    if int(line.split()[0]):
                        density.append(float(line.split()[4]))
                        break
                except:
                    pass
    
    plt.plot(np.linspace(1,len(density), len(density)), density)

plt.savefig("compare_density.png")