import importlib 
from io import StringIO
import pathlib
import numpy
import pandas
import unittest
from unittest.mock import patch
import warnings



import GPChannel as GPCH

importlib.reload(GPCH)




class Test_XXX(unittest.TestCase):

    def setUp(self):
        self.verbose = 1
        
    def test_basic(self):
        pass
        
  


        
if __name__ == '__main__': 
    verbosity = 1

    if 1:
        suite = unittest.TestLoader().loadTestsFromTestCase( Test_XXX )
        unittest.TextTestRunner(verbosity=verbosity).run(suite)           