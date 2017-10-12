#!/bin/bash
cd /Users/gmatteo/git_repos/abitutorials/abitutorials/dfpt/flow_alas_ecut_conv/w5/outdata
# OpenMp Environment
export OMP_NUM_THREADS=1
# Commands before execution
source ~/env.sh

mpirun -n 1 mrgddb --nostrict < /Users/gmatteo/git_repos/abitutorials/abitutorials/dfpt/flow_alas_ecut_conv/w5/outdata/mrgddb.stdin > /Users/gmatteo/git_repos/abitutorials/abitutorials/dfpt/flow_alas_ecut_conv/w5/outdata/mrgddb.stdout 2> /Users/gmatteo/git_repos/abitutorials/abitutorials/dfpt/flow_alas_ecut_conv/w5/outdata/mrgddb.stderr
