#!/usr/bin/env python
import sys
import abipy.abilab as abilab
import abipy.flowtk as flowtk
import abipy.data as abidata


def build_ngkpt_flow(options):
    """
    Crystalline silicon: computation of the total energy
    Convergence with respect to the number of k points. Similar to tbase3_3.in

    Args:
        options: Command line options.

    Return:
        Abinit Flow object.
    """
    # Definition of the different grids
    ngkpt_list = [(2, 2, 2), (4, 4, 4), (6, 6, 6), (8, 8, 8)]

    # These shifts will be the same for all grids
    shiftk = [float(s) for s in "0.5 0.5 0.5 0.5 0.0 0.0 0.0 0.5 0.0 0.0 0.0 0.5".split()]

    # Build MultiDataset object (container of `ndtset` inputs).
    # Structure is initialized from CIF file.
    multi = abilab.MultiDataset(structure=abidata.cif_file("si.cif"),
                                pseudos=abidata.pseudos("14si.pspnc"), ndtset=len(ngkpt_list))

    # These variables are the same in each input.
    multi.set_vars(ecut=8, toldfe=1e-6, diemac=12.0, iomode=3)

    # Each input has its own value of `ngkpt`. shiftk is constant.
    for i, ngkpt in enumerate(ngkpt_list):
        multi[i].set_kmesh(ngkpt=ngkpt, shiftk=shiftk)

    workdir = options.workdir if (options and options.workdir) else "flow_base3_ngkpt"

    # Split the inputs by calling multi.datasets() and pass the list of inputs to Flow.from_inputs.
    return flowtk.Flow.from_inputs(workdir, inputs=multi.split_datasets())


def build_relax_flow(options):
    """
    Crystalline silicon: computation of the optimal lattice parameter.
    Convergence with respect to the number of k points. Similar to tbase3_4.in
    """
    # Structural relaxation for different k-point samplings.
    ngkpt_list = [(2, 2, 2), (4, 4, 4)]

    shiftk = [float(s) for s in "0.5 0.5 0.5 0.5 0.0 0.0 0.0 0.5 0.0 0.0 0.0 0.5".split()]

    multi = abilab.MultiDataset(structure=abidata.cif_file("si.cif"),
                                pseudos=abidata.pseudos("14si.pspnc"), ndtset=len(ngkpt_list))

    # Global variables
    multi.set_vars(
        ecut=8,
        tolvrs=1e-9,
        optcell=1,
        ionmov=3,
        ntime=10,
        dilatmx=1.05,
        ecutsm=0.5,
        diemac=12,
        iomode=3,
    )

    for i, ngkpt in enumerate(ngkpt_list):
        multi[i].set_kmesh(ngkpt=ngkpt, shiftk=shiftk)

    workdir = options.workdir if (options and options.workdir) else "flow_base3_relax"

    return flowtk.Flow.from_inputs(workdir, inputs=multi.split_datasets(), task_class=flowtk.RelaxTask)


def build_ebands_flow(options):
    """
    Band structure calculation.
    First, a SCF density computation, then a non-SCF band structure calculation.
    Similar to tbase3_5.in
    """
    multi = abilab.MultiDataset(structure=abidata.cif_file("si.cif"),
                                pseudos=abidata.pseudos("14si.pspnc"), ndtset=2)
    # Global variables
    shiftk = [float(s) for s in "0.5 0.5 0.5 0.5 0.0 0.0 0.0 0.5 0.0 0.0 0.0 0.5".split()]
    multi.set_vars(ecut=8, diemac=12, iomode=3)

    # Dataset 1
    multi[0].set_vars(tolvrs=1e-9)
    multi[0].set_kmesh(ngkpt=[4, 4, 4], shiftk=shiftk)

    # Dataset 2
    multi[1].set_vars(tolwfr=1e-15)
    multi[1].set_kpath(ndivsm=5)

    scf_input, nscf_input = multi.split_datasets()

    workdir = options.workdir if (options and options.workdir) else "flow_base3_ebands"

    return flowtk.bandstructure_flow(workdir, scf_input=scf_input, nscf_input=nscf_input)


@flowtk.flow_main
def main(options):
    """
    This is our main function that will be invoked by the script.
    flow_main is a decorator implementing the command line interface.
    Command line args are stored in `options`.
    """
    #flow = build_ngkpt_flow(options)
    flow = build_relax_flow(options)
    #flow = build_ebands_flow(options)
    flow.build_and_pickle_dump()
    return flow


if __name__ == "__main__":
    sys.exit(main())
