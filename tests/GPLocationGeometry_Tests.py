import importlib 
from io import StringIO
import pathlib
import numpy
import pandas
import unittest
from unittest.mock import patch
import warnings



import GPLocationGeometry as GPLG

importlib.reload(GPLG)




class Test_basic(unittest.TestCase):

    def setUp(self):
        self.verbose = 1
        
    def test_basic_location(self):
        L = GPLG.Location(1,2)
        
  
    def test_basic_geometry(self):
        G = GPLG.Geometry()

        
if __name__ == '__main__': 
    verbosity = 1

    if 1:
        suite = unittest.TestLoader().loadTestsFromTestCase( Test_basic )
        unittest.TextTestRunner(verbosity=verbosity).run(suite)           