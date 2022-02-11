import importlib 
from io import StringIO
import numpy
import unittest
from unittest.mock import patch
import warnings
import logging
import pathlib
import pandas

import GPMolecule as GPMO

importlib.reload(GPMO)

class Test_basic(unittest.TestCase):

    def setUp(self):
        self.verbose = 1
        
    def test_basic(self):

        molecule = GPMO.Molecule("ch4", verbose = self.verbose)
        self.assertEqual(molecule.name, "methane") 


class Test_error_handling(unittest.TestCase):          

    def setUp(self):
        self.verbose = 1
    
    def test_wrong_name_invalid_default(self):
        with self.assertRaises(ValueError) as cm:
            with warnings.catch_warnings(record=True) as w:
                molecule = GPMO.Molecule("fiets", verbose = self.verbose)
        self.assertEqual(str(cm.exception), "GPConstants.molecule_properties(): fiets is not a valid name for a molecule")        
     
    def test_name_is_none(self):
        with self.assertRaises(ValueError) as cm:
            with warnings.catch_warnings(record=True) as w:
                molecule = GPMO.Molecule(None, verbose = self.verbose)
        self.assertEqual(str(cm.exception), "GPConstants.molecule_properties(): None is not a valid name for a molecule")        
        

        
        
        
if __name__ == '__main__': 
    verbosity = 1
    
    if 1:
        suite = unittest.TestLoader().loadTestsFromTestCase( Test_basic)
        unittest.TextTestRunner(verbosity=verbosity).run(suite)  
    if 1:
        suite = unittest.TestLoader().loadTestsFromTestCase( Test_error_handling)
        unittest.TextTestRunner(verbosity=verbosity).run(suite)          