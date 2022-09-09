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
num1=$(($n1 * 10))
#echo "Number of N=100 PGN in system:"
n2=$2
num2=$(($n2 * 10))

trial=$3
rand=$RANDOM

high=3700000

mkdir -p ./pgnpmf/trial$trial
mkdir -p ./pgnpmf/trial$trial/$n1$n2
mkdir -p ./pgnpmf/packmol/trial$trial
mkdir -p ./pgnpmf/packmol/trial$trial/$n1$n2
touch ./pgnpmf/packmol/trial$trial/$n1$n2/$n1$n2.inp

if [ $n1 -eq 0 ]
then
    echo "tolerance 55
    output $n1$n2.pdb

    filetype pdb

    seed 13579

    structure Pg.pdb
        number $num2
        inside cube 0. 0. 0. 4000
        radius 55
    end structure" >> ./pgnpmf/packmol/trial$trial/$n1$n2/$n1$n2.inp

elif [ $n2 -eq 0 ]
then
    echo "tolerance 55
    output $n1$n2.pdb

    filetype pdb

    seed 13579

    structure Ap.pdb
        number $num1
        inside cube 0. 0. 0. 4000
        radius 55
    end structure" >> ./pgnpmf/packmol/trial$trial/$n1$n2/$n1$n2.inp

else

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

    seed $rand

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
    end structure" >> ./pgnpmf/packmol/trial$trial/$n1$n2/$n1$n2.inp
fi

packmol < ./pgnpmf/packmol/trial$trial/$n1$n2/$n1$n2.inp

# conversion into lammps input script

mv $n1$n2.pdb ./pgnpmf/packmol/trial$trial/$n1$n2/$n1$n2.pdb
python3 ./pgnpmf/packmol/fixpdb.py "./trial$trial/$n1$n2/$n1$n2.pdb" "./trial$trial/$n1$n2/fix$n1$n2.pdb"
python3 ./pgnpmf/packmol/pdb2lmp.py "./trial$trial/$n1$n2/fix$n1$n2.pdb" "./../trial$trial/$n1$n2/dat$n1$n2.dat"


# run generation
mkdir ./pgnpmf/trial$trial/$n1$n2/generation
mkdir ./pgnpmf/trial$trial/$n1$n2/generation/trajectory
mpirun -np 4 lmp -in ./pgnpmf/genpmf.in -var input_data ./pgnpmf/trial$trial/$n1$n2/dat$n1$n2.dat -var steps_gen 5000 -var usic 1 -var trial $trial -var Temp 300 -var Vseed $rand -var ts 0.5 -var write_restart ./pgnpmf/trial$trial/$n1$n2/genpmf.res -var folder trial$trial/$n1$n2 -l ./pgnpmf/trial$trial/$n1$n2/gen.log


# run equilibration
mkdir ./pgnpmf/trial$trial/$n1$n2/equilibration
mkdir ./pgnpmf/trial$trial/$n1$n2/equilibration/trajectory

#declare -a ps

mpirun -np 4 lmp -in ./pgnpmf/equpmf.in -var read_res ./pgnpmf/trial$trial/$n1$n2/genpmf.res -var steps_equ 50000 -var usic 1 -var trial $trial -var temp 300 -var high $high -var ts 0.25 -var write_res ./pgnpmf/trial$trial/$n1$n2/equpmf1.res -var folder trial$trial/$n1$n2 -l ./pgnpmf/trial$trial/$n1$n2/logequ1.lammps

for iter in {1..69}
do 
next=$(($iter + 1))
mpirun -np 4 lmp -in ./pgnpmf/equpmf.in -var read_res ./pgnpmf/trial$trial/$n1$n2/equpmf$iter.res -var steps_equ 50000 -var usic 1 -var trial $trial -var temp 300 -var high $high -var ts 0.25 -var write_res ./pgnpmf/trial$trial/$n1$n2/equpmf$next.res -var folder trial$trial/$n1$n2 -l ./pgnpmf/trial$trial/$n1$n2/logequ$next.lammps
#ps[$(($iter - 1))]=$(python3 ./pgnpmf/equilibrate.py $num1$num2 $next)
done

mpirun -np 4 lmp -in ./pgnpmf/equpmf_save.in -var read_res ./pgnpmf/trial$trial/$n1$n2/equpmf70.res -var steps_equ 50000 -var usic 1 -var trial $trial -var temp 300 -var high $high -var ts 0.25 -var write_res ./pgnpmf/trial$trial/$n1$n2/equpmf71.res -var folder trial$trial/$n1$n2 -l ./pgnpmf/trial$trial/$n1$n2/logequ71.lammps

# cd ./pgnpmf/trial$trial/$n1$n2

# greatest=0

# for i in {0..71}
# do
# if [ ! -e equpmf$i.res ]
# then
#     greatest=$(($i - 1))
#     sbatch restart.sh $n1 $n2 $greatest 71 $trial
#     break
# fi






