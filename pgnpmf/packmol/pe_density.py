import os
from matplotlib import pyplot as plt
import numpy as np

os.chdir('C:\\Users\\03022\\Desktop\\pgnpmf\\500500')
l = os.listdir()
lam = []

for f in l:
    if f[-6:] == 'lammps':
        lam.append(f)

print(lam)

# densit = [0.16421108, 0.22729624, 0.41212976, 0.60175091, 0.7969575, 0.8953416, 0.99615211, 1.0621828, 1.1299008, 1.1979153, 1.2622369, 1.3374095, 1.445961, 
# 1.5707356, 1.7115166, 1.8378004, 1.901097, 1.9222239, 1.9254894, 1.9283325, 1.9312017, 1.9305621, 1.9327647, 1.9350683, 1.9383652, 1.9392671, 
# 1.9383841, 1.9399374, 1.9415183, 1.9419307, 1.9405988, 1.9431549, 1.9434647]
# poten = [-2756500.7, -3882355.0, -7287647.8, -10926047.0, -14478870.0, -22696541.0, -25545773.0, -27199570.0, -27829353.0, -27970150.0, -28447693.0, -28654400.0, -28821017.0, -29807571.0, -30794610.0, -31855054.0, -32699382.0, -33093418.0, -33181277.0, -33010535.0, -33173780.0, -33023025.0, 
# -33264007.0, -33158534.0, -33236826.0, -33290912.0, -33181434.0, -33274069.0, -33305091.0, -33329645.0, -33290549.0, -33338058, -33332090]

density = []
poteng = []

for n in lam:
    with open(n) as f:
        lines = f.readlines()[::-1]
        for line in lines:
            try:
                if int(line.split()[0]):
                    poteng.append(float(line.split()[3]))
                    density.append(float(line.split()[4]))
                    break
            except:
                pass

print(density)
print(poteng)

arr = np.linspace(1, len(lam), len(lam))
plt.plot(arr, density)
plt.xlabel("Number of iterations")
plt.ylabel("Density (g/cm^3)")
plt.show()

plt.plot(arr, poteng)
plt.xlabel("Number of iterations")
plt.ylabel("Potential Energy (Kcal/mol)")
plt.show()