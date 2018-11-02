#!/bin/bash
#PBS -k o
#PBS -l nodes=1:ppn=1,walltime=5:00:00

[ $PBS_O_WORKDIR ] && cd $PBS_O_WORKDIR

module load matlab/2017a

cat > build.m <<END
addpath(genpath('/N/u/brlife/git/vistasoft'));
addpath(genpath('/N/u/brlife/git/jsonlab'));
addpath(genpath('/N/u/brlife/git/o3d-code'));
addpath(genpath('/N/u/brlife/git/encode'));
addpath(genpath('/N/u/brlife/git/mba'))
addpath(genpath('/N/u/brlife/git/wma'))
mcc -m -R -nodisplay -d compiled afqConverter
mcc -m -R -nodisplay -d compiled write_fg_to_trk_shift
exit
END
matlab -nodisplay -nosplash -r build && rm build.m
