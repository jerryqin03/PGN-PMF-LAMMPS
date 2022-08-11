from cmath import sqrt
import cmath
from math import pi
import numpy as np
import matplotlib.pyplot as plt
import os


select_atomtype=2 #atomtype of oxygen used to calculate O-O rdf
nframes=201 #number of frames
c=[] #xyz coordinates of all oxygen
b=[] #xyz boundaries

os.chdir("C:\LAMMPS 64-bit 24Mar2022\Examples\water")
#read coordinates
with open('water.dump', 'r') as file: 
	for n in range(nframes):
		c.append([])
		b.append([])
		n_sel_atom=0
		file.readline() 
		file.readline()
		file.readline() 
		natoms=int(file.readline().split()[0])
		file.readline() 
		for i in range(3): 
			row=file.readline().split() 
			b[n].append(np.array(row).astype(float)) 
		file.readline()
		
		#read coordinates of selected atomtype into your c object
		for line in range(900):
			row = file.readline().split()
			if int(row[1]) == select_atomtype:
				c[n].append(np.array(row[2:]).astype(float))


#transform to numpy array
b=np.array(b)
c=np.array(c)
n_sel_atom = len(c[0])

binwidth = 0.05
maxhistlen = 10 #maximum distance to use in rdf calculation
nbin=int(maxhistlen/binwidth) #number of bins

Vtotal = [(l[0][1]*2)**3 for l in b] #system volume
rho = [n_sel_atom/V for V in Vtotal] #calculate the density of the box for each frame


out=np.zeros(nbin)
for frame in range(nframes): 
	histogram=np.zeros(nbin)
	for atom in range(n_sel_atom): 
		cnew=c[frame]-c[frame][atom] 
		#first shift frame such that atom at at (0,0,0) --> center of box
		
		#account for pbc conditions in all necessary dimensions

		#cnew = np.where([[abs(cnew[:,0]) > b[frame][0][1], abs(cnew[:,1]) > b[frame][0][1], abs(cnew[:,2]) > b[frame][0][1]]]*len(cnew), [[abs(cnew[:,0]) % (b[frame][0][1]) - (b[frame][0][1]), abs(cnew[:,1]) % (b[frame][0][1]) - (b[frame][0][1], abs(cnew[:,2]) % (b[frame][0][1]) - (b[frame][0][1]))]]*len(cnew), [[cnew[:,0], cnew[:,1], cnew[:,2]]] * len(cnew))

		for loc in range(len(cnew)):
			if atom != loc:
				for coord in range(3):
					if abs(cnew[loc][coord]) > b[frame][0][1]:
						#print(cnew[loc][coord], end=' ')
						cnew[loc][coord] = abs(cnew[loc][coord]) % (b[frame][0][1]) - (b[frame][0][1])
						#print(cnew[loc][coord])
			#then do the real calculation - distance is easy now because reference atom is at (0,0,0)
			#
			# ... calculate the distance dx and add 1 to the corresponding bin
				dist = cmath.sqrt(cnew[loc][0]**2 + cnew[loc][1]**2 + cnew[loc][2]**2)
				if (np.real(dist) < maxhistlen): 
					try:
						histogram[int(np.real(dist)//binwidth)] += 1
					except:
						print(cnew[loc])
		
        
    #normalize the rdf here with resulting normalized rdf being the list "out"
	for bin in range(1, len(histogram)):
		vol = (4/3)*pi*((binwidth*(bin+1))**3 - (binwidth*(bin))**3)
		histogram[bin] /= vol
	
	histogram /= n_sel_atom
	histogram /= rho[frame]
	out = out + histogram

out /= nframes




xlist = [0.05*x for x in range(nbin)]#define your corresponding r values for the abscissa


os.chdir("C:\LAMMPS 64-bit 24Mar2022\Examples\water")

x = []
y = []
with open("oxygen.rdf") as f:
    lines = f.readlines()
    lines = lines[4:]
    for line in lines:
        x.append(float(line.split()[1]))
        y.append(float(line.split()[2]))
    
#plotting - or write your own output method and plot with your favorite tool
plt.plot(xlist,out, x, y)
plt.xlabel(r"Distance (Angstroms)")#labeling
plt.ylabel(r"g(r)")#labeling
plt.ylim()#limits
plt.xlim(right=10.5)#limits
#plt.grid(True)
plt.tight_layout()
#plt.savefig(".jpg", dpi=300, optimize=True)
plt.show()
