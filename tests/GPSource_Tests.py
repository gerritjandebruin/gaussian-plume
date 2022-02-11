import importlib 
from io import StringIO
import numpy
import unittest
from unittest.mock import patch
import warnings
import logging
import pathlib
import pandas

import GPFunctions as GPF
import GPConstants as GPC
import GPSource as GPSO
import GPMolecule as GPMO

importlib.reload(GPF)
importlib.reload(GPC)
importlib.reload(GPSO)
importlib.reload(GPMO)

class Test_init(unittest.TestCase):

    def setUp(self):
        self.verbose = 1
        
    def test_basic(self):
        S = GPSO.Source(source_id = 0, molecule = "ch4", verbose = self.verbose)
        # print(S)
        self.assertEqual(S.label, "0 methane")


    def test_init_id_is_number(self):
        S = GPSO.Source(source_id = 0, verbose = self.verbose)
        self.assertEqual(S.label, "0")

    def test_init_id_is_string(self):
        S = GPSO.Source(source_id = "fiets", verbose = self.verbose)
        self.assertEqual(S.label, "fiets")        

    def test_init_molecule_is_string(self):
        S = GPSO.Source(source_id = 0, molecule = "ch4", verbose = self.verbose)
        self.assertEqual(S.label, "0 methane")  

    def test_init_molecule_is_object(self):
        molecule = GPMO.Molecule("ch4", verbose = self.verbose)
        S = GPSO.Source(source_id = 0, molecule = molecule, verbose = self.verbose)
        self.assertEqual(S.label, "0 methane")  

    def test_init_molecule_wrong_string(self):
        with self.assertRaises(ValueError) as cm:
            S = GPSO.Source(source_id = 0, molecule = "fiets", verbose = self.verbose)
        self.assertEqual(str(cm.exception), "GPConstants.molecule_properties(): fiets is not a valid name for a molecule")

    def test_init_molecule_is_none(self):
        S = GPSO.Source(source_id = 0, molecule = None, verbose = self.verbose)
        self.assertEqual(S.label, "0")  
        self.assertIsNone(S.molecule)
        
    def test_set_dx(self):
        dx = numpy.arange(3)
        S = GPSO.Source(0, "ch4", dx = dx)
        self.assertTrue(numpy.all(S.dx == dx))
        

           
        
if __name__ == '__main__': 
    verbosity = 1
    
    if 1:
        suite = unittest.TestLoader().loadTestsFromTestCase( Test_init)
        unittest.TextTestRunner(verbosity=verbosity).run(suite)             
        