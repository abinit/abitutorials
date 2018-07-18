[![Nbviewer](https://img.shields.io/badge/render-nbviewer-orange.svg)](https://nbviewer.jupyter.org/github/abinit/abitutorials/blob/master/abitutorials/index.ipynb)
[![Binder](https://mybinder.org/badge.svg)](https://mybinder.org/v2/gh/abinit/abitutorials/master)
[![Build Status](https://travis-ci.org/abinit/abitutorials.svg?branch=master)](https://travis-ci.org/abinit/abitutorials)

[![Coverage Status](https://coveralls.io/repos/github/abinit/abitutorials/badge.svg?branch=master)](https://coveralls.io/github/abinit/abitutorials?branch=master)

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
  Go into the `abitutorials` directory and click the `index.ipynb` file to open the index file.
  Select e.g. the `Structure` notebook and start to run the python code in the jupyter cells
  (select the cell and click the `Run` button). 
  See also the other options available in the `Cell` tab.

- Install AbiPy and Abinit on your machine and use the python scripts as well as the netcdf files 
  in the github repository like a real pythonista.

If you opt for the last option, use:

    git clone https://github.com/abinit/abitutorials

to clone this repository on your machine.

To open the notebook in your browser, use the command:

    jupyter notebook FILE.ipynb

where FILE.ipynb is one the ipython notebooks available inside the `abitutorials`
directory.

To open, for instance, the notebook for the first lessons, use:

    cd abitutorials
    jupyter notebook base1/lesson_base1.ipynb

Note that the notebook contains python code that will invoke Abinit 
so before executing the jupyter notebook you need to install all the required dependencies:
python, jupyter, abipy, abinit  and obviously a web browser (DOH!)

In principle, you can use [pip](https://pip.pypa.io/en/stable/) to install python code with:

    pip install jupyter abipy

Note, however, that you may need to compile from source some of the low-level dependencies
including the Abinit executable so the entire process could require some time,
besides your machine must provide a sane environment to build Fortran/C/C++ code, possibly with MPI support.

If you love building software from source, feel free to use this approach and 
use the configuration examples available on the [abiconfig repository](https://github.com/abinit/abiconda)
to build Abinit on your machine/cluster.

If you prefer to skip the compilation process, 
we suggest using the [conda](https://conda.io/miniconda.html) to install Abipy and (optionally) Abinit.
In what follows, we give the list of steps required to bootstrap everything with conda.
More detailed instructions on how to install with conda are available
in the [abiconda](https://github.com/abinit/abiconda) documentation.

## How to install Abinit in five steps <a id="Abinit_in_five_steps"></a>

To install AbiPy with conda, download the [miniconda installer](https://conda.io/miniconda.html)
If you are a Linux user, download and install `miniconda` on your local machine with:

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

Create a new conda environment (let's call it `abienv`) based on python3.6 with:

    conda create --name abienv python=3.6

and activate it with:

    source activate abienv

You should see the name of the conda environment in the shell prompt.

Now add ``conda-forge``, ``matsci`` and ``abinit`` to your conda channels with:

    conda config --add channels conda-forge
    conda config --add channels matsci
    conda config --add channels abinit

These are the channels from which we will download pymatgen, abipy and abinit.

To install AbiPy from the [abinit-channel](https://anaconda.org/abinit) use::

    conda install abipy -c abinit

Now open the python interpreter and import the following three modules
to check that the python installation is OK:

```python
import spglib
import pymatgen
from abipy import abilab 
```

At this point, we have installed the latest version of AbiPy and we can
start to use the AbiPy scripts from the command line to analyze the output results.
Note, however, that you won't be able to invoke Abinit from Abipy.
Firstly because we haven't installed Abinit yet (DOH!), secondly because
we have to generate two configuration files to tell AbiPy how to execute the Fortran code. 

Let's focus on the Abinit installation first.
To install the *parallel* version of abinit from the ``abinit channel`` use:

    conda install abinit --channel abinit

The Abinit executables are placed inside the anaconda directory associated to the ``abienv`` environment:

    which abinit
    /Users/gmatteo/anaconda3/envs/abienv/bin/abinit

To perform a basic validation of the build, execute:

    abinit -b

Now we explain how to prepare the configuration files required by Abipy
For a more detailed description of the syntax used in this configuration file
please consult the [TaskManager documentation](http://abinit.github.io/abipy/workflows/taskmanager.html).

Copy the `scheduler.yml` and `manager.yml` files from the `managers` directory 
of this repository to your `$HOME/.abinit/abipy` directory.
Open `manager.yml` and make sure that the `pre_run` section contains the shell commands 
needed to setup the environment before launching Abinit (e.g. Abinit is in $PATH)

At this point, execute:

    abicheck.py

You should see:

```shell
$ abicheck.py
AbiPy Manager:
[Qadapter 0]
ShellAdapter:localhost
Hardware:
   num_nodes: 2, sockets_per_node: 1, cores_per_socket: 2, mem_per_node 4096,
Qadapter selected: 0

Abinitbuild:
Abinit Build Information:
    Abinit version: 8.7.6
    MPI: True, MPI-IO: True, OpenMP: False
    Netcdf: True

Abipy Scheduler:
PyFlowScheduler, Pid: 19379
Scheduler options: {'weeks': 0, 'days': 0, 'hours': 0, 'minutes': 0, 'seconds': 5}

Installed packages:
Package         Version
--------------  ---------
system          Darwin
python_version  3.6.1
numpy           1.14.2
scipy           1.0.0
netCDF4         1.3.1
apscheduler     2.1.0
pydispatch      2.0.5
yaml            3.12
pymatgen        2018.3.14


Abipy requirements are properly configured
```

If the script fails with the error message:

    Abinit executable does not support netcdf
    Abipy requires Abinit version >= 8.0.8 but got 0.0.0

it means that your environment is not property configured or that there's a problem
with the binary executable.
In this case, look at the files produced in the temporary directory of the flow.
The script reports the name of the directory, something like:

    CRITICAL:pymatgen.io.abinit.tasks:Error while executing /var/folders/89/47k8wfdj11x035svqf8qnl4m0000gn/T/tmp28xi4dy1/job.sh

Check the `job.sh` script for possible typos, then search for possible error messages in `run.err`.

The last test consists in executing a small calculation with AbiPy and Abinit.
Inside the shell, execute:

    abicheck.py --with-flow

to run a GS + NSCF band structure calculation for Si.
If the software stack is properly configured, you should obtain:

```shell
Work #0: <BandStructureWork, node_id=313436, workdir=../../../../var/folders/89/47k8wfdj11x035svqf8qnl4m0000gn/T/tmpygixwf9a/w0>, Finalized=True
  Finalized works are not shown. Use verbose > 0 to force output.

all_ok reached


Submitted on: Sat Mar 17 23:16:57 2018
Completed on: Sat Mar 17 23:17:07 2018
Elapsed time: 0:00:10.046392
Flow completed successfully

Calling flow.finalize()...

Work #0: <BandStructureWork, node_id=313436, workdir=../../../../var/folders/89/47k8wfdj11x035svqf8qnl4m0000gn/T/tmpygixwf9a/w0>, Finalized=True
  Finalized works are not shown. Use verbose > 0 to force output.

all_ok reached


Test flow completed successfully
```

Great, if you've reached this part it means that you've installed AbiPy and Abinit on your machine!
We can finally start to run the scripts in this repo or use one of the AbiPy script to analyze  the results.

Select one of the directory with a lesson_*.py script e.g. sigeph/lesson_sigeph.py.
Read the corresponding README.md file. Then look at the python script and use:

    lesson_sigeph.py

to run the flow automatically or 

    lesson_sigeph.py --help

to get the list of supported options.

TIP:

All the AbiPy scripts start with the `abi` prefix. 
Just type:

    abi + <TAB> 
    
in the shell to get the list of possible scripts.
Please consult the [AbiPy documentation](http://abinit.github.io/abipy/index.html) for further details.
