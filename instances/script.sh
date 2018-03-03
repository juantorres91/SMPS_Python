#!/bin/sh
#PBS -l nodes=1:ppn=12
#PBS -l walltime=03:00:00
#PBS -l mem=64gb
#PBS -N sslprf5_25_100_1_cp_ph-1
#PBS -V 


cd    /home/juantorres/splib/siplib/SSLPRF5
pysp

mpirun -np 1 pyomo_ns -n localhost :\
       -np 1 dispatch_srvr  :\
       -np 12 phsolverserver localhost :\
       -np 1 runph -m test.py --default-rho=1\
       --scenario-solver-options="threads=1"\
       --solver-manager=phpyro --phpyro-required-workers=12 \
       --rho-cfgfile=rhosetter2.py\
       --max-iterations=300\
       --enable-ww-extensions\
       --enable-termdiff-convergence\
       --termdiff-threshold=0.001 \
       --pyro-host=localhost \
       --handshake-with-phpyro\
       --shutdown-pyro\
       --traceback\
