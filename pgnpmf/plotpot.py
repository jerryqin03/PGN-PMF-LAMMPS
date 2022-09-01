import matplotlib.pyplot as plt

files = ["N20.txt", "N100.txt", "mixed_potential.txt"]



for g in files:
    distance = []
    pot = []

    with open(g) as f:
        lines = f.readlines()[4:-1]
        for line in lines:
            distance.append(float(line.split()[1]))
            pot.append(float(line.split()[3]))

        plt.plot(distance, pot)
    

plt.xlabel("Interatomic distance (A)")
plt.ylabel("Force ()")
plt.legend(("N20", "N100", "mixed"))
plt.ylim(top=100, bottom=-200)
plt.savefig("Force2.png")