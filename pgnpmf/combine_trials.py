import os
from matplotlib import pyplot as plt
import numpy as np
import sys
import scipy.interpolate as interpolate

def integ(x, tck, constant=0):
    x = np.atleast_1d(x)
    out = np.zeros(x.shape, dtype=x.dtype)
    for n in range(len(out)):
        out[n] = interpolate.splint(0, x[n], tck)
    out += constant
    return out


if sys.argv[1] == "i":

    density = []
    composition = []


    for i in range(1, 5):
        den = []
        comp = []

        n1 = 0
        n2 = 100
        
        for iter in range(0,11):

            comp.append(n1)

            os.chdir("/home/jjq4271/pgnpmf/trial%i/%i%i" % (i, n1, n2))
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
            
            n1 += 10
            n2 -= 10

        density.append(den)
        composition.append(comp)

    os.chdir("/home/jjq4271/pgnpmf")
    for i in range(4):
        plt.plot(composition[i], density[i])
        
    plt.legend(("Trial 1", "Trial 2", "Trial 3", "Trial 4"))
    plt.xlabel("% Composition of N20 PGN")
    plt.ylabel("Density (g/cm^3)")
    plt.savefig("4compare_dens.png")

elif sys.argv[1] == "T":

    composition = []
    toughness = []

    for i in range(1,4):
        os.chdir("/home/jjq4271/pgnpmf/tensile/%s" % (i))
        comp = []
        T = []

        for n in np.linspace(0, 100, 11, dtype=int):
            with open ('tensile%s%s_1_%s.txt' % (n, 100-n, i)) as f:
                s = []
                e = []
                lines = f.readlines()[1:]
                for line in lines:
                    args = line.split()
                    e.append((float(args[0]) + 1)**3 - 1)
                    s.append((float(args[1]) + float(args[2]) + float(args[3]))/3)


                #x = np.arange(0, 2*np.pi+np.pi/4, 2*np.pi/8)
                #y = np.sin(x)
                tck = interpolate.splrep(e[:28204], s[:28204], s=0)
                #enew = np.arange(0, e[-1], len(e))
                snew = interpolate.splev(e[:28204], tck, der=0)
                Tint = integ(e[:28204], tck)

                comp.append("%i" % (n))
                T.append(Tint[-1])
            #plt.plot(e, Tint)

        composition.append(comp)
        toughness.append(T)

    os.chdir("/home/jjq4271/pgnpmf")
    for i in range(3): 
        plt.plot(composition[i], toughness[i])
        #plt.legend(tuple([(x + "% N20") for x in np.linspace(0, 100, 11, dtype=str)]))
    plt.xlabel("% N20 PGN composition")
    plt.ylabel("Toughness (GPa)")
    plt.legend(("Trial1", "Trial2", "Trial3"))
    plt.savefig("3combine_toughness.png")

elif sys.argv[1] == "E":
    
    composition = []
    modulus = []

    for i in range(1,4):
        os.chdir("/home/jjq4271/pgnpmf/tensile/%s" % (i))
        comp = []
        E = []

        for n in np.linspace(0, 100, 11, dtype=int):
            with open ('tensile%s%s_1_%s.txt' % (n, 100-n, i)) as f:
                s = []
                e = []
                lines = f.readlines()[1:]
                for line in lines:
                    args = line.split()
                    e.append((float(args[0]) + 1)**3 - 1)
                    s.append((float(args[1]) + float(args[2]) + float(args[3]))/3)


                #x = np.arange(0, 2*np.pi+np.pi/4, 2*np.pi/8)
                #y = np.sin(x)
                tck = interpolate.splrep(e, s, s=0)
                #enew = np.arange(0, e[-1], len(e))
                snew = interpolate.splev(e, tck, der=1)
                comp.append(n*10)
                E.append(snew[40])
        
        composition.append(comp)
        modulus.append(E)
        
    os.chdir("/home/jjq4271/pgnpmf/tensile")

    for i in range(3):
        plt.plot(composition[i], modulus[i])
    
    plt.xlabel("% N20 PGN composition")
    plt.ylabel("Young's Modulus (GPa)")
    plt.legend(("Trial 1", "Trial 2", "Trial 3"))
    plt.savefig("3combine_E.png")  

