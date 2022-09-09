import scipy.interpolate as interpolate
import numpy as np
from matplotlib import pyplot as plt
import os
import sys

def integ(x, tck, constant=0):
    x = np.atleast_1d(x)
    out = np.zeros(x.shape, dtype=x.dtype)
    for n in range(len(out)):
        out[n] = interpolate.splint(0, x[n], tck)
    out += constant
    return out


os.chdir("/home/jjq4271/pgnpmf/tensile/%s" % (sys.argv[1]))

if sys.argv[2] == "T":

    comp = []
    T = []

    for n in np.linspace(0, 100, 11, dtype=int):
        with open ('tensile%s%s_1_%s.txt' % (n, 100-n, sys.argv[1])) as f:
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

    plt.plot(comp, T)
    #plt.legend(tuple([(x + "% N20") for x in np.linspace(0, 100, 11, dtype=str)]))
    plt.xlabel("% N20 PGN composition")
    plt.ylabel("Toughness (GPa)")
    plt.savefig("toughness%s.png" % (sys.argv[1]))

elif sys.argv[2] == "E":

    comp = []
    E = []

    for n in np.linspace(0, 100, 11, dtype=int):
        with open ('tensile%s%s_1_%s.txt' % (n, 100-n, sys.argv[1])) as f:
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
            comp.append(n)
            E.append(snew[40])
    
    plt.plot(comp, E)
    plt.xlabel("% N20 PGN composition")
    plt.ylabel("Young's Modulus (GPa)")
    plt.savefig("E%s.png" % (sys.argv[1]))   