#!/bin/bash
#SBATCH --account=p31680 ## Required: your allocation/account name, i.e. eXXXX, pXXXX or bXXXX
#SBATCH --partition=short ## Required: (buyin, short, normal, long, gengpu, genhimem, etc)
#SBATCH --time=00:10:00
#SBATCH --output=lammps.log
#SBATCH --nodes=8

module load mpi/openmpi-4.1.1-gcc.10.2.0 gcc/9.2.0 hdf5/1.8.10
cd pgnpmf

mpirun -np 4 lmp -in tenpmf.in -var read_res ./700300/equpmf71.res -var Temp 300 -var ts_save 100 -var usic 1 -var trial 1 -var strain_rate 5e-6 -var N20 700 -var N100 300 -var ts 1 -var steps_tensile 250000 -l log1.lammps