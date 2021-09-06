import importlib 
from io import StringIO
import pathlib
import numpy
import pandas
import unittest
from unittest.mock import patch
import warnings



import GPSource as GPSO

importlib.reload(GPSO)




class Test_basic(unittest.TestCase):

    def setUp(self):
        self.verbose = 1
        
    def test_basic(self):
        GPSO.Source(source_identifier = 0, molecules = "no2")
        
  


        
if __name__ == '__main__': 
    verbosity = 1

    if 1:
        suite = unittest.TestLoader().loadTestsFromTestCase( Test_basic )
        unittest.TextTestRunner(verbosity=verbosity).run(suite)           