#!/bin/bash
cd /Users/gmatteo/git_repos/abitutorials/abitutorials/sigeph/flow_diamond/w1/outdata
# OpenMp Environment
export OMP_NUM_THREADS=1
# Commands before execution
ulimit -n 2048
source ~/env.sh
export PATH=$HOME/git_repos/abinit/_build/src/98_main:$PATH

mpirun  -n 1 mrgdv < /Users/gmatteo/git_repos/abitutorials/abitutorials/sigeph/flow_diamond/w1/outdata/mrgdvdb.stdin > /Users/gmatteo/git_repos/abitutorials/abitutorials/sigeph/flow_diamond/w1/outdata/mrgdvdb.stdout 2> /Users/gmatteo/git_repos/abitutorials/abitutorials/sigeph/flow_diamond/w1/outdata/mrgdvdb.stderr
