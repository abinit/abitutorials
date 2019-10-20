#!/usr/bin/env python
import sys
import abipy.data as abidata
import abipy.abilab as abilab
import abipy.flowtk as flowtk


def make_inputs(ngkpt, dos_ngkpt=(6, 6, 6), paral_kgb=0):
    """
    Crystalline silicon: calculation of the G0W0 band structure with the scissors operator.

    Args:
        ngkpt: list of 3 integers. Abinit variable defining the k-point sampling.
        dos_ngkpt: list of 3 integers. k-point sampling for DOS.
        paral_kgb: Option used to select the eigensolver in the GS part.

    Return:
        Six AbinitInput objects:

        [0]: Ground state run to get the density.
        [1]: NSCF run to get the KS band structure on a high-symmetry k-path.
        [2]: NSCF run with a homogeneous sampling of the BZ to compute the KS DOS with `dos_ngkpt`.
        [3]: NSCF run with empty states to prepare the GW steps.
        [4]: Calculation of the screening from the WFK file computed in dataset 4.
        [5]: Use the SCR file computed at step 5 and the WFK file computed in dataset 4 to get the GW corrections.
    """
    multi = abilab.MultiDataset(abidata.cif_file("si.cif"),
                                pseudos=abidata.pseudos("14si.pspnc"), ndtset=6)

    # Add mnemonics to input file.
    multi.set_mnemonics(True)

    # This grid is the most economical and we will use it for the GS.
    # Note that it does not contain Gamma point so we cannot use it to
    # compute the QP corrections at the Gamma point.
    scf_kmesh = dict(
        ngkpt=ngkpt,
        shiftk=[0.5, 0.5, 0.5,
                0.5, 0.0, 0.0,
                0.0, 0.5, 0.0,
                0.0, 0.0, 0.5]
    )

    # k-point sampling for DOS (gamma-centered)
    dos_kmesh = dict(
        ngkpt=dos_ngkpt,
        shiftk=[0.0, 0.0, 0.0])

    # This grid contains the Gamma point, which is the point at which
    # we will compute the (direct) band gap.
    gw_kmesh = dict(
        ngkpt=ngkpt,
        shiftk=[0.0, 0.0, 0.0,
                0.0, 0.5, 0.5,
                0.5, 0.0, 0.5,
                0.5, 0.5, 0.0]
    )

    # Global variables
    ecut = 6
    multi.set_vars(
        ecut=ecut,
        istwfk="*1",
        paral_kgb=paral_kgb,
        gwpara=2,
    )

    # Dataset 1 (GS run to get the density)
    multi[0].set_kmesh(**scf_kmesh)
    multi[0].set_vars(
        tolvrs=1e-6,
        nband=4,
    )
    multi[0].set_kmesh(**scf_kmesh)

    # Dataset 2 (NSCF run with k-path)
    multi[1].set_vars(iscf=-2,
                      tolwfr=1e-12,
                      nband=8,
                      )
    multi[1].set_kpath(ndivsm=8)

    # Dataset 3 (DOS NSCF)
    multi[2].set_vars(iscf=-2,
                      tolwfr=1e-12,
                      nband=8,
                      )
    multi[2].set_kmesh(**dos_kmesh)

    # Dataset 4 (NSCF run to produce WFK for GW, note the presence of empty states)
    multi[3].set_vars(iscf=-2,
                      tolwfr=1e-12,
                      nband=35,
                     )
    multi[3].set_kmesh(**gw_kmesh)

    # Dataset3: Calculation of the screening.
    multi[4].set_vars(
        optdriver=3,
        nband=25,
        ecutwfn=ecut,
        symchi=1,
        inclvkb=0,    # Disable [Vnl, r] contribution for q --> 0
        ecuteps=4.0,
    )
    multi[4].set_kmesh(**gw_kmesh)

    multi[5].set_vars(
            optdriver=4,
            nband=10,
            ecutwfn=ecut,
            ecuteps=4.0,
            ecutsigx=6.0,
            symsigma=1,
            gw_qprange=-4,  # Compute GW corrections for all kpts in IBZ,
                            # all occupied states and 4 empty states,
        )
    multi[5].set_kmesh(**gw_kmesh)

    return multi.split_datasets()


def build_g0w0_flow(options=None, ngkpt=(2, 2, 2)):
    """
    Build and return a flow with two works.
    The first work is a standard KS band-structure calculation that consists of
    an initial GS calculation to get the density followed by two NSCF calculations.

    The first NSCF task computes the KS eigenvalues on a high-symmetry path in the BZ,
    whereas the second NSCF task employs a homogeneous k-mesh so that one can compute
    the DOS from the KS eigenvalues.

    The second work represents the real GW workflow that uses the density computed in the first task of
    the previous work  to compute the KS bands for many empty states.
    The WFK file produced in this step is then used to compute the screened interaction $W$.
    Finally, we perform a self-energy calculation that uses the $W$ produced
    in the previous step and the WFK file to compute the matrix elements of the self-energy and
    the $G_0W_0$ corrections for all the k-points in the IBZ and 8 bands (4 occupied + 4 empty)
    """

    # Call make_input to build our 4 input objects.
    scf, bands_nscf, dos_nscf, gw_nscf, scr, sig = make_inputs(ngkpt=ngkpt)

    workdir = options.workdir if (options and options.workdir) else "flow_g0w0"
    flow = flowtk.Flow(workdir=workdir)

    # Add KS band structure work (SCF-GS followed by two NSCF runs
    # (the first one is done on a k-path, the second on the IBZ to compute the DOS
    work0 = flowtk.BandStructureWork(scf, bands_nscf, dos_inputs=dos_nscf)
    flow.register_work(work0)

    # Create new Work for GW
    work1 = flowtk.Work()

    # NSCF run with empty states
    gw_nscf_task = work1.register_nscf_task(gw_nscf, deps={work0[0]: "DEN"})

    # SCR run with WFK produced by previous task.
    scr_task = work1.register_scr_task(scr, deps={gw_nscf_task: "WFK"})

    # SIGMA task (requires WFK with empty states and SCR file)
    sigma_task = work1.register_sigma_task(sig, deps={gw_nscf_task: "WFK", scr_task: "SCR"})

    # Add GW work to flow.
    flow.register_work(work1)

    return flow


@flowtk.flow_main
def main(options):
    return build_g0w0_flow(options)


if __name__ == "__main__":
    sys.exit(main())
