from __future__ import annotations
from math import sqrt as sqrt
from typing import List, Tuple
import numpy as np


class vector3D:
    def __init__(self, p1 : List[float], p2 : List[float]) -> None:
        self.dx = p2[0] - p1[0]
        self.dy = p2[1] - p1[1]
        self.dz = p2[2] - p1[2]
        self.magnitude = sqrt(self.dx**2.0 + self.dy**2.0 + self.dz**2.0)
        if self.magnitude == 0:
            print(p1, p2)
            raise Exception("0 magnitude")
        self.unit = (self.dx/self.magnitude, self.dy/self.magnitude, self.dz/self.magnitude)
    
    @classmethod
    def vec(cls, dx : float, dy : float, dz : float) -> vector3D:
        cls.dx = dx
        cls.dy = dy
        cls.dz = dz

        return cls((0, 0, 0), (dx, dy, dz))

    def dot(self, other : vector3D) -> float:
        return (self.dx * other.dx + self.dy * other.dy + self.dz * other.dz)
        

    def __add__(self, other : Tuple[float]) -> Tuple[float]:
        return (self.dx + other[0], self.dy + other[1], self.dz + other[2])
        
    def __mul__(self, other : float) -> vector3D:
        return vector3D.vec(other * self.dx, other * self.dy, other * self.dz)

class particle:
    def __init__(self, k : int, pos : Tuple[float]) -> None:
        self.kind = k
        self.position = pos    
    
    @classmethod
    def fromlist(cls, str) -> particle:
        lis = str.split()
        kind = int(lis[1])
        position = (float(lis[2]), float(lis[3]), float(lis[4]))
        return cls(kind, position)

    def neighbors(self, atom_list : List[particle], cutoff : float, kind : bool = False) -> List[particle]:
        coordinate = self.position
        neigh_list = []
        atom_list = [atom - coordinate for atom in atom_list]
        if not kind:
            for atom in atom_list:
                if (sqrt((atom.position[0])**2 + (atom.position[1])**2 + (atom.position[2])**2) < cutoff) and (atom.position != (0.0, 0.0, 0.0)):
                    neigh_list.append(atom + coordinate)
        else:
            for atom in atom_list:
                if (sqrt((atom.position[0])**2 + (atom.position[1])**2 + (atom.position[2])) < cutoff) and (atom.kind == self.kind) and (atom != self):
                    neigh_list.append(atom + coordinate)
    
        return neigh_list

    def find_neighbors(self, atom_list : List[particle], box_dims : List[float], cutoff : float) -> List[particle]:
        nei_list = []
        box_dimsi = [1/bd for bd in box_dims]
        
        for atom in atom_list:
            dx = atom.position[0] - self.position[0]
            dy = atom.position[1] - self.position[1]
            dz = atom.position[2] - self.position[2]

            dx = dx - box_dims[1] * np.round(dx * box_dimsi[1])
            dy = dy - box_dims[1] * np.round(dy * box_dimsi[1])
            dz = dz - box_dims[1] * np.round(dz * box_dimsi[1])

            if (sqrt(dx**2 + dy**2 +dz**2) < cutoff) and (atom.position != self.position):
                nei_list.append(atom)

        
        return nei_list
            



    def find_neighbors_bad(self, atom_list : List[particle], box_dims : List[float], cutoff : float) -> List[particle]:
        coordinate = self.position
        neigh_list = []
        atom_list = [atom - coordinate for atom in atom_list]

        for atom in atom_list:
            if atom.position != (0,0,0):
                v = vector3D((0,0,0), atom.position)
                if v.magnitude > box_dims[1]:
                    periodic = vector3D.vec(*v.unit) * (-1 * (box_dims[1] - box_dims[0])) + atom.position 
                    if sqrt(periodic[0]**2 + periodic[1]**2 + periodic[2]**2) < cutoff:
                        print("periodic pos: ", periodic[0], periodic[1], periodic[2], sqrt(periodic[0]**2 + periodic[1]**2 + periodic[2]**2))
                        neigh_list.append(atom + coordinate)
                else:
                    if (v.magnitude < cutoff):
                        print("pos: ", atom.position, v.magnitude)
                        neigh_list.append(atom + coordinate)

        return neigh_list

    def in_box(self, bl) -> bool:
        for dim in range(3):
            if self.position[dim] > bl[1] or self.position[dim] < bl[0]:
                return False
        
        return True
    
    def __eq__(self, other) -> bool:
        return (self.kind == other.kind and self.position == other.position)

    def __ne__(self, __o: object) -> bool:
        return (self.kind != __o.kind or self.position != __o.position)

    def __sub__(self, other : Tuple[float]) -> particle:
        return particle(self.kind, (self.position[0] - other[0], self.position[1] - other[1], self.position[2] - other[2]))

    def __add__(self, other : Tuple[float]) -> particle:
        return particle(self.kind, (self.position[0] + other[0], self.position[1] + other[1], self.position[2] + other[2]))





    






