#!/usr/bin/env python
import sys
import numpy as np
import abipy.abilab as abilab
import abipy.flowtk as flowtk
import abipy.data as abidata


def gs_input(x=0.7, ecut=10, acell=(10, 10, 10)):
    """
    This function builds an AbinitInput object to compute the total energy
    of the H2 molecule in a big box.

    Args:
        x: Position of the first Hydrogen along the x-axis in Cartesian coordinates.
           The second Hydrogen is located at [-x, 0, 0]
        ecut: Cutoff energy in Ha.
        acell: Lengths of the primitive vectors (in Bohr)

    Returns:
        AbinitInput object.
    """
    # Build structure from dictionary with input variables.
    structure = abilab.Structure.from_abivars(
        ntypat=1,                           # There is only one type of atom.
        znucl=1,                            # Atomic numbers of the type(s) of atom.
        natom=2,                            # There are two atoms.
        typat=(1, 1),                       # They both are of type 1, that is, Hydrogen.
        xcart=[-x, 0.0, 0.0,                # Cartesian coordinates of atom 1, in Bohr.
               +x, 0.0, 0.0],               # second atom.
        acell=acell,                        # Lengths of the primitive vectors (in Bohr).
        rprim=[1, 0, 0, 0, 1, 0, 0, 0, 1]   # Orthogonal primitive vectors (default).
    )

    # Build AbinitInput from structure and pseudo(s) taken from AbiPy package.
    inp = abilab.AbinitInput(structure=structure, pseudos=abidata.pseudos("01h.pspgth"))

    # Set value of other variables.
    inp.set_vars(
        ecut=ecut,
        nband=1,
        diemac=2.0,
        toldfe=1e-6,
        prtwf=-1,
        iomode=3
    )

    # Define k-point sampling.
    inp.set_kmesh(ngkpt=(1, 1, 1), shiftk=(0, 0, 0))

    return inp


def build_flow(options):
    """
    Generate a flow to compute the total energy and forces for the H2 molecule in a big box
    as a function of the interatomic distance.

    Args:
        options: Command line options.

    Return:
        Flow object.
    """
    inputs = [gs_input(x=x) for x in np.linspace(0.5, 1.025, 21)]

    workdir = options.workdir if (options and options.workdir) else "flow_h2"

    return flowtk.Flow.from_inputs(workdir, inputs)


@flowtk.flow_main
def main(options):
    """
    This is our main function that will be invoked by the script.
    flow_main is a decorator implementing the command line interface.
    Command line args are stored in `options`.
    """
    return build_flow(options)


if __name__ == "__main__":
    sys.exit(main())
