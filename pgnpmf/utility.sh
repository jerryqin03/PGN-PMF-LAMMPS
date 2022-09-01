#!/bin/bash
#SBATCH --account=p31680 ## Required: your allocation/account name, i.e. eXXXX, pXXXX or bXXXX
#SBATCH --partition=short ## Required: (buyin, short, normal, long, gengpu, genhimem, etc)
#SBATCH --time=00:10:00
#SBATCH --output=utility.log
#SBATCH --nodes=1
#SBATCH --ntasks=4

#cd "trial 2"
n1=3
n2=7

# module load mpi/openmpi-4.1.1-gcc.10.2.0 gcc/9.2.0 hdf5/1.8.10
# mpirun -np 4 /home/jjq4271/lammps2022Apr/build_pgn/lmp -in ./pgnpmf/genpmf.in -var input_data ./pgnpmf/t$n1$n2/dat$n1$n2.dat -var steps_gen 10000 -var usic 1 -var trial 1 -var Temp 300 -var Vseed 57138 -var ts 1 -var write_restart ./pgnpmf/t$n1$n2/genpmftest.res -var folder t$n1$n2 -l ./pgnpmf/t$n1$n2/gentest.log

num1=100
num2=0

cd trial4

for iter in {0..10}
do
cd $num1$num2
mkdir ./tensile
mkdir ./tensile/trajectory
mkdir ./tensile/restart
cd ..
num1=$(($num1 - 10))
num2=$(($num2 + 10))
done

# num1=1000
# num2=0

# for iter in {0..10}
# do
# if [ $num1 -eq 300 ]
# then
#     echo "number is 300"
# elif [ $num1 -eq 0 ] || [ $num1 -eq 100 ]
# then
#     echo "special number $num1"
# else
#     echo "regular number"
# fi
# num1=$(($num1 - 100))
# num2=$(($num2 + 100))
# done