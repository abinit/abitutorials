# DFPT lesson with AbiPy

This file explains how to use the AbiPy command line interface to run the calculation and analyze the results.
A web browser is a luxury when running calculations on a cluster while the command line is available everywhere!
I assume you are already familiar with python so I'm just giving hints on how to use the command line interface.

## Running the flow

Use:

    ./lessons_dfpt.py --help

to get the list of available options.
Run the script without arguments:

    ./lessons_dfpt.py 

to build the flow (well, AbiPy will complain because there's already a directory with the same name...)

Use:

    abirun.py FLOWDIR COMMAND

to interact with the flow and:

    abirun.py --help 

to access the documentation.
The debug COMMAND is quite handy if something goes wrong!

## Convergence study at Γ

To build a DdbRobot with the "final" DDBs in the Work directories, use:

    abicomp.py ddb flow_alas_ecut_conv/w*/outdata/

then, inside ipython, type:

    %matplotlib
    data_gamma = robot.get_dataframe_at_qpoint((0, 0, 0))

and follow the examples given in the jupyter notebook.
Feel free to explore the AbiPy API!

Use:

    robot. + <TAB>

in ipython to get autocompletion.

Use:

    robot.method?

to get the documentation of method and 

    robot.method??

to inspect the code like real pythonista.

TIPS:

    1. Plot methods start with `plot_`
    2. Methods invoking abinit starts with `abiget`
    3. Methods invoking anaddb starts with `anaget`
    4. Methods returning results usually start with `get_`

## Phonon band structure of AlAs

Use:

    abiview.py ddb flow_alas_phonons/outdata/out_DDB

for a quick view of the results.

For a more flexible interface, open the file with:

    abiopen.py flow_alas_phonons/outdata/out_DDB

and start to interact with the DdbFile object (use the TAB, Luke!)
To print the `abifile` without starting an ipython session, use:

    abiopen.py flow_alas_phonons/outdata/out_DDB -p

The same API can be used for other files...

Any file with structural information can be passed as argument to `abistruct.py`.
Use `abistruct.py --help`, Luke
