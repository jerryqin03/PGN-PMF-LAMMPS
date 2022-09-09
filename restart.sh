#!/bin/bash
#SBATCH --account=p31680 ## Required: your allocation/account name, i.e. eXXXX, pXXXX or bXXXX
#SBATCH --partition=short ## Required: (buyin, short, normal, long, gengpu, genhimem, etc)
#SBATCH --time=04:00:00
#SBATCH --output=pgnrestart.log
#SBATCH --nodes=1 ## how many computers/nodes do you need (no default)
#SBATCH --ntasks=4

module load mpi/openmpi-4.1.1-gcc.10.2.0 gcc/9.2.0 hdf5/1.8.10 fftw/3.3.8-openmpi-4.0.5-gcc-10.2.0

num1=$1
num2=$2
low=$3
high=$4
trial=$5
high=370000


#mpirun -np 4 lmp -in ./pgnpmf/equpmf.in -var read_res ./pgnpmf/trial$trial/$num1$num2/genpmf.res -var steps_equ 50000 -var usic 1 -var trial $trial -var temp 300 -var ts 0.05 -var write_res ./pgnpmf/trial$trial/$num1$num2/equpmf1.res -var folder $num1$num2 -l ./pgnpmf/trial$trial/$num1$num2/logequ1.lammps
for (( iter=$low; iter < $(($high + 1)); iter++ ))
do 
next=$(($iter + 1))
mpirun -np 4 lmp -in ./pgnpmf/equpmf.in -var read_res ./pgnpmf/trial$trial/$num1$num2/equpmf$iter.res -var steps_equ 50000 -var usic 1 -var trial $trial -var temp 300 -var high $high -var ts 0.25 -var write_res ./pgnpmf/trial$trial/$num1$num2/equpmf$next.res -var folder $num1$num2 -l ./pgnpmf/trial$trial/$num1$num2/logequ$next.lammps
#ps[$(($iter - 1))]=$(python3 ./pgnpmf/equilibrate.py $num1$num2 $next)
done

# cd ./pgnpmf/$n1$n2

# greatest=0

# for (( iter=$low; iter < $(($high + 1)); iter++ ))
# do
# if [ ! -e equpmf$i.res ]
# then
#     greatest=$(($i - 1))
#     sbatch restart.sh $n1 $n2 $greatest 71
#     break
# fi