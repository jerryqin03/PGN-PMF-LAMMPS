import numpy as np
from matplotlib import pyplot as plt
import time

def rdf(timestep, data):
    row = 0
    for i in range(0, np.size(data,0)):
        if data[i,0] == timestep:
            row = i
            break
    
    data = data[row+1:row+50, [1,2]]
    #print(data)
    
    #plt.plot(data[:,0], data[:,1])
    return data[:,0], data[:,1]


path = 'C:\LAMMPS 64-bit 24Mar2022\Examples\iron\\bulk.rdf'


with open(path) as f:
    lines = f.readlines()
    lines = lines[3:]
    for i in range(len(lines)):
        lines[i] = lines[i].split()
        if len(lines[i]) == 2:
            lines[i].append('0')
            lines[i].append('0')
    data = np.array(lines, dtype=float)
    
    x1,y1 = rdf(0,data)
    
    plt.ion()
    fig = plt.figure()
    ax = fig.add_subplot(111)
    line1, = ax.plot(x1, y1, 'b-')
    time.sleep(5)
    for t in range(1,30):
        time.sleep(1)
        x, y = rdf(t*100, data)
        line1.set_ydata(y)
        plt.draw()



# plt.rcParams["figure.figsize"] = [7.00, 3.50]
# plt.rcParams["figure.autolayout"] = True
# plt.subplot(211)
# data = np.array(np.random.rand(100))
# y, binEdges = np.histogram(data, bins=100)
# plt.hist(data, bins=100, edgecolor='black')
# plt.subplot(212)
# bincenters = 0.5 * (binEdges[1:] + binEdges[:-1])
# plt.plot(bincenters, y, '-', c='black')
# plt.show()