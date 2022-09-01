import os
from matplotlib import pyplot as plt
import numpy as np
import sys

if sys.argv[1] == "i":
    pot = []
    den = []

    n1 = 0
    n2 = 1000

    for i in range(0,11):
        os.chdir("/home/jjq4271/pgnpmf/trial1/%i%i" % (n1, n2))
        l = os.listdir()
        
        lamp = []

        for f in l:
            if f[-6:] == 'lammps':
                lamp.append(f)
        
        lam = [" "]*len(lamp)

        for l in lamp:
            lam[int(l[6:-7]) - 1] = l

        density = []
        poteng = []

        for n in lam:
            #iter.append(int(n[6:-7]))
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


        plt.plot(np.linspace(1,len(density), len(density)), density)
        #pot.append(poteng)
        #den.append(density)
        n1 += 100
        n2 -= 100
        os.chdir("/home/jjq4271/pgnpmf")

    plt.xlabel("Numbner of iterations")
    plt.ylabel("Density (g/cm^3)")
    plt.legend(tuple([(x + "% N20") for x in np.linspace(0, 100, 11, dtype=str)]))
    #plt.legend(("0 1000", "100900", "200800", "300700", "400600", "500500", "600400", "700300", "800200", "900100", "1000 0"))
    plt.savefig('density3.png')

elif sys.argv[1] == "c":
    n1 = 0
    n2 = 1000

    den = []
    comp = []
    
    for i in range(0,11):

        comp.append(n1/100)

        os.chdir("/home/jjq4271/pgnpmf/trial1/%i%i" % (n1, n2))
        l = os.listdir()
        
        lamp = "logequ1.lammps" 

        for f in l:
            if f[-6:] == 'lammps' and (int(f[6:-7]) > int(lamp[6:-7])):
                lamp = f
        
        with open(lamp) as g:
            lines = g.readlines()[::-1]
            for line in lines:
                try:
                    if int(line.split()[0]):
                        den.append(float(line.split()[4]))
                        break
                except:
                    pass
        
        n1 += 100
        n2 -= 100
    
    os.chdir("/home/jjq4271/pgnpmf")
    plt.plot(comp, den)
    plt.xlabel("% Composition of N20 PGN")
    plt.ylabel("Density (g/cm^3)")
    plt.savefig("Den vs comp3_1.png")

else:
    print("Invalid flag")
    

