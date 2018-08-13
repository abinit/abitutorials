This file explains how to use the AbiPy command line interface to run the calculation and analyze the results.
A web browser is a luxury when running calculations on a cluster while the command line is available everywhere!

I assume you are already familiar with python so I'm just giving hints on how to use the command line interface.

## Running the flow

Use:

    ./lessons_elastic.py --help

to get the list of available options.

    ./lessons_elastic.py 

to build the flow 
(well, AbiPy will complain because there's already a directory with the same name...)

Use:

    abirun.py FLOWDIR COMMAND

to interact with the flow and:

    abirun.py --help 

to access the documentation.
The debug COMMAND is quite handy if something goes wrong!

## How to post-process the results


Once the calculation is completed, use:

    abiopen.py flow_elastic/w0/outdata/out_DDB

to open the DDB file.
Then follow the examples given in the HTML page and try to reproduce them.
