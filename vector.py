from __future__ import annotations
import math
from typing import List, Tuple


class vector3D:
    def __init__(self, p1, p2) -> None:
        self.dx = p2[0] - p1[0]
        self.dy = p2[1] - p1[1]
        self.dz = p2[2] - p1[2]
        self.magnitude = math.sqrt(self.dx**2 + self.dy**2 + self.dz**2)
    
    def dot(self, other) -> float:
        return (self.dx * other.dx + self.dy * other.dy)

    def acos(inp : float) -> float:
        if math.asin(inp) >= 0:
            return math.acos(inp)
        else:
            return math.pi + math.acos(inp)


class particle:
    def __init__(self, k : int, pos : Tuple[float]) -> None:
        self.kind = k
        self.position = pos    
    
    @classmethod
    def fromlist(cls, str) -> particle:
        lis = str.split()
        kind = int(lis[0])
        position = (float(lis[1]), float(lis[2]), float(lis[3]))
        return particle(kind, position)

    def neighbors(self, atom_list : List[particle], cutoff : float, kind : bool =False) -> List[particle]:
        coordinate = self.position
        neigh_list = []
        atom_list = [atom - coordinate for atom in atom_list]
        if not kind:
            for atom in atom_list:
                if math.sqrt((atom.position[0])**2 + (atom.position[1])**2 + (atom.position[2])**2) < cutoff and atom != self:
                    neigh_list.append(atom)
        else:
            for atom in atom_list:
                if math.sqrt((atom.position[0])**2 + (atom.position[1])**2 + (atom.position[2])) < cutoff and atom.kind == self.kind and atom != self:
                    neigh_list.append(atom)
    
        return neigh_list
    
    def __eq__(self, other) -> bool:
        return (self.kind == other.kind and self.position == other.position)

    def __ne__(self, __o: object) -> bool:
        return (self.kind != __o.kind or self.position != __o.position)

    def __sub__(self, other : Tuple[float]) -> particle:
        return particle(self.kind, (self.position[0] - other[0], self.position[1] - other[1], self.position[2] - other[2]))

    def __add__(self, other : Tuple[float]) -> particle:
        return particle(self.kind, (self.position[0] + other[0], self.position[1] + other[1], self.position[2] + other[2]))





    



