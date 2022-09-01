from math import sqrt
import os
from matplotlib import pyplot as plt
import numpy as np
from scipy import interpolate

os.chdir('C:\LAMMPS 64-bit 24Mar2022\Examples\pgnpmf')

def linitpl(target, arr, arry, index=0): # takes in dis and pot 20, target from dis100, 
    for i in range(index, len(arr[index:])-1): 
        if arr[index+i] < target and arr[index+i+1] > target:
            per = (target - arr[index+i]) / (arr[index+i+1] - arr[index+i]) # percentage way between dis20 and next dis20
            ans = arry[index+i] + per*(arry[index+i+1] - arry[index+i]) # linear interpolate for dis100 coordinate with dis 20 values
            return (ans, index+i)
    else:
        if target > arr[-1]:
            return (0, index)
        


potential20 = []
distance20 = []
potential100 = []
distance100 = []

with open("N20.txt") as f:
    lines = f.readlines()[4:]
    for line in lines:
        distance20.append(float(line.split()[1]))
        potential20.append(float(line.split()[2]))

with open("N100.txt") as f:
    lines = f.readlines()[4:]
    for line in lines:
        distance100.append(float(line.split()[1]))
        potential100.append(float(line.split()[2]))
    
epsilon20 = 990.62
sigma20 = 53.93
potential20 = [y/epsilon20 for y in potential20]
distance20 = [x/sigma20 for x in distance20]

epsilon100 = 9752.6
sigma100 = 82.84
potential100 = [y/epsilon100 for y in potential100]
distance100 = [x/sigma100 for x in distance100]

# data = np.array((distance100,potential100))
# tck,u = scipy.interpolate.splprep(data, s=0)
# unew = np.arange(0, 1.01, 0.01)
# out = scipy.interpolate.splev(unew, tck)

# data2 = np.array((distance20,potential20))
# tck2,u2 = scipy.interpolate.splprep(data2, s=0)
# unew2 = np.arange(0, 1.01, 0.01)
# out2 = scipy.interpolate.splev(unew2, tck2)


# plt.plot(out[0], out[1], color='orange')

# plt.plot(data[0,:], data[1,:])

# plt.show()
# plt.plot(distance20,potential20)
# plt.plot(distance100,potential100)
# plt.xlim(right=200)
# plt.ylim(top=40000)
# plt.xlabel("Interatomic distance (Angstroms)", fontsize='large')
# plt.ylabel("Potential Energy (Kcal/mol)", fontsize='large')

# plt.legend(('N=20', 'N=100'))
# plt.show()

potint = [] # potential for N=20 fitted to the points of N=100, to use for averaging
disint = []

disint = distance100
potint = []

# for dis in range(len(disint)):
#     if disint[dis] > 1:

for dis in distance100[1:]:
    index = 0
    result, ind = linitpl(dis, distance20, potential20, index)
    potint.append(result)
    index = ind
    
potint.append(0)


avgdis = disint
avgpota = []
avgpotg = []


potint = [x + 1 for x in potint]
potential100 = [x + 1 for x in potential100]
for dis in range(1, len(distance100)):
    try:
        avgpotg.append(sqrt(potint[dis] * potential100[dis]))
    except:
        print(potint[dis], potential100[dis])
        avgpotg.append(0)

potint = [x - 1 for x in potint]
potential100 = [x - 1 for x in potential100]
avgpotg = [x - 1 for x in avgpotg]
avgpotg.append(0)
    

for dis in range(1, len(distance100)):
    avgpota.append((potint[dis] + potential100[dis]) / 2) 
avgpota.append(0)




plt.plot(distance100, avgpota)
plt.plot(distance100, avgpotg)
plt.plot(distance100, potential100)
plt.plot(disint, potint)
plt.ylim(top=10)
plt.xlabel('r/σ')
plt.ylabel('Ψ/ε')
plt.legend(('arithmetic', 'geometric', 'N=100', 'N=20'))
plt.show()

em = sqrt(epsilon100 * epsilon20)
sm_g = sqrt(sigma100 * sigma20)
sm_a = (sigma100 + sigma20)/2

avgdis_a = [x*sm_a for x in avgdis]
avgdis_g = [x*sm_g for x in avgdis]
avgpotg = [y*em for y in avgpotg]
avgpota = [y*em for y in avgpota]

potential20 = [y*epsilon20 for y in potential20]
distance20 = [x*sigma20 for x in distance20]

potential100 = [y*epsilon100 for y in potential100]
distance100 = [x*sigma100 for x in distance100]

plt.plot(avgdis_a, avgpotg)
plt.plot(avgdis_g, avgpotg)
plt.plot(distance20, potential20)
plt.plot(distance100, potential100)
plt.legend(('arithmetic', 'geometric', 'N=20', 'N=100'))
plt.ylim(top=1000)
plt.ylabel('Ψ (Kcal/mol)', fontsize="large")
plt.xlabel('r (Angstrom)', fontsize="large")
plt.show()

tck = interpolate.splrep(avgdis_a, avgpotg, s=0)
#ynew = interpolate.splev(avgdis_a, tck, der=0)
yder = interpolate.splev(avgdis_a, tck, der=1)
yder = [y*(-1) for y in yder]
# plt.plot(avgdis_a, avgpotg)
# plt.plot(avgdis_a, yder)
# plt.legend(('potential', 'force'))
# plt.ylim(top=1000)
# plt.show()


# f = open('mixed_potential.txt', 'x')
# f.write('#Tabulated Double Exponential potential for NP, R20C25M20\n')
# f.write('DE_GNP\n')
# f.write('N %i\n\n' % len(avgdis_a))
# for i in range(len(avgdis_a)):
#     f.write('%i %.14f %.12f %.12f\n' % (i+1, avgdis_a[i], avgpotg[i], yder[i]))














