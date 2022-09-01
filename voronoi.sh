#!/bin/bash
#SBATCH --account=p31680 ## Required: your allocation/account name, i.e. eXXXX, pXXXX or bXXXX
#SBATCH --partition=short ## Required: (buyin, short, normal, long, gengpu, genhimem, etc)
#SBATCH --time=04:00:00
#SBATCH --output=voronoi.log
#SBATCH --nodes=1 ## how many computers/nodes do you need (no default)
#SBATCH --ntasks=4

module load mpi/openmpi-4.1.1-gcc.10.2.0 gcc/9.2.0 hdf5/1.8.10 fftw/3.3.8-openmpi-4.0.5-gcc-10.2.0

num1=0
num2=10

for iter in {0..10}
do
if [ num1 -eq 0 ]
then
    mpirun -np 4 /home/jjq4271/lammps2022Apr/build_pgn_voronoi/lmp -in ./pgnpmf/voronoi.in -var read_res ./pgnpmf/trial2/$num1$num2/equpmf156.res -var steps_equ 5000 -var folder trial2/$num1$num2 -var usic 1 -var trial 1 -var temp 300 -var ts 0.5 -l ./pgnpmf/trial2/$num1$num2/logvoronoi.lammps
else
    mpirun -np 4 /home/jjq4271/lammps2022Apr/build_pgn_voronoi/lmp -in ./pgnpmf/voronoi.in -var read_res ./pgnpmf/trial2/$num1$num2/equpmf71.res -var steps_equ 5000 -var folder trial2/$num1$num2 -var usic 1 -var trial 1 -var temp 300 -var ts 0.5 -l ./pgnpmf/trial2/$num1$num2/logvoronoi.lammps
fi

num1=$(($num1 + 1))
num2=$(($num2 - 1))

done