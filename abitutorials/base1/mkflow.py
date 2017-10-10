#!/usr/bin/env python
from __future__ import division, print_function, unicode_literals, absolute_import

import sys
import os
import numpy as np
import abipy.abilab as abilab
import abipy.flowtk as flowtk
import abipy.data as abidata


def gs_input(x=0.7, ecut=10, acell=(10, 10, 10)):
    """H2 molecule in a big box"""
    structure = abilab.Structure.from_abivars(
        ntypat=1,
        znucl=1,
        natom=2,
        typat=(1, 1),
        xcart=[-x, 0.0, 0.0,
               +x, 0.0, 0.0],
        acell=acell,
        rprim=[1, 0, 0, 0, 1, 0, 0, 0, 1]
    )

    inp = abilab.AbinitInput(structure=structure, pseudos=abidata.pseudos("01h.pspgth"))

    inp.set_vars(
        ecut=ecut,
        nband=1,
        diemac=2.0,
        toldfe=1e-6,
        prtwf=-1,
        iomode=3
    )

    inp.set_kmesh(ngkpt=(1, 1, 1), shiftk=(0, 0, 0))
    return inp


def build_flow(options):
    """
    H2 molecule in a big box:
    Generate a flow to compute the total energy and forces as a function of the interatomic distance
    """
    workdir = options.workdir
    if not options.workdir:
        workdir = os.path.basename(__file__).replace(".py", "").replace("run_", "flow_")

    inputs = [gs_input(x=x) for x in np.linspace(0.5, 1.025, 21)]
    return flowtk.Flow.from_inputs("flow_h", inputs, remove=options.remove, pickle_protocol=0)


@abilab.flow_main
def main(options):
    flow = build_flow(options)
    flow.build_and_pickle_dump()
    return flow


if __name__ == "__main__":
    sys.exit(main())
