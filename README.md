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

The repository contains the input required to run the lessons as well as the main output 
and the netcdf files.
So there are several options available to you depending on the software installed on your machine.

You can:

- Follow the tutorial using the static 
  [HTML version](https://nbviewer.jupyter.org/github/abinit/abitutorials/blob/master/abitutorials/index.ipynb),
  and look at the input/output files in the github repository without having to install AbiPy and Abinit.
- Click the **Launch Binder** badge to start a Docker image.
  The image contains Abinit, AbiPy and all the other python dependencies
  required to run the code inside the jupyter notebooks.
  The notebook will be opened in your browser after building.
- Install AbiPy and Abinit on your machine and use the python scripts as well as the netcdf files 
  in the github repository like a real pythonista.

If you opt for the last option, use:

    git clone https://github.com/abinit/abitutorials

to clone this repository on your machine.
To install Abinit and Abipy we suggest using the [conda](https://conda.io/miniconda.html) installer.
Detailed instructions on how to install Abinit and Abipy with conda are available
in the [abiconda](https://github.com/abinit/abiconda) documentation.
