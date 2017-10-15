#!/usr/bin/env python
from __future__ import division, print_function, unicode_literals, absolute_import

import sys
import os

import numpy as np
import abipy.abilab as abilab
import abipy.flowtk as flowtk
import abipy.data as abidata


def gs_input(ecut, pawecutdg, acell_ang=3.567):
    # tpaw1_2.in
    # Input for PAW1 tutorial
    # Diamond at experimental volume
    structure = abilab.Structure.from_abivars(
        natom=2,
        ntypat=1,
        typat=2 * [1],
        znucl=6,
        acell=3*[acell_ang * abilab.units.ang_to_bohr],
        rprim=[0.0,  0.5,  0.5,
               0.5,  0.0,  0.5,
               0.5,  0.5,  0.0],
        xred=[0.0, 0.0, 0.0,
              1/4, 1/4, 1/4],
    )
    inp = abilab.AbinitInput(structure=structure, pseudos=abidata.pseudos("6c.lda.atompaw"))

    # Optimization of the lattice parameters
    inp.set_vars(
        ecut=ecut,
        pawecutdg=pawecutdg,
        ecutsm=0.5,
        nband=6,
        tolvrs=1e-10,
        nstep=20,
    )

    inp.set_autokmesh(nksmall=6) # ngkpt=[6, 6, 6], shiftk=[0.5, 0.5, 0.5])

    return inp


def build_ecut_conv_flow(options):
    inputs = [gs_input(ecut=ecut, pawecutdg=50) for ecut in np.linspace(start=8, stop=24, num=9)]
    return flowtk.Flow.from_inputs("flow_ecut_conv", inputs)

    #flow.make_scheduler().start()
    #with abilab.abirobot(flow, "GSR") as robot:
    #    data = robot.get_dataframe()
    #    print(data)
    #    data.plot(x="ecut", y="energy", title="Energy vs ecut")


def build_pawecutdg_conv_flow(options):
    inputs = [gs_input(ecut=12, pawecutdg=pawecutdg)
              for pawecutdg in np.linspace(start=12, stop=39, num=10)]

    return flowtk.Flow.from_inputs("flow_pawecutdg_conv", inputs)

    #flow.make_scheduler().start()
    #with abilab.abirobot(flow, "GSR") as robot:
    #    data = robot.get_dataframe()
    #    print(data)
    #    data.plot(x="pawecutdg", y="energy", title="Energy vs pawecutdg")


def build_ecut_pawecutdg_flow(options):
    import itertools
    ecut_list = np.linspace(start=8, stop=24, num=9)
    pawecutdg_list = [24, 30]
    inputs = [gs_input(ecut, pawecutdg)
              for pawecutdg, ecut in itertools.product(pawecutdg_list, ecut_list)]

    return flowtk.Flow.from_inputs("flow_pawecutdg_ecut", inputs)

    #flow.make_scheduler().start()
    #with abilab.abirobot(flow, "GSR") as robot:
    #    data = robot.get_dataframe()
    #    print(data)
    #    robot.pairplot(x_vars="ecut", y_vars="energy", hue="pawecutdg")


def build_eos_flow(options):
    inputs = [gs_input(ecut=12, pawecutdg=24, acell_ang=acell_ang)
              for acell_ang in np.linspace(start=3.52, stop=3.55, num=7)]
    return flowtk.Flow.from_inputs("flow_eos", inputs)

    #flow.build()
    #flow.make_scheduler().start()
    #with abilab.abirobot(flow, "GSR") as robot:
    #    #fit = robot.eos_fit()
    #    fits, table = robot.eos_fit("all")
    #    print(table)

    #print(fit)
    #fit.plot()


@abilab.flow_main
def main(options):
    flow = build_ecut_conv_flow(options)
    #flow = build_pawecutdg_conv_flow(options)
    #flow = build_eos_flow(options)
    #flow = flow_ecut_pawecutdg(options)
    flow.build_and_pickle_dump()
    return flow


if __name__ == "__main__":
    sys.exit(main())
