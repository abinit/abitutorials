[![Nbviewer](https://img.shields.io/badge/render-nbviewer-orange.svg)](https://nbviewer.jupyter.org/github/abinit/abitutorials/blob/master/abitutorials/index.ipynb)
[![Binder](https://mybinder.org/badge.svg)](https://mybinder.org/v2/gh/abinit/abitutorials/master)
[![Build Status](https://travis-ci.org/abinit/abitutorials.svg?branch=master)](https://travis-ci.org/abinit/abitutorials)

WARNING: This package is under active development. 
Many things will change rapidly, including a possible history reset. 

[Index of jupyter notebooks](https://nbviewer.jupyter.org/github/abinit/abitutorials/blob/master/abitutorials/index.ipynb)

About
=====

This repository contains notebook-based documentation for [AbiPy](https://github.com/abinit/abipy)
This augments our Sphinx-based [documentation](http://pythonhosted.org/abipy/) with jupyter notebooks 
containing interactive tutorials and examples.
Additional examples are available on the:

* [AbiPy plot gallery](http://abinit.github.io/abipy/gallery/index.html)
* [AbiPy flow gallery](http://abinit.github.io/abipy/flow_gallery/index.html)
* [Pymatgen website](http://pymatgen.org/examples.html)

How to use the tutorials
========================

The repository contains the input required to run the lessons as well as the input files,
the main output in text format and the netcdf files.
There are several options available to you depending on the software installed on your machine.

You can:

- Follow the tutorial using the static 
  [HTML version](https://nbviewer.jupyter.org/github/abinit/abitutorials/blob/master/abitutorials/index.ipynb),
  and look at the input/output files in the github repository **without installing** AbiPy and Abinit.

- Click the **Launch Binder** badge to start a Docker image.
  The image contains Abinit, AbiPy and all the other python dependencies
  required to run the code inside the jupyter notebooks.
  The notebook will be opened in your browser after building.

- Install AbiPy and Abinit on your machine and use the python scripts as well as the netcdf files 
  in the github repository like a real pythonista.

If you opt for the last option, use:

    git clone https://github.com/abinit/abitutorials

to clone this repository on your machine.

To open the notebook in your browser, use::

    jupyter notebook FILE

Note that the notebook contains python code that will invoke Abinit 
so before executing the jupyter notebook you need to install all the required dependencies
(python, jupyter, abipy, abinit  and, obviously, a web browser)

In principle, you can use [pip](https://pip.pypa.io/en/stable/) to install python code with::

    pip install jupyter abipy

but then you may need to compile from source some of the low-level dependencies.
including the Abinit executable so the entire process could require 
some time and your host must provide a sane environment to build Fortran/C/C++ code, possibly with MPI support.

If you love building software from source, feel free to use this approach and 
use the configuration examples available on the [abiconfig repository](https://github.com/abinit/abiconda)
to build Abinit on your machine/cluster.

If you prefer to skip the compilation process, 
we suggest using the [conda](https://conda.io/miniconda.html) installer.
to install Abipy and (optionally) Abinit.
In what follows, we give the list of commands/steps required to bootstrap everything with conda.
More detailed instructions on how to install with conda are available
in the [abiconda](https://github.com/abinit/abiconda) documentation.

## How to install Abinit in five steps <a name="Abinit_in_five_steps"></a>

To install AbiPy with conda, download the `miniconda installer <https://conda.io/miniconda.html>`_
If you are a Linux user, download and install ``miniconda`` on your local machine with:

    wget https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh
    bash Miniconda3-latest-Linux-x86_64.sh

while for MacOSx use:

    curl -o https://repo.continuum.io/miniconda/Miniconda3-latest-MacOSX-x86_64.sh
    bash Miniconda3-latest-MacOSX-x86_64.sh

Answer ``yes`` to the question:

    Do you wish the installer to prepend the Miniconda3 install location
    to PATH in your /home/gmatteo/.bashrc ? [yes|no]
    [no] >>> yes

Source your ``.bashrc`` file to activate the changes done by ``miniconda`` to your ``$PATH``:

    source ~/.bashrc

Create a new conda environment (let's call it `abipy3.6`) based on python3.6 with::

    conda create --name abipy3.6 python=3.6

and activate it with::

    source activate abipy3.6

You should see the name of the conda environment in the shell prompt.

Now add ``conda-forge``, ``matsci`` and ``abinit`` to your conda channels with::

    conda config --add channels conda-forge
    conda config --add channels matsci
    conda config --add channels abinit

These are the channels from which we will download pymatgen, abipy and abinit.

To install AbiPy from the [abinit-channel](https://anaconda.org/abinit) use::

    conda install abipy -c abinit

At this point, open the python interpreter and import the following three modules
to check that the python installation is OK::

    import spglib
    import pymatgen
    from abipy import abilab 

At this point, you have installed the latest version of AbiPy and you can
start to use the AbiPy scripts from the command line to analyze the output results.
Note, however, that you won't be able to invoke Abinit from Abipy.
Firstly because we haven't installed Abinit yet (DOH!), secondly because
we have to generate two configuration files to tell AbiPy how to execute the Fortran code. 

Let's focus on the Abinit installation first.
To install the *parallel* version of abinit from the ``abinit channel`` use:

    conda install abinit --channel abinit

use which abinit
and perform a basic validation of the build by executing::

    abinit -b

Now we explain how to prepare the configuration files required by Abipy
Copy the `scheduler.yml` and `manager.yml` files from the `managers` directory 
of this repo to your `$HOME/.abinit/abipy` directory.

At this point, execute::

    abicheck.py

You should see:

The last test consists in executing a small calculation with AbiPy and Abinit.
Inside the shell, execute::

    abicheck.py --with-flow

to run a GS + NSCF band structure calculation for Si.
If the software stack is propertly configure, you should obtain:
