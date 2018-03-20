This file explains how to use the AbiPy command line interface to run the calculation and analyze the results.
A web browser is a luxury when running calculations on a cluster while the command line is available everywhere!

I assume you are already familiar with python so I'm just giving hints on how to use the command line interface.

## Running the flow

Use:

    ./lessons_eph.py --help

to get the list of available options.

    ./lessons_eph_al.py 

to build the flow 
(well, AbiPy will complain because there's already a directory with the same name...)

Use:

    abirun.py FLOWDIR COMMAND

to interact with the flow and:

    abirun.py --help 

to access the documentation.
The debug COMMAND is quite handy if something goes wrong!

## How to analyze the electronic properties and the DOS

Use:

    abiview.py ebands flow_eph_al/w0/t1/outdata/out_GSR.nc

to visualize the electronic properties or, alternatively, open the file inside ipython with 

    abiopen.py flow_eph_al/w0/t1/outdata/out_GSR.nc

and start to interact with the python object directly.

The same approach can be used to analyze the total DDB file.
Use:

    abiview.py ddb flow_eph_al/w1/outdata/out_DDB

to produce plots with the vibrational properties and abiopen.py to open the file 
and access the AbiPy API directly.

To build a GsrRobot from the terminal with all the GSR files produced in w0, use:

    abicomp.py gsr flow_eph_al/w0/

and follow the examples given in the jupyter notebook to analyze the data.

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

## How to analyze A2F files

Use:

    abiview.py a2f flow_eph_al/w2/t0/outdata/out_A2F.nc

for a quick view of the results.

For a more flexible interface, open the file with abiopen.py

    abiopen.py a2f flow_eph_al/w2/t0/outdata/out_A2F.nc

and start to interact with the DdbFile object (use the TAB, Luke!)

To build a A2FRobot with all the A2F.nc files generated in the flow, use:

    abicomp.py a2f flow_eph_al

Use the ipython magic:

    %matplotlib 

and follow the examples given in the jupyter notebook to analyze the data.
