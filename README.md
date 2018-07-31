[![Nbviewer](https://img.shields.io/badge/render-nbviewer-orange.svg)](https://nbviewer.jupyter.org/github/abinit/abitutorials/blob/master/abitutorials/index.ipynb)
[![Binder](https://mybinder.org/badge.svg)](https://mybinder.org/v2/gh/abinit/abitutorials/master)
[![Build Status](https://travis-ci.org/abinit/abitutorials.svg?branch=master)](https://travis-ci.org/abinit/abitutorials)

[![Coverage Status](https://coveralls.io/repos/github/abinit/abitutorials/badge.svg?branch=master)](https://coveralls.io/github/abinit/abitutorials?branch=master)

[Index of jupyter notebooks](https://nbviewer.jupyter.org/github/abinit/abitutorials/blob/master/abitutorials/index.ipynb)

About
=====

This repository contains notebook-based documentation for [AbiPy](https://github.com/abinit/abipy).
This augments our Sphinx-based [documentation](http://pythonhosted.org/abipy/) with jupyter notebooks 
containing interactive tutorials and examples.
Additional examples are available on the:

* [AbiPy plot gallery](http://abinit.github.io/abipy/gallery/index.html)
* [AbiPy flow gallery](http://abinit.github.io/abipy/flow_gallery/index.html)
* [Pymatgen website](http://pymatgen.org/examples.html)

How to use the tutorials
========================

The repository contains the input required to run the lessons on Abipy, as well as the input files,
the main output in text format and the netcdf files. The workhorse of these tutorials are so-called 'jupyter notebooks'.
There are several options available to you depending on the software installed on your machine.

You can:

1. Follow the tutorial using the static 
   [HTML version](https://nbviewer.jupyter.org/github/abinit/abitutorials/blob/master/abitutorials/index.ipynb),
   and look at the input/output files in jupyter notebooks in the github repository **without installing** AbiPy and Abinit.

2. Click the **Launch Binder** badge to start a Docker image.
   The image contains Abinit, AbiPy and all the other python dependencies
   required to run the code inside the jupyter notebooks.
   The notebook will be opened in your browser after building.
   Go into the `abitutorials` directory and click the `index.ipynb` file to open the index file.
   Select e.g. the `Structure` notebook and start to run the python code in the jupyter cells
   (select the cell and click the `Run` button). 
   See also the other options available in the `Cell` tab.

3. Install AbiPy, Abinit and Jupyter on your machine (see later) and use the python scripts as well as the netcdf files 
   in the github repository (you also need git), like a real pythonista. You will need to execute the jupyter notebooks, and thus 
   install all the required dependencies: python, jupyter, abipy, abinit  and obviously a web browser (DOH!).

Of course, choosing between these options depends on what is your actual interest with Abipy.
You might only be interested in getting a flavour of how to use Abipy (or what are these Abipy tutorials), without actually using Abipy.
Then options 1 or 2 are convenient.

However, if you really plan to use Abipy, we suggest you choose 2 or 3. Really running the examples is the most efficient use of the tutorial.
Of course, in order to use Abipy, you will obviously need to install it, as well as to install abinit. 
Choosing 2 only spare you the possible trouble of installing jupyter. The installation of Abipy and abinit (also using git) in a coherent way
is presented in the [Abipy README on Github](https://github.com/abinit/abipy), 
or in [the stable version of the Abipy doc](https://pythonhosted.org/abipy/installation.html),  
or in [the develop version of the Abipy doc](https://abinit.github.io/abipy/installation.html). 

If you opt for option 3, after installing jupyter as described below, in addition to AbiPy and abinit, you will have to
open the notebook in your browser 

    jupyter notebook FILE.ipynb

where FILE.ipynb is one the ipython notebooks available inside the `abitutorials` directory. 
To open, for instance, the notebook for the first lesson, use:

    cd abitutorials
    jupyter notebook base1/lesson_base1.ipynb

Acccessing the notebooks and installing jupyter
===============================================

First step, download the abitutorials

    git clone https://github.com/abinit/abitutorials

In case you followed the conda way to [install Abipy and abinit](https://github.com/abinit/abipy), the installation of jupyter is very simple.
Be sure to install it *in the same conda environment* as Abipy and abinit, though.

Inside the *abitutorials* directory, issue

    conda install --file ./requirements.txt

Then, you might also like to install graphviz and python-graphviz, in order to allow the full vizualization of figures in the tutorials.

    conda install graphviz
    conda install python-graphviz 

More detailed instructions on how to install with conda are available
in the [abiconda](https://github.com/abinit/abiconda) documentation.

As an alternative to conda, you can use [pip](https://pip.pypa.io/en/stable/) to install python code for jupyter with:

    pip install jupyter abipy

Note, however, that you may need to compile from source some of the low-level dependencies
including the Abinit executable so the entire process could require some time,
besides your machine must provide a sane environment to build Fortran/C/C++ code, possibly with MPI support.

If you love building software from source, feel free to use this approach and 
use the configuration examples available on the [abiconfig repository](https://github.com/abinit/abiconda)
to build Abinit on your machine/cluster.

After installing jupyter, we can launch one of the notebooks as described above.

As a test of the coherent installation of AbiPy and abinit, select one of the directory with a lesson_*.py script e.g. sigeph/lesson_sigeph.py.
Read the corresponding README.md file. Then look at the python script and use:

    ./lesson_sigeph.py

to run the flow automatically or 

    ./lesson_sigeph.py --help

to get the list of supported options.

TIP:

All the AbiPy scripts start with the `abi` prefix. 
Just type:

    abi + <TAB> 
    
in the shell to get the list of possible scripts.
Please consult the [AbiPy documentation](http://abinit.github.io/abipy/index.html) for further details.
