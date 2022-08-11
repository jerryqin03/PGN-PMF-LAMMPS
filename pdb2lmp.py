dim = 6000.0
atom_types = {"Pgna":(1, 0), "Pgnb":(2, 0)}
masses = [221851.569, 422051.5699]
bond_type = "zero"
angle_type = "zero"
inp = open("C:\\Users\\03022\\Desktop\\pgnpmf109.pdb", "r")
out = open("C:\\Users\\03022\\Desktop\\pgnpmf109.dat", "x")

def format(inlst):
    output = ""
    inlst = inlst.split()
    output += str(inlst[1]) + " " + str(atom_types[inlst[2]][0]) + " "\
        + " " + str(inlst[5]) + " "\
            + str(inlst[6]) + " " + str(inlst[7])
    return output

lines = inp.readlines()
bonds = []
angles = []
if lines[-1] == 'END\n':
    lines.pop(-1)
while True:
    l = lines[0].split()
    if l[0] != "HETATM":
        lines.pop(0)
    else:
        break

while (lines[-1].split()[0] == "CONECT"):
    if (len(lines[-1].split()) == 3):
        bonds.insert(0, lines[-1].split())       
    else:
        angles.insert(0, lines[-1].split())
    lines.pop(-1)
#lines = lines[5:]

out.write("LAMMPS data file, Author: Jerry Qin\n\n")
out.write('%d atoms\n' % (len(lines)))
out.write('%d bonds\n' % (len(bonds)))
out.write('%d angles\n\n' % (len(angles)))
out.write('%d atom types\n\n' % (len(atom_types)))

for dimension in ['x','y','z']:
    out.write('0.0 %d %slo %shi\n' % (dim, dimension, dimension))

out.write('\nMasses\n')
for i in range(len(atom_types)):
    out.write('%d %d\n' % (i+1, masses[i]))

out.write('\nAtoms\n\n')

i = 1
for line in lines:
    try:
        if (format(line) == ""):
            print("error")
        out.write(format(line))
        out.write('\n')
        print(i)
        i += 1
    except:
        print(line)
        break

if len(bonds) != 0:
    out.write('\nBonds\n')
    for i in range(len(bonds)):
        try:
            out.write('%s %s %s %s\n' % (i, bond_type, bonds[i][1], bonds[i][2]))
        except:
            print(bonds[i])
            break

if len(angles) != 0:
    out.write('\nAngles\n')
    for i in range(len(angles)):
        try:
            out.write('%s %s %s %s %s\n' % (i, angle_type, angles[i][1], angles[i][2], angles[i][3]))
        except:
            print(bonds[i])
            break

inp.close()
out.close()