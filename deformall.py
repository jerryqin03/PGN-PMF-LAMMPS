import os
import subprocess
import sys
import numpy as np

trial = int(sys.argv[1])
os.makedirs('/home/jjq4271/pgnpmf/tensile/%s' % (trial), exist_ok=True)

for i in np.linspace(0, 100, 11, dtype=int):

    os.chdir("/home/jjq4271/pgnpmf/trial%i/%i%i" % (trial, i, 100-i))
    os.makedirs("tensile/trajectory", exist_ok=True)
    os.makedirs("tensile/restart", exist_ok=True)

    l = os.listdir()
        
    lamp = []

    for f in l:
        if f[-3:] == 'res':
            lamp.append(f)

    os.chdir("/home/jjq4271")
    subprocess.run(['sbatch', 'deform.sh', '%s' % (i), '%s' % (100-i), '%s' % (trial), '%s' % (len(lamp) - 1)])