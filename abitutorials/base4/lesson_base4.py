#!/usr/bin/env python
import sys
import abipy.abilab as abilab
import abipy.flowtk as flowtk
import abipy.data as abidata


def relax_input(tsmear, nksmall):
    """
    Crystalline aluminum: optimization of the lattice parameter
    at fixed number of k points and broadening. Similar to tbase4_1.in with minor
    """
    inp = abilab.AbinitInput(structure=abidata.ucells.structure_from_ucell("Al"),
                             pseudos=abidata.pseudos("13al.981214.fhi"))

    # Define k-point sampling.
    # nshiftk and shift are automatically selected from the lattice and the number of divisions
    # for the smallest direction. nksmall 2 e.g. will automatically select
    #   ngkpt 2 2 2
    #   nshiftk 4
    #   shiftk
    #       0.5 0.5 0.5
    #       0.5 0.0 0.0
    #       0.0 0.5 0.0
    #       0.0 0.0 0.5
    inp.set_autokmesh(nksmall=nksmall)

    inp.set_vars(
        ecut=6,
        occopt=4,
        tsmear=tsmear,
        toldfe=1e-6,
        nstep=10,
        optcell=1,    # Optimization of the lattice parameters
        ionmov=3,
        ntime=10,
        dilatmx=1.05,
        ecutsm=0.5,
        ixc=1,
    )

    return inp


def build_relax_flow(options):

    workdir = options.workdir if (options and options.workdir) else "flow_al_relax"

    return flowtk.Flow.from_inputs(workdir, inputs=relax_input(tsmear=0.05, nksmall=2),
                                   task_class=flowtk.RelaxTask)


def build_relax_tsmear_nkpts_convflow(options, tsmear_list=(0.01, 0.02, 0.03, 0.04), nksmall_list=(2, 4, 6)):
    # product computes the Cartesian product of input iterables.
    # It's equivalent to nested for-loops
    from itertools import product
    inputs = [relax_input(tsmear, nksmall) for tsmear, nksmall in product(tsmear_list, nksmall_list)]

    # Build flow form inputs.
    # Note the Flow.from_inputs is a simplified interface that, by default, builds tasks
    # for Ground-state calculation (GsTask).
    # Here we are performing a structural relaxation so we have to specify the task class explicitly.
    # AbiPy will use this piece of information to handle the restart of the RelaxTask that differs
    # from the one provided by GsTask.

    workdir = options.workdir if (options and options.workdir) else "flow_al_relax_tsmear_nkpt"

    return flowtk.Flow.from_inputs(workdir, inputs=inputs, task_class=flowtk.RelaxTask)


@flowtk.flow_main
def main(options):
    #flow = build_relax_flow(options)
    flow = build_relax_tsmear_nkpts_convflow(options)
    return flow


if __name__ == "__main__":
    sys.exit(main())
