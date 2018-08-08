# HOWTO add a new jupyter notebook.

This is a quick howto for developer who want to add a new notebook to `abitutorials`.
We distinguish between to kind of notebooks:

   1. notebooks documenting the python API and the usage of netcdf files
   2. notebooks with lessons showing how to run calculations and 
      analyze the results.
       
In the first category we have, for instance, the `structure.ipynb` notebook or the `GSR.nc` notebook. 
These notebooks are usually placed in the top-level directory of the package.

Notebooks with lessons, on the other hand, are usually located is sub-directories
and are accompanied by a python script that provides the objects/functions required 
to execute the calculation.

Adding a new notebook of type 1 is easy. Just:

   1. Use the template provided in `template.ipynb`
   2. Add a links to the new notebook in `index.ipynb`
   
Adding a new lessons (type 2) requires some extra work.

   1. Create a new directory for the lesson e.g. `foo`
   2. Use `template.ipynb` as template and rename it (e.g. `foo/lesson_foo.ipynb`)
   3. Add a python script `foo/lesson_foo.py`
   


