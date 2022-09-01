#!/bin/bash
#SBATCH --account=p31680 ## Required: your allocation/account name, i.e. eXXXX, pXXXX or bXXXX
#SBATCH --partition=short ## Required: (buyin, short, normal, long, gengpu, genhimem, etc)
#SBATCH --time=04:00:00
#SBATCH --output=lammps.log
#SBATCH --nodes=1
#SBATCH --ntasks=4

module load mpi/openmpi-4.1.1-gcc.10.2.0 gcc/9.2.0 hdf5/1.8.10 fftw/3.3.8-openmpi-4.0.5-gcc-10.2.0
cd pgnpmf

num1=100
num2=0
trial=$1

for iter in {0..10}
do
if [ $num1 -eq 0 ]
then
    mpirun -np 4 lmp -in tenpmf.in -var read_res ./trial$trial/$num1$num2/equpmf111.res -var Temp 300 -var ts_save 100 -var usic 1 -var trial $trial -var strain_rate 5e-6 -var N20 $num1 -var N100 $num2 -var ts 0.1 -var steps_tensile 6000000 -l ./tensile/deform$num1$num2.$trial.lammps
elif [ $num1 -eq 10 ]
then
    mpirun -np 4 lmp -in tenpmf.in -var read_res ./trial$trial/$num1$num2/equpmf101.res -var Temp 300 -var ts_save 100 -var usic 1 -var trial $trial -var strain_rate 5e-6 -var N20 $num1 -var N100 $num2 -var ts 0.1 -var steps_tensile 6000000 -l ./tensile/deform$num1$num2.$trial.lammps
# elif [ $num1 -eq 200 ]
# then
#     mpirun -np 4 lmp -in tenpmf.in -var read_res ./$num1$num2/equpmf81.res -var Temp 300 -var ts_save 100 -var usic 2 -var trial $trial -var strain_rate 5e-6 -var N20 $num1 -var N100 $num2 -var ts 0.1 -var steps_tensile 6000000 -l ./tensile/deform$num1$num2.$trial.lammps
else
    mpirun -np 4 lmp -in tenpmf.in -var read_res ./trial$trial/$num1$num2/equpmf71.res -var Temp 300 -var ts_save 100 -var usic 1 -var trial $trial -var strain_rate 5e-6 -var N20 $num1 -var N100 $num2 -var ts 0.1 -var steps_tensile 6000000 -l ./tensile/deform$num1$num2.$trial.lammps
fi
num1=$(($num1 - 10))
num2=$(($num2 + 10))
done