#!/usr/bin/env python
"""Optical properties with excitonic effects (Bethe-Salpeter formalism)."""
import sys
import abipy.abilab as abilab
import abipy.flowtk as flowtk
import abipy.data as abidata


def make_scf_nscf_bse_inputs(ngkpt=(6, 6, 6), ecut=6, ecuteps=3,
                             mdf_epsinf=12.0, mbpt_sciss="0.8 eV"):
    """
    Build and returns three `AbinitInput` objects to perform a
    GS-SCF + GS-NSCF + BSE calculation with model dielectric function.

    Args:
        ngkpt: Three integers giving the number of divisions for the k-mesh.
        ecut: Cutoff energy for the wavefunctions.
        ecuteps: Cutoff energy for the screened interation W_{GG'}.
        mdf_epsinf: Static limit of the macroscopic dielectric functions.
            Used to build the model dielectric function.
        mbpt_sciss: Scissors operator energy (used to open the initial KS gap).
    """
    multi = abilab.MultiDataset(structure=abidata.structure_from_ucell("Si"),
                                pseudos=abidata.pseudos("14si.pspnc"), ndtset=3)
    multi.set_mnemonics(True)

    # Variables common to the three datasets.
    multi.set_vars(
        ecut=ecut,
        nband=8,
        istwfk="*1",
        diemac=12.0,
        #iomode=3,
    )

    # SCF run to get the density.
    multi[0].set_vars(tolvrs=1e-8)
    multi[0].set_kmesh(ngkpt=ngkpt, shiftk=(0, 0, 0))

    # NSCF run on a randomly shifted k-mesh (improve the convergence of optical properties)
    multi[1].set_vars(
        iscf=-2,
        nband=15,
        tolwfr=1e-8,
        chksymbreak=0,  # Skip the check on the k-mesh.
    )

    # This shift breaks the symmetry of the k-mesh.
    multi[1].set_kmesh(ngkpt=ngkpt, shiftk=(0.11, 0.21, 0.31))

    # BSE run with Haydock iterative method (only resonant + W + v)
    multi[2].set_vars(
        optdriver=99,                 # BS calculation
        chksymbreak=0,                # To skip the check on the k-mesh.
        bs_calctype=1,                # L0 is constructed with KS orbitals and energies.
        mbpt_sciss=mbpt_sciss,        # Scissors operator used to correct the KS band structure.
        bs_exchange_term=1,           # Exchange term included.
        bs_coulomb_term=21,           # Coulomb term with model dielectric function.
        mdf_epsinf=mdf_epsinf,        # Parameter for the model dielectric function.
        bs_coupling=0,                # Tamm-Dancoff approximation.
        bs_loband=2,                  # Lowest band included in the calculation
        nband=6,                      # Highest band included in the calculation
        bs_freq_mesh="0 6 0.02 eV",   # Frequency mesh for the dielectric function
        bs_algorithm=2,               # Use Haydock method.
        zcut="0.15 eV",               # Complex shift to avoid divergences in the continued fraction.
        ecutwfn=ecut,                 # Cutoff for the wavefunction.
        ecuteps=ecuteps,              # Cutoff for W and /bare v.
        inclvkb=2,                    # The commutator for the optical limit is correctly evaluated.
    )

    # Same shift as the one used in the previous dataset.
    multi[2].set_kmesh(ngkpt=ngkpt, shiftk=(0.11, 0.21, 0.31))

    scf_input, nscf_input, bse_input = multi.split_datasets()

    return scf_input, nscf_input, bse_input


def build_bse_flow(options):
    """
    Build a flow to solve the BSE with default parameters.

    Args:
        options: Command line options.

    Return:
        Flow object.
    """
    workdir = options.workdir if (options and options.workdir) else "flow_bse"
    flow = flowtk.Flow(workdir=workdir)

    # Build a Work for BSE calculation with the model dielectric function ...
    scf_inp, nscf_inp, bse_inp = make_scf_nscf_bse_inputs()

    work = flowtk.BseMdfWork(scf_inp, nscf_inp, bse_inp)

    # and add it to the flow
    flow.register_work(work)

    return flow


def build_bse_metallicW_flow(options):
    """
    Build a flow to solve the BSE with metallic screening.
    Note the value of `mdf_epsinf`.

    Args:
        options: Command line options.

    Return:
        Flow object.
    """
    workdir = options.workdir if (options and options.workdir) else "flow_bse_metallicW"
    flow = flowtk.Flow(workdir=workdir)

    # Model dielectric function with metallic screening
    scf_inp, nscf_inp, bse_inp = make_scf_nscf_bse_inputs(ngkpt=(4, 4, 4), ecut=6, ecuteps=3,
                                                          mdf_epsinf=1.0e+12)

    flow.register_work(flowtk.BseMdfWork(scf_inp, nscf_inp, bse_inp))

    return flow


def build_bse_kconv_flow(options):
    """
    Build a flow to analyze the convergence of the BSE spectrum wrt k-point sampling.

    Args:
        options: Command line options.

    Return:
        Flow object.
    """
    workdir = options.workdir if (options and options.workdir) else "flow_bse_kconv"
    flow = flowtk.Flow(workdir=workdir)

    # 3 works with differet ngkpt.
    for nk in [4, 6, 8]:
        scf_inp, nscf_inp, bse_inp = make_scf_nscf_bse_inputs(ngkpt=3 * [nk], ecut=6, ecuteps=3)
        work = flowtk.BseMdfWork(scf_inp, nscf_inp, bse_inp)
        flow.register_work(work)

    return flow


@flowtk.flow_main
def main(options):
    """
    This is our main function that will be invoked by the script.
    flow_main is a decorator implementing the command line interface.
    Command line args are stored in `options`.
    """
    flow = build_bse_flow(options)
    #flow = build_bse_metallicW_flow(options)
    #flow = build_bse_kconv_flow(options)
    return flow


if __name__ == "__main__":
    sys.exit(main())
