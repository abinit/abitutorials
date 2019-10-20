#!/usr/bin/env python
"""DFPT lesson: phonon band structure of AlAs with Born effective charges."""
import sys

import abipy.abilab as abilab
import abipy.data as abidata
import abipy.flowtk as flowtk


def make_scf_input(ecut=2, ngkpt=(4, 4, 4)):
    """
    This function constructs an `AbinitInput` to perform a GS-SCF calculation in crystalline AlAs.

    Args:
        ecut: cutoff energy in Ha.
        ngkpt: 3 integers specifying the k-mesh for the electrons.

    Return:
        `AbinitInput` object
    """
    # Initialize the AlAs structure from an internal database. Use the pseudos shipped with AbiPy.
    gs_inp = abilab.AbinitInput(structure=abidata.structure_from_ucell("AlAs"),
                                pseudos=abidata.pseudos("13al.981214.fhi", "33as.pspnc"))

    # Set the value of the Abinit variables needed for GS runs.
    gs_inp.set_vars(
        nband=4,
        ecut=ecut,
        ngkpt=ngkpt,
        nshiftk=4,
        shiftk=[0.0, 0.0, 0.5,   # This gives the usual fcc Monkhorst-Pack grid
                0.0, 0.5, 0.0,
                0.5, 0.0, 0.0,
                0.5, 0.5, 0.5],
        ixc=1,
        nstep=25,
        diemac=9.0,
        tolvrs=1.0e-10,
        #iomode=3,
    )

    return gs_inp


def build_flow_alas_ecut_conv(options):
    """
    Build and return Flow for convergence study of phonon frequencies at Gamma as function of ecut.
    """
    scf_input = make_scf_input()
    return flowtk.phonon_conv_flow("flow_alas_ecut_conv", scf_input, qpoints=(0, 0, 0),
                                   params=["ecut", [4, 6, 8]])


def build_flow_alas_phonons(options):
    """
    Build and return a Flow to compute the dynamical matrix on a (2, 2, 2) qmesh
    as well as DDK and Born effective charges.
    The final DDB with all perturbations will be merged automatically and placed
    in the Flow `outdir` directory.
    """
    scf_input = make_scf_input(ecut=6, ngkpt=(4, 4, 4))
    return flowtk.PhononFlow.from_scf_input("flow_alas_phonons", scf_input,
                                            ph_ngqpt=(2, 2, 2), with_becs=True)


@flowtk.flow_main
def main(options):
    """
    This is our main function that will be invoked by the script.
    flow_main is a decorator implementing the command line interface.
    Command line args are stored in `options`.
    """
    #flow = build_flow_alas_ecut_conv(options)
    flow = build_flow_alas_phonons(options)
    return flow


if __name__ == "__main__":
    sys.exit(main())
