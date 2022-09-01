import os 
from matplotlib import pyplot as plt

os.chdir("/home/jjq4271/pgnpmf")

stress = []
strain = []

with open ('tensile_1_1.txt') as f:
    lines = f.readlines()[1:]
    for line in lines:
        strain.append(float(line.split()[0]))
        stress.append(float(line.split()[1]))

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


plt.plot(strain, stress)
plt.xlabel("strain")
plt.ylabel("stress (GPa)")
plt.xlim(left=0, right=1)
plt.savefig("test.png")