#!/usr/bin/env python
"""Calculations of the Fan-Migdal Debye-Waller self-energy in diamond."""
from __future__ import print_function, division, unicode_literals, absolute_import

import os
import sys
import numpy as np
import abipy.data as abidata
import abipy.abilab as abilab
import abipy.flowtk as flowtk


def build_flow(options):
    """
    C in diamond structure. Very rough q-point mesh, low ecut, completely unconverged.
    The flow computes the ground state density and a WFK file on a 8x8x8 k-mesh including
    empty states needed for the self-energy. Then all the independent atomic perturbations
    for the irreducible qpoints in a 4x4x4 grid are obtained with DFPT.
    Finally, we enter the EPH driver to compute the EPH self-energy.
    """
    workdir = options.workdir if (options and options.workdir) else "flow_diamond"

    # Define structure explicitly.
    structure = abilab.Structure.from_abivars(
        acell=3*[6.70346805],
        rprim=[0.0, 0.5, 0.5,
               0.5, 0.0, 0.5,
               0.5, 0.5, 0.0],
        typat=[1, 1],
        xred=[0.0, 0.0, 0.0, 0.25, 0.25, 0.25],
        ntypat=1,
        znucl=6,
    )

    # Initialize input from structure and norm-conserving pseudo provided by AbiPy.
    gs_inp = abilab.AbinitInput(structure, pseudos="6c.pspnc")

    # Set basic variables for GS part.
    gs_inp.set_vars(
        istwfk="*1",
        ecut=20.0,          # Too low, shout be ~30
        nband=4,
        tolvrs=1e-8,
    )

    # The kpoint grid is minimalistic to keep the calculation manageable.
    # The q-mesh for phonons must be a submesh of this one.
    gs_inp.set_kmesh(
        ngkpt=[8, 8, 8],
        shiftk=[0.0, 0.0, 0.0],
    )

    # Build new input for NSCF calculation with k-path (automatically selected by AbiPy)
    # Used to plot the KS band structure and interpolate the QP corrections.
    nscf_kpath_inp = gs_inp.new_with_vars(
        nband=8,
        tolwfr=1e-16,
        iscf=-2,
    )
    nscf_kpath_inp.set_kpath(ndivsm=10)

    # Build another NSCF input with k-mesh and empty states.
    # This step generates the WFK file used to build the EPH self-energy.
    nscf_empty_kmesh_inp = gs_inp.new_with_vars(
        nband=210,     # Too low. ~300
        nbdbuf=10,     # Reduces considerably the time needed to converge empty states!
        tolwfr=1e-16,
        iscf=-2,
    )

    # Create empty flow.
    flow = flowtk.Flow(workdir=workdir)

    # Register GS + band structure parts in the first work
    work0 = flowtk.BandStructureWork(gs_inp, nscf_kpath_inp, dos_inputs=[nscf_empty_kmesh_inp])
    flow.register_work(work0)

    # Generate Phonon work with 4x4x4 q-mesh
    # Reuse variables from GS input and let AbiPy handle the generation of the input files
    # Note that the q-point grid is a sub-grid of the k-point grid (here 8x8x8)
    ddb_ngqpt = [4, 4, 4]
    ph_work = flowtk.PhononWork.from_scf_task(work0[0], ddb_ngqpt, is_ngqpt=True,
                                              tolerance={"tolvrs": 1e-6})  # This to speedup DFPT
    flow.register_work(ph_work)

    # Build template for self-energy calculation. See also v8/Input/t44.in
    # The k-points must be in the WFK file
    #
    eph_inp = gs_inp.new_with_vars(
        optdriver=7,             # Enter EPH driver.
        eph_task=4,              # Activate computation of EPH self-energy.
        ddb_ngqpt=ddb_ngqpt,     # q-mesh used to produce the DDB file (must be consistent with DDB data)
        symsigma=1,              # Use symmetries in self-energy integration (IBZ_k instead of BZ)
        nkptgw=1,
        kptgw=[0, 0, 0],
        bdgw=[1, 8],
        # For more k-points...
        #nkptgw=2,
        #kptgw=[0, 0, 0,
        #       0.5, 0, 0],
        #bdgw=[1, 8, 1, 8],
        #gw_qprange=-4,
        tmesh=[0, 200, 5],    # (start, step, num)
        zcut="0.2 eV",
    )

    # Set q-path for Fourier interpolation of phonons.
    eph_inp.set_qpath(10)

    # Set q-mesh for phonons DOS.
    eph_inp.set_phdos_qmesh(nqsmall=16, method="tetra")

    # EPH part requires the GS WFK, the DDB file with all perturbations
    # and the database of DFPT potentials (already merged by PhononWork)
    deps = {work0[2]: "WFK", ph_work: ["DDB", "DVDB"]}

    # Now we use the EPH template to perform a convergence study in which
    # we change the q-mesh used to integrate the self-energy and the number of bands.
    # The code will activate the Fourier interpolation of the DFPT potentials if eph_ngqpt_fine != ddb_ngqpt

    for eph_ngqpt_fine in [[4, 4, 4], [8, 8, 8]]:
        # Create empty work to contain EPH tasks with this value of eph_ngqpt_fine
        eph_work = flow.register_work(flowtk.Work())
        #for nband in [50, 100, 200]:
        for nband in [100, 150, 200]:
            new_inp = eph_inp.new_with_vars(eph_ngqpt_fine=eph_ngqpt_fine, nband=nband)
            eph_work.register_eph_task(new_inp, deps=deps)

    # Generate last work with our best parameters to compute the QP correction in the IBZ
    # We include all occupied states and 4 empty bands.
    # The QP corrections in the IBZ are then interpolate with star functions
    #new_inp = eph_inp.new_with_vars(eph_ngqpt_fine=[8, 8, 8], nband=100)
    #new_inp.pop_vars(["nkptgw", "kptgw", "bdgw"])
    #new_inp["gw_qprange"] = -4
    #flow.register_eph_task(new_inp, deps=deps, task_class=flowtk.EphTask, append=False)

    flow.allocate()

    return flow


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
