import importlib 
from io import StringIO
import pathlib
import numpy
import pandas
import unittest
from unittest.mock import patch
import warnings



import GPMolecule as GPMO

importlib.reload(GPMO)




class Test_basic(unittest.TestCase):

    def setUp(self):
        self.verbose = 1
        
    def test_basic(self):
        M = GPMO.Molecule("ch4")
        
    def test_invalid_molecule_name(self):
    
        with self.assertRaises(ValueError) as cm:
            M = GPMO.Molecule("abc") 
          
        self.assertEqual(str(cm.exception), "GPMolecule.Molecule.__init__(): abc is not a valid name of a molecule.")    
         
        
        
       


        
if __name__ == '__main__': 
    verbosity = 1

    if 1:
        suite = unittest.TestLoader().loadTestsFromTestCase( Test_basic )
        unittest.TextTestRunner(verbosity=verbosity).run(suite)           