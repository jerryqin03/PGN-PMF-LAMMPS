from __future__ import annotations
import math
from typing import List, Tuple
import freud
import numpy as np
from matplotlib import pyplot as plt
import warnings
import os
from vector import vector3D as vector3D
from vector import particle as particle
import random


class system:

    def __init__(self, atom_list : List[particle], box_dims : List[float], cutoff : float) -> None:
        avg = sum(box_dims)/2
        self.atom_list = [atom - (avg, avg, avg) for atom in atom_list]
        self.box_dims = [box_dims[0] - avg, box_dims[1] - avg]
        
        atoms = (self.atom_list).copy()
        dims = [self.box_dims[0] - cutoff, self.box_dims[1] + cutoff]
        print(dims)
        box_length = self.box_dims[1] - self.box_dims[0]

        for x in [-1, 0, 1]:
            for y in [-1, 0, 1]:
                for z in [-1, 0, 1]:
                    if x == y == z == 0:
                        continue
                    for atom in self.atom_list:
                        new = atom - (x*box_length, y*box_length, z*box_length)
                        if new.in_box(dims):
                            atoms.append(new)

        self.periodic_atoms = atoms
        
    @classmethod
    def fromdump(cls, path : str, cutoff : float) -> system:
        with open(path) as f:
            lines = f.readlines()
            bd = [float(lines[5].split()[0]), float(lines[5].split()[1])]
            al = []
            for line in lines[9:]:
                al.append(particle.fromlist(line))
            return system(al, bd, cutoff)


    def make_periodic(self, cutoff) -> None:
        atoms = (self.atom_list).copy()
        dims = [self.box_dims[0] - cutoff, self.box_dims[1] + cutoff]
        box_length = self.box_dims[1] - self.box_dims[0]

        for x in [-1, 0, 1]:
            for y in [-1, 0, 1]:
                for z in [-1, 0, 1]:
                    if x == y == z == 0:
                        continue
                    for atom in self.atom_list:
                        new = atom - (x*box_length, y*box_length, z*box_length)
                        if new.in_box(dims):
                            atoms.append(new)

        setattr(self, "periodic_atoms", atoms)
        


    def lbod_bins():
        os.chdir("/Users/jerryqin/Desktop/Recent Research Stf")

        path = "trajectory_1_1_0.tensile.custom.xyz"

        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            # We read the number of particles, the system box, and the
            # particle positions into 3 separate arrays.
            N = int(np.genfromtxt(path, max_rows=1))
            box_data = np.genfromtxt(path, skip_header=1, max_rows=3)
            data = np.genfromtxt(path, skip_header=4, invalid_raise=False)

        box = freud.box.Box.from_box(box_data[:,1] - box_data[:,0])
        data = data[:, 1:]


        lbod = freud.environment.BondOrder(5, 'lbod')

        aq = freud.locality.AABBQuery(box, data)
        query_result = aq.query(data, dict(num_neighbors=4, exclude_ii=True))
        nlist = query_result.toNeighborList()
        r = lbod.compute((box, data), neighbors=nlist)

        return r

    def legendre0(o, l) -> float:

        if o == 0:
            return 1
        elif o == 1:
            return l
        elif o == 2:
            return 0.5*(3*(l**2) - 1)
        elif o == 3:
            return 0.5*(5*(l**3) - 3*l)
        elif o == 4:
            return (1/8)*(35*(l**4) - 30*(l**2) + 3)
        elif o == 5:
            return (1/8)*(63*(l**5) - 70*(l**3) + 15*l)
        elif o == 6:
            return (1/16)*(231*(l**6) - 315*(l**4) + 105*(l**2) - 5)
        else:
            raise Exception("U too big brain")
                
        
    def sphharm0(l, theta) -> float:
        return (math.sqrt((2*l+1)/(4*math.pi)) * system.legendre0(l, math.cos(theta)))

    def sph4(c):
        return (math.sqrt((2*4+1)/(4*math.pi)) * ((1/8)*(35*(c**2) - 30*(c) + 3)))

    def sph6(c):
        return (math.sqrt((2*6+1)/(4*math.pi)) * (1/16)*(231*(c**3) - 315*(c**2) + 105*(c) - 5))


    # use frued to find the 2D histogram of angles



    # define function for computing local bond order qi
    def qo(self, l : int, target : particle, cutoff : float) -> float:
        
        # periodic boundary conditions
        #periodic_atoms = self.periodic_atoms
        # final local bond order value
        qresult = 0

        # find list of neighbors within cutoff
        neigh_i = target.neighbors(self.periodic_atoms, cutoff)    
            
        # outer loop of neighbors of i
        for neigh in range(1):#neigh_i:

            # results of spherical harmonic summations
            sijk = 0
            skjk = 0
            sjij = 0

            # loop over neighbors j
            for j in range(len(neigh_i)):
                
                neigh_j = neigh_i[j].neighbors(self.periodic_atoms, cutoff)
                    
                # loop over neighbors k
                for k in range(len(neigh_j)):
                    ij = vector3D(target.position, neigh_i[j].position)
                    jk = vector3D(neigh_i[j].position, neigh_j[k].position)
                        
                    # find delta ijk and spherical harmonic
                    dijk = math.acos(ij.dot(jk) / (ij.magnitude * jk.magnitude))
                    sphharm = system.sphharm0(l, dijk)
                        
                    # sum results
                    sijk += sphharm

                    # loop over neighbors k'
                    for kp in range(k, len(neigh_j)):
                        jk = vector3D(neigh_i[j].position, neigh_j[k].position)
                        jkp = vector3D(neigh_i[j].position, neigh_j[kp].position)

                        # find delta kjk' and spherical harmonic
                        dkjk = math.acos(jk.dot(jkp) / (jk.magnitude * jkp.magnitude))
                        sphharm2 = system.sphharm0(l, dkjk)

                        # sum results
                        skjk += sphharm2
                    
                # loop over neighbros j'
                for jp in range(j, len(neigh_i)):
                    ij = vector3D(target.position, neigh_i[j].position)
                    ijp = vector3D(target.position, neigh_i[jp].position)

                    # find delta jij' and spherical harmonic
                    djij = math.acos(ij.dot(ijp) / (ij.magnitude * ijp.magnitude))
                    print(djij)
                    sphharm3 = system.sphharm0(l, djij)

                    # sum results
                    sjij += sphharm3

            # perform calculation
            print(sijk, sjij, skjk)
            qresult += sijk/(math.sqrt(abs(sjij)) * math.sqrt(abs(skjk)))
        
        qresult /= 1 #len(neigh_i)

        return qresult




    def q(self, l : int, target : particle, cutoff : float) -> float:
        
        # periodic boundary conditions
        #periodic_atoms = self.make_periodic(cutoff).atom_list
        # final local bond order value
        qresult = 0

        # find list of neighbors within cutoff
        neigh_i = target.find_neighbors(self.atom_list, self.box_dims, cutoff)
        print(len(neigh_i))

        for j in range(len(neigh_i)):

            neigh_j = neigh_i[j].find_neighbors(self.atom_list, self.box_dims, cutoff)
            
            # results of spherical harmonic summations
            sijk = 0
            skjk = 0
            sjij = 0

            for jp in range(len(neigh_i)):
                neigh_jp = neigh_i[jp].find_neighbors(self.atom_list, self.box_dims, cutoff)

                for jp2 in range(len(neigh_i)):
                    #print(target.position, neigh_i[j].position, neigh_i[jp].position)
                    ij = vector3D(target.position, neigh_i[jp].position)
                    ijp = vector3D(target.position, neigh_i[jp2].position)
                    costheta=ij.dot(ijp) / (ij.magnitude * ijp.magnitude)


                # find delta jij' and spherical harmonic
                    djij = math.acos(np.float32(costheta))
                
                #print(target.position, neigh_i[j].position, neigh_i[jp].position, djij, math.cos(djij)**2)
                    sphharm3 = system.sphharm0(l, djij)

                # sum results
                    sjij += sphharm3

                for k in range(len(neigh_jp)):
                    ij = vector3D(target.position, neigh_i[jp].position)
                    jk = vector3D(neigh_i[jp].position, neigh_jp[k].position)

                    #print(target.position, neigh_i[jp].position, neigh_jp[k].position) 
                    #print(ij.dx, ij.dy, ij.dz)
                    #print(jk.dx, jk.dy, jk.dz)
                    # find delta ijk and spherical harmonic
                    cosijk = ij.dot(jk) / (ij.magnitude * jk.magnitude)
                    
                    dijk = math.acos(np.float32(cosijk))
                    sphharm = system.sphharm0(l, dijk)
                        
                    # sum results
                    sijk += sphharm

            for k in range(len(neigh_j)):
                for kp in range(len(neigh_j)):
                    jk = vector3D(neigh_i[j].position, neigh_j[k].position)
                    jkp = vector3D(neigh_i[j].position, neigh_j[kp].position)

                    # find delta kjk' and spherical harmonic
                    coskjk = jk.dot(jkp) / (jk.magnitude * jkp.magnitude)

                    dkjk = math.acos(np.float32(coskjk))
                    sphharm2 = system.sphharm0(l, dkjk)

                    # sum results
                    skjk += sphharm2                                                         
            #print(sijk, sjij, skjk)
            qresult += sijk/(math.sqrt(sjij) * math.sqrt(skjk))

        if len(neigh_i) == 0:
            return 0

        qresult /= len(neigh_i)
        print(qresult)

        return (qresult)
                




    def q_ave(self, l : int, target : particle, cutoff : float) -> float:
        
        nei = target.find_neighbors(self.atom_list, self.box_dims, cutoff)
        sum = self.q(l, target, cutoff)

        for j in nei:
            sum += self.q(l, j, cutoff)

        result = sum / (1 + len(nei))
        return result

    
    def plot_qave(self, num : int, pair : Tuple[int], cutoff : float):
        x = []
        y = []
        ran = random.sample(range(0,500), num)
        for r in ran:
            x.append(self.q_ave(pair[0], self.atom_list[r], cutoff))
            y.append(self.q_ave(pair[1], self.atom_list[r], cutoff))
        
        plt.scatter(x,y)
        plt.xlabel("q%i" % (pair[0]))
        plt.ylabel("q%i" % (pair[1]))
        plt.show()

        
