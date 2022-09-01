#!/bin/bash
#SBATCH --account=p31680 ## Required: your allocation/account name, i.e. eXXXX, pXXXX or bXXXX
#SBATCH --partition=short ## Required: (buyin, short, normal, long, gengpu, genhimem, etc)
#SBATCH --time=04:00:00
#SBATCH --output=pgn.log
#SBATCH --nodes=1
#SBATCH --ntasks=4


module load mpi/openmpi-4.1.1-gcc.10.2.0 gcc/9.2.0 hdf5/1.8.10 fftw/3.3.8-openmpi-4.0.5-gcc-10.2.0

# packmol generation
#echo "Packmol generation"
#echo "Number of N=20 PGN in system:"
n1=$1
num1=$(($n1 * 100))
#echo "Number of N=100 PGN in system:"
n2=$2
num2=$(($n2 * 100))

mkdir ./pgnpmf/$n1$n2
mkdir ./pgnpmf/packmol/$n1$n2
touch ./pgnpmf/packmol/$n1$n2/$n1$n2.inp

if [ $(($num1 % 200)) -eq 0 ]
then
    a1=$(($num1 / 8))
    b1=$(($num1 / 8))
    a2=$(($num2 / 8))
    b2=$(($num2 / 8))
else
    a1=$((($num1 * 10 / 8 + 5) / 10))
    b1=$((($num1 * 10 / 8 - 5) / 10))
    a2=$((($num2 * 10 / 8 + 5) / 10))
    b2=$((($num2 * 10 / 8 - 5) / 10))
fi

echo "tolerance 55
output $n1$n2.pdb

filetype pdb

seed 13579

structure Ap.pdb
    number $a1
    inside box 0. 0. 0. 2000 2000 2000
    radius 55
end structure

structure Ap.pdb
    number $b1
    inside box 2000 0. 0. 4000 2000 2000
    radius 55
end structure

structure Ap.pdb
    number $a1
    inside box 0. 2000 0. 2000 4000 2000
    radius 55
end structure

structure Ap.pdb
    number $b1
    inside box 0. 0. 2000 2000 2000 4000
    radius 55
end structure

structure Ap.pdb
    number $a1
    inside box 2000 2000 0. 4000 4000 2000
    radius 55
end structure

structure Ap.pdb
    number $b1
    inside box 2000 0. 2000 4000 2000 4000
    radius 55
end structure

structure Ap.pdb
    number $a1
    inside box 0. 2000 2000 2000 4000 4000
    radius 55
end structure

structure Ap.pdb
    number $b1
    inside box 2000 2000 2000 4000 4000 4000
    radius 55
end structure

structure Pg.pdb
    number $a2
    inside box 0. 0. 0. 2000 2000 2000
    radius 55
end structure

structure Pg.pdb
    number $b2
    inside box 2000 0. 0. 4000 2000 2000
    radius 55
end structure

structure Pg.pdb
    number $a2
    inside box 0. 2000 0. 2000 4000 2000
    radius 55
end structure

structure Pg.pdb
    number $b2
    inside box 0. 0. 2000 2000 2000 4000
    radius 55
end structure

structure Pg.pdb
    number $a2
    inside box 2000 2000 0. 4000 4000 2000
    radius 55
end structure

structure Pg.pdb
    number $b2
    inside box 2000 0. 2000 4000 2000 4000
    radius 55
end structure

structure Pg.pdb
    number $a2
    inside box 0. 2000 2000 2000 4000 4000
    radius 55
end structure

structure Pg.pdb
    number $b2
    inside box 2000 2000 2000 4000 4000 4000
    radius 55
end structure" >> ./pgnpmf/packmol/$n1$n2/$n1$n2.inp

packmol < ./pgnpmf/packmol/$n1$n2/$n1$n2.inp

# conversion into lammps input script

mv $n1$n2.pdb ./pgnpmf/packmol/$n1$n2/$n1$n2.pdb
python3 ./pgnpmf/packmol/fixpdb.py "./$n1$n2/$n1$n2.pdb" "./$n1$n2/fix$n1$n2.pdb"
python3 ./pgnpmf/packmol/pdb2lmp.py "./$n1$n2/fix$n1$n2.pdb" "./../$n1$n2/dat$n1$n2.dat"


# run generation
mkdir ./pgnpmf/$n1$n2/generation
mkdir ./pgnpmf/$n1$n2/generation/trajectory
mpirun -np 4 lmp -in ./pgnpmf/genpmf.in -var input_data ./pgnpmf/$n1$n2/dat$n1$n2.dat -var steps_gen 5000 -var usic 1 -var trial 1 -var Temp 300 -var Vseed 97531 -var ts 1 -var write_restart ./pgnpmf/$n1$n2/genpmf.res -var folder $n1$n2 -l ./pgnpmf/$n1$n2/gen.log


# run equilibration
mkdir ./pgnpmf/$n1$n2/equilibration
mkdir ./pgnpmf/$n1$n2/equilibration/trajectory

#declare -a ps

mpirun -np 4 lmp -in ./pgnpmf/equpmf.in -var read_res ./pgnpmf/$n1$n2/genpmf.res -var steps_equ 5000 -var usic 1 -var trial 1 -var temp 300 -var ts 0.25 -var write_res ./pgnpmf/$n1$n2/equpmf1.res -var folder $n1$n2 -l ./pgnpmf/$n1$n2/logequ1.lammps

for iter in {1..70}
do 
next=$(($iter + 1))
mpirun -np 4 lmp -in ./pgnpmf/equpmf.in -var read_res ./pgnpmf/$n1$n2/equpmf$iter.res -var steps_equ 5000 -var usic 1 -var trial 1 -var temp 300 -var ts 0.25 -var write_res ./pgnpmf/$n1$n2/equpmf$next.res -var folder $n1$n2 -l ./pgnpmf/$n1$n2/logequ$next.lammps
#ps[$(($iter - 1))]=$(python3 ./pgnpmf/equilibrate.py $num1$num2 $next)
done

cd ./pgnpmf/$n1$n2

greatest=0

for i in {0..71}
do
if [ ! -e equpmf$i.res ]
then
    greatest=$(($i - 1))
    sbatch restart.sh $n1 $n2 $greatest 71
    break
fi






