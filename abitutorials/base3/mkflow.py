#!/usr/bin/env python
from __future__ import division, print_function, unicode_literals, absolute_import

import sys
import os
import abipy.abilab as abilab
import abipy.flowtk as flowtk
import abipy.data as abidata


def build_ngkpt_flow(options):
    # Definition of the different grids
    ngkpt_list = [(2, 2, 2), (4, 4, 4), (6, 6, 6), (8, 8, 8)]
    # These shifts will be the same for all grids
    shiftk = [float(s) for s in "0.5 0.5 0.5 0.5 0.0 0.0 0.0 0.5 0.0 0.0 0.0 0.5".split()]

    multi = abilab.MultiDataset(structure=abidata.cif_file("si.cif"),
                                pseudos=abidata.pseudos("14si.pspnc"), ndtset=len(ngkpt_list))
    # Global variables
    multi.set_vars(ecut=8, toldfe=1e-6)

    for i, ngkpt in enumerate(ngkpt_list):
        multi[i].set_kmesh(ngkpt=ngkpt, shiftk=shiftk)

    return flowtk.Flow.from_inputs(workdir="flow_base3_ngkpt", inputs=multi.split_datasets())


def build_relax_flow(options):
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
    )

    for i, ngkpt in enumerate(ngkpt_list):
        multi[i].set_kmesh(ngkpt=ngkpt, shiftk=shiftk)

    return flowtk.Flow.from_inputs("flow_base3_relax", inputs=multi.split_datasets(),
                                   task_class=flowtk.RelaxTask)


def build_ebands_flow(options):
    """Band structure calculation."""
    multi = abilab.MultiDataset(structure=abidata.cif_file("si.cif"),
                                pseudos=abidata.pseudos("14si.pspnc"), ndtset=2)
    # Global variables
    shiftk = [float(s) for s in "0.5 0.5 0.5 0.5 0.0 0.0 0.0 0.5 0.0 0.0 0.0 0.5".split()]
    multi.set_vars(ecut=10)

    # Dataset 1
    multi[0].set_vars(tolvrs=1e-9)
    multi[0].set_kmesh(ngkpt=[4, 4, 4], shiftk=shiftk)

    # Dataset 2
    multi[1].set_vars(tolwfr=1e-15)
    multi[1].set_kpath(ndivsm=5)

    scf_input, nscf_input = multi.split_datasets()

    return flowtk.bandstructure_flow(workdir="flow_base3_ebands", scf_input=scf_input, nscf_input=nscf_input)


@abilab.flow_main
def main(options):
    #flow = build_ngkpt_flow(options)
    flow = build_relax_flow(options)
    #flow = build_ebands_flow(options)
    flow.build_and_pickle_dump()
    return flow


if __name__ == "__main__":
    sys.exit(main())
