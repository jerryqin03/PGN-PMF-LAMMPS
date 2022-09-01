#!/bin/bash
#SBATCH --account=p31680 ## Required: your allocation/account name, i.e. eXXXX, pXXXX or bXXXX
#SBATCH --partition=short ## Required: (buyin, short, normal, long, gengpu, genhimem, etc)
#SBATCH --time=03:00:00
#SBATCH --output=equlibrate.log
#SBATCH --nodes=4

module load mpi/openmpi-4.1.1-gcc.10.2.0 gcc/9.2.0 hdf5/1.8.10

num1=400
num2=600

# run equilibration
#mkdir ./pgnpmf/$num1$num2/equilibration
#mkdir ./pgnpmf/$num1$num2/equilibration/trajectory

#declare -a ps

#lmp -in ./pgnpmf/equpmf.in -var read_res ./pgnpmf/$num1$num2/genpmf.res -var steps_equ 5000 -var usic 1 -var trial 1 -var temp 300 -var ts 0.5 -var write_res ./pgnpmf/$num1$num2/equpmf1.res -var folder $num1$num2 -l ./pgnpmf/$num1$num2/logequ1.lammps

for iter in {1..70}
do 
next=$(($iter + 1))
lmp -in ./pgnpmf/equpmf.in -var read_res ./pgnpmf/$num1$num2/equpmf$iter.res -var steps_equ 5000 -var usic 1 -var trial 1 -var temp 300 -var ts 0.5 -var write_res ./pgnpmf/$num1$num2/equpmf$next.res -var folder $num1$num2 -l ./pgnpmf/$num1$num2/logequ$next.lammps
#ps[$(($iter - 1))]=$(python3 ./pgnpmf/equilibrate.py $num1$num2 $next)
done