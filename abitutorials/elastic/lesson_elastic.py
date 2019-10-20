#!/usr/bin/env python
r"""
Flow for elastic constants and piezoelectric tensor with DFPT
=============================================================

This example shows how to use AbiPy to calculate physical properties
related to strain for an insulator.

    - the rigid-atom elastic tensor
    - the rigid-atom piezoelectric tensor (insulators only)
    - the internal strain tensor
    - the atomic relaxation corrections to the elastic and piezoelectric tensor

Here we follow the discussion presented in
in the `official tutorial <https://docs.abinit.org/tutorial/elastic/>`_

The DDB file with all the perturbations will be produced automatically at the end of the run
and saved in ``flow_elastic/w0/outdata/out_DDB``.
"""
import sys
import numpy as np
import abipy.abilab as abilab
import abipy.data as abidata

from abipy import flowtk


def make_scf_input(ngkpt=(4, 4, 4)):
    """
    This function constructs the input file for the GS calculation of
    AlAs in hypothetical wurzite (hexagonal) structure.
    In principle, the stucture should be relaxed before starting the calculation,
    here we use the *unrelaxed* geometry of the official tutorial.

    Args:
        ngkpt: K-mesh used both in the GS and in the DFPT part.
    """

    # Initialize structure. Use enough significant digits
    # so that Abinit will recognize the correct spacegroup
    # (Hexagonal and rhombohedral lattices are a bit problematic).
    structure = abilab.Structure.from_abivars(
        acell=[7.5389648144E+00, 7.5389648144E+00, 1.2277795374E+01],
        natom=4,
        ntypat=2,
        rprim=[ np.sqrt(0.75), 0.5, 0.0 ,
               -np.sqrt(0.75), 0.5, 0.0,
                          0.0, 0.0, 1.0],
        typat=[1, 1, 2, 2],
        xred=[1/3, 2/3, 0,
              2/3, 1/3, 1/2,
              1/3, 2/3, 3.7608588373E-01,
              2/3, 1/3, 8.7608588373E-01],
        znucl=[13, 33],
    )

    pseudos = abidata.pseudos("13al.pspnc", "33as.pspnc")
    gs_inp = abilab.AbinitInput(structure, pseudos=pseudos)

    # Set other important variables (consistent with tutorial)
    # All the other DFPT runs will inherit these parameters.
    gs_inp.set_vars(
        nband=8,
        ecut=6.0,
        ecutsm=0.5,        # Important when performing structural optimization
                           # with variable cell. All DFPT calculations should use
                           # the same value to be consistent.
        ngkpt=ngkpt,
        nshiftk=1,
        shiftk=[0.0, 0.0, 0.5],   # This choice preserves the hexagonal symmetry of the grid.
        diemac=9.0,
        nstep=40,
        paral_kgb=0,
        tolvrs=1.0e-18,
    )

    return gs_inp


def build_flow(options=None):
    """
    Create a `Flow` for phonon calculations. The flow has one work with:

        - 1 GS Task
        - 3 DDK Task
        - 4 Phonon Tasks (Gamma point)
        - 6 Elastic tasks (3 uniaxial + 3 shear strain)

    The Phonon tasks and the elastic task will read the 3 DDK files produced at the beginning
    """
    workdir = options.workdir if (options and options.workdir) else "flow_elastic"

    flow = flowtk.Flow(workdir=workdir)

    # Build input for GS calculation and register the first work.
    scf_input = make_scf_input()

    # Build work for elastic properties (clamped-ions)
    # activate internal strain and piezoelectric part.
    elast_work = flowtk.ElasticWork.from_scf_input(scf_input, with_relaxed_ion=True, with_piezo=True)

    flow.register_work(elast_work)

    return flow


def build_ngkpt_convflow(options=None, ngkpt_list=([2, 2, 2], [4, 4, 4], [8, 8, 8])):
    """
    Build and return a flow computing elastic and piezoelectric properties with
    different k-point samplings given in `ngkpt_list`.
    In principle, one should perform different structural relaxations for each `ngkpt`
    and use the relaxed structures to compute elastic properties.
    """
    workdir = options.workdir if (options and options.workdir) else "flow_elastic_ngkpt_conv"

    flow = flowtk.Flow(workdir=workdir)

    for ngkpt in ngkpt_list:
        scf_input = make_scf_input(ngkpt=ngkpt)

        elast_work = flowtk.ElasticWork.from_scf_input(scf_input, with_relaxed_ion=True, with_piezo=True)

        flow.register_work(elast_work)

    return flow


@flowtk.flow_main
def main(options):
    """
    This is our main function that will be invoked by the script.
    flow_main is a decorator implementing the command line interface.
    Command line args are stored in `options`.
    """
    # Compute elastic and piezoletric properties (no convergence study)
    #return build_flow(options=options)

    # Convergence study wrt nkpt
    return build_ngkpt_convflow(options=options)


if __name__ == "__main__":
    sys.exit(main())
