#!/usr/bin/env python
r"""
Flow for E-PH calculations
==========================

This flow computes the phonon linewidths and the Eliashberg function in Al.
"""
import sys
import abipy.data as abidata
import abipy.abilab as abilab
import abipy.flowtk as flowtk


def build_flow(options):
    """
    Build and return an AbiPy flow to compute phonon linewidths and Eliashberg function in Aluminium:

        1. Compute DFPT phonons on a 4x4x4 q-mesh with a coarse 8x8x8 k-sampling

        2. Generate 3 WFK files on a much denser k-mesh (x16, x24, x32)

        3. Run the EPH code with:

          - one of the WFK files generated in point 2.
          - interpolated DFPT potentials (from the initial 4x4x4 to a 8x8x8 q-mesh)

        4. Analyze the convergence of the results wrt nkpt.

    Note that the q-point grid must be a sub-grid of the k-point grid
    """
    workdir = options.workdir if (options and options.workdir) else "flow_eph_al"

    # Create empty flow.
    flow = flowtk.Flow(workdir=workdir)

    # Init structure. Use NC pseudo
    structure = abilab.Structure.fcc(a=7.5, species=["Al"], units="bohr")
    pseudos = abidata.pseudos("Al.oncvpsp")

    # Input for GS part.
    gs_inp = abilab.AbinitInput(structure, pseudos)
    gs_inp.set_vars(
        istwfk="*1",
        ecut=8.0,
        nband=4,
        occopt=7,      # Include metallic occupation function with a small smearing
        tsmear=0.04,
        tolvrs=1e-7,
    )

    # The k-grid is minimalistic to keep the calculation manageable.
    gs_inp.set_kmesh(
        ngkpt=[8, 8, 8],
        shiftk=[0.0, 0.0, 0.0],
    )

    # Build new input for NSCF calculation along k-path (automatically selected by AbiPy)
    # Used to plot the KS band structure.
    nscf_kpath_inp = gs_inp.new_with_vars(
        nband=4,
        tolwfr=1e-16,
        iscf=-2,
    )
    nscf_kpath_inp.set_kpath(ndivsm=10)

    # Build NSCF inputs with denser k-meshes
    # This step generates the WFK files used to compute the Eliashberg function.
    # We have a cubic material so we only need to specify the first number of divisions.
    nk_list = [16, 24, 32]

    nscf_kmesh_inputs = []
    for nk in nk_list:
        new_inp = gs_inp.new_with_vars(
            tolwfr=1e-16,
            iscf=-2,
            ngkpt=[nk] * 3,
            shiftk=[0.0, 0.0, 0.0],
        )
        nscf_kmesh_inputs.append(new_inp)

    # Register GS + NSCF kpath + NSCF with k-meshes in work0.
    work0 = flowtk.BandStructureWork(gs_inp, nscf_kpath_inp, dos_inputs=nscf_kmesh_inputs)
    flow.register_work(work0)

    # Generate Phonon work with 4x4x4 q-mesh
    # Reuse the variables from GS input and let AbiPy handle the generation of the input files
    # Note that the q-point grid is a sub-grid of the k-mesh so we do not need WFQ on k+q mesh.
    ddb_ngqpt = [4, 4, 4]
    ph_work = flowtk.PhononWork.from_scf_task(work0[0], ddb_ngqpt, is_ngqpt=True)
    flow.register_work(ph_work)

    # Ssction for EPH calculation: compute linewidths with different WFK files.
    eph_work = flowtk.Work()
    for ik, nk in enumerate(nk_list):
        # Each task uses a different WFK file. DDB and DBDB do not change.
        eph_deps = {work0[2 + ik]: "WFK", ph_work: ["DDB", "DVDB"]}

        # Interpolate DFPT potentials 4x4x4 --> 8x8x8
        eph_ngqpt_fine = (8, 8, 8)

        # Build input for E-PH run. See also v7/Input/t85.in
        # The k-points must be in the WFK file
        eph_inp = gs_inp.new_with_vars(
            optdriver=7,                    # Enter EPH driver.
            eph_task=1,                     # Compute phonon linewidths in metals.
            ddb_ngqpt=ddb_ngqpt,            # q-mesh used to produce the DDB file (must be consistent with DDB data)
            eph_fsewin="0.8 eV",            # Energy window around Ef (only states in this window are included)
            eph_intmeth=2,                  # Tetra method
            #eph_intmeth=1,                 # Gaussian
            #eph_fsmear=eph_fsmear * abilab.units.eV_to_Ha, # Broadening
            eph_ngqpt_fine=eph_ngqpt_fine,  # Interpolate DFPT potentials if != ddb_ngqpt
            eph_mustar=0.12,                # mustar parameter
            ngkpt=[nk] * 3,
            shiftk=[0.0, 0.0, 0.0],
        )

        # Set q-path to interpolate phonons and phonon linewidths.
        eph_inp.set_qpath(10)

        # Set q-mesh for phonons DOS and a2F(w)
        eph_inp.set_phdos_qmesh(nqsmall=24, method="tetra")
        eph_work.register_eph_task(eph_inp, deps=eph_deps)

    flow.register_work(eph_work)

    # Avoid producing (big) output files that not required by children.
    flow.allocate(use_smartio=True)

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
