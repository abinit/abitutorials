"""Tests for jupyter notebooks"""
from __future__ import print_function, division, unicode_literals, absolute_import

import sys
import os

#pack_dir, x = os.path.split(os.path.abspath(__file__))
#pack_dir, x = os.path.split(pack_dir)
#sys.path.insert(0, pack_dir)

from glob import glob
from monty.os.path import find_exts
from abipy.core.testing import AbipyTest

# Put any notebooks to be excluded here
EXCLUDE_NBS = {
}

#module_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)))

EXPECTED_ERRORS = {
    #"lessons/python_primer/5 - Lists.ipynb": 2, # Exception examples
    #"lessons/python_primer/8 - Writing Functions.ipynb": 1, # Fill in example
}

class NotebookTest(AbipyTest):

    def setUp(self):
        # Get all ipynb files
        top = os.path.dirname(os.path.abspath(__file__))
        top = os.path.abspath(os.path.join(top, ".."))
        nbpaths = find_exts(top, ".ipynb", exclude_dirs=".ipynb_checkpoints")
        # Basenames must be unique.
        assert len(nbpaths) == len(set([os.path.basename(p) for p in nbpaths]))
        #nb_paths = [path for path in nbpaths
        #                 if not any([path.startswith(e) for e in EXCLUDE_NBS])]
        self.nb_paths = sorted(nbpaths)
        print("top", top)
        print("nbpaths", self.nb_paths)
        #raise ValueError()

    def test_notebooks(self):
        """Testing jupyter notebooks"""
        for i, path in enumerate(self.nb_paths):
            print("Building notebook:", path)
            nb, errors = self.run_nbpath(path)
            #nb, errors = self.run_nbpath(os.path.join(module_dir, path))
            #expected_errors = EXPECTED_ERRORS.get(path, 0)
            #self.assertEqual(len(errors), expected_errors,
            #                 msg="Errors in nb {} found: {}".format(path, errors))
            assert errors == []
            if i == 1: break
