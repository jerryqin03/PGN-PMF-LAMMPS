import os 
from matplotlib import pyplot as plt
import numpy as np
import sys

os.chdir("/home/jjq4271/pgnpmf/tensile/%s" % (sys.argv[1]))

stress = []
strain = []

for n in np.linspace(0, 100, 11, dtype=int):
    with open ('tensile%s%s_1_%s.txt' % (n, 100-n, sys.argv[1])) as f:
        s = []
        e = []
        lines = f.readlines()[1:]
        for line in lines:
            args = line.split()
            e.append((float(args[0]) + 1)**3 - 1)
            s.append((float(args[1]) + float(args[2]) + float(args[3]))/3)
        
        stress.append(s)
        strain.append(e)

# with open('log.lammps') as f:
#     lines = f.readlines()
#     data = []

    
#     for i in range(len(lines)):
#         if len(lines[i].split()) > 0 and lines[i].split()[0] == '0':
#             x = 0
#             while(True):
#                 try:    
#                     data.append(lines[i+x])
#                     strain.append(float(lines[i+x].split()[10]))
#                     stress.append(float(lines[i+x].split()[28]))
#                     x += 1
#                 except:
#                     break
#             break


# print(strain)
# print(stress)

# plt.plot(strain,stress)
# plt.xlabel("Engineering strain")
# plt.ylabel("Stress (GPa)")
# plt.show()


# with open("stress-strain_N20.csv") as f:
#     lines = f.readlines()
#     lines = lines[1:]

#     for line in lines:
#         stress.append(float(line.split()[1]))
#         strain.append(float(line.split()[0]))

for i in range(0, 11):
    plt.plot(strain[i], stress[i])

plt.xlabel("Volumetric strain")
plt.ylabel("Average stress (GPa)")
plt.xlim(left=0, right=1)
plt.legend(tuple([(x + "% N20") for x in np.linspace(0, 100, 11, dtype=str)]))
plt.savefig("ss_%s.png" % (sys.argv[1]))