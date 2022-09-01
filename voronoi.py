import matplotlib.pyplot as plt
import numpy as np
import os
import sys

N20 = []
N100 = []

for i in np.linspace(0, 100, 11, dtype=int):
    n20 = []
    n100 = []
    volume = 0

    with open("/home/jjq4271/pgnpmf/trial2/%i%i/voronoi/voronoi_1_1.custom" % (i, 100-i)) as f:
        lines = f.readlines()
        volume += (float(lines[5].split()[1]) - float(lines[5].split()[0]))**3
        for line in lines[9:]:
            l = line.split()
            if l[0] == "1":
                n20.append(float(l[-2]))
            else:
                n100.append(float(l[-2]))

    if i == 0:
        N20.append(0)
        N100.append((sum(n100) / len(n100)))
    elif i == 100:
        N20.append((sum(n20) / len(n20)))
        N100.append(0)
    else:
        avg20 = (sum(n20) / len(n20))
        avg100 = (sum(n100) / len(n100))
        N20.append(avg20)
        N100.append(avg100)


plt.plot(np.linspace(1, 100, 9), N20[1:-1])
plt.plot(np.linspace(1, 100, 9), N100[1:-1])
plt.legend(("N20", "N100"))
plt.xlabel("Percent composition of N20 PGN (%)")
plt.ylabel("Average volume of PGN")
plt.savefig("voronoi.png")







