#!/usr/bin/env python
from __future__ import division, print_function, unicode_literals, absolute_import

import sys
import os
import abipy.abilab as abilab
import abipy.flowtk as flowtk
import abipy.data as abidata


def relax_input(tsmear, nksmall):
    """
    Crystalline aluminum: optimization of the lattice parameter
    at fixed number of k points and broadening.
    """
    inp = abilab.AbinitInput(structure=abidata.ucells.structure_from_ucell("Al"),
                             pseudos=abidata.pseudos("13al.981214.fhi"))

    # nshiftk and shift are automatically selected from the lattice.
    #Definition of the k-point grid
    #ngkpt 2 2 2       # This is a 2x2x2 FCC grid, based on the primitive vectors
    #nshiftk 4         # of the reciprocal space. For a FCC real space lattice,
    #                  # like the present one, it actually corresponds to the
    #                  # so-called 4x4x4 Monkhorst-Pack grid, if the following shifts
    #                  # are used :
    #shiftk 0.5 0.5 0.5
    #       0.5 0.0 0.0
    #       0.0 0.5 0.0
    #       0.0 0.0 0.5
    inp.set_autokmesh(nksmall=nksmall)

    # Optimization of the lattice parameters
    inp.set_vars(
        ecut=6,
        occopt=4,
        tsmear=tsmear,
        toldfe=1e-6,
        nstep=10,
        optcell=1,
        ionmov=3,
        ntime=10,
        dilatmx=1.05,
        ecutsm=0.5,
        ixc=1,
    )

    return inp


def build_relax_flow(options):
    flow = flowtk.Flow.from_inputs("flow_al_relax", inputs=relax_input(tsmear=0.05, nksmall=2),
                                   task_class=flowtk.RelaxTask)

    return flow


def build_tsmear_nkpts_convflow(options, tsmear_list=(0.01, 0.02, 0.03, 0.04),
                                nksmall_list=(2, 4, 6)):
    # Cartesian product of input iterables. Equivalent to nested for-loops.
    from itertools import product
    inputs = [relax_input(tsmear, nksmall) for tsmear, nksmall in product(tsmear_list, nksmall_list)]

    return flowtk.Flow.from_inputs(workdir="flow_al_relax_tsmear_nkpt", inputs=inputs,
                                   task_class=flowtk.RelaxTask)

    #flow.make_scheduler().start()
    #with abilab.abirobot(flow, "GSR") as robot:
    #    data = robot.get_dataframe()
    #    print(data)
    #    robot.pairplot(x_vars="nkpts", y_vars=["energy", "a", "volume"], hue="tsmear")

    #grid = sns.FacetGrid(data, col="tsmear")
    #grid.map(sns.pointplot, "nkpts", "a")
    #sns.pairplot(data, x_vars="nkpts", y_vars=["energy", "a", "volume"], hue="tsmear")
    #grid.map(plt.scatter, s=50)


@abilab.flow_main
def main(options):
    #flow = build_relax_flow(options)
    flow = build_tsmear_nkpts_convflow(options)
    flow.build_and_pickle_dump()
    return flow


if __name__ == "__main__":
    sys.exit(main())
