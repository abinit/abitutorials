#!/bin/bash
cd /Users/gmatteo/git_repos/abitutorials/abitutorials/eph_al/flow_eph_al/w1/outdata
# OpenMp Environment
export OMP_NUM_THREADS=1
# Commands before execution
source ~/env.sh

mpirun  -n 1 mrgddb --nostrict < /Users/gmatteo/git_repos/abitutorials/abitutorials/eph_al/flow_eph_al/w1/outdata/mrgddb.stdin > /Users/gmatteo/git_repos/abitutorials/abitutorials/eph_al/flow_eph_al/w1/outdata/mrgddb.stdout 2> /Users/gmatteo/git_repos/abitutorials/abitutorials/eph_al/flow_eph_al/w1/outdata/mrgddb.stderr
