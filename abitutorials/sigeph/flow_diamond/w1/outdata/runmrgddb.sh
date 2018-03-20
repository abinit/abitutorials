#!/bin/bash
cd /Users/gmatteo/git_repos/abitutorials/abitutorials/sigeph/flow_diamond/w1/outdata
# OpenMp Environment
export OMP_NUM_THREADS=1
# Commands before execution
source ~/env.sh

mpirun  -n 1 mrgddb --nostrict < /Users/gmatteo/git_repos/abitutorials/abitutorials/sigeph/flow_diamond/w1/outdata/mrgddb.stdin > /Users/gmatteo/git_repos/abitutorials/abitutorials/sigeph/flow_diamond/w1/outdata/mrgddb.stdout 2> /Users/gmatteo/git_repos/abitutorials/abitutorials/sigeph/flow_diamond/w1/outdata/mrgddb.stderr
