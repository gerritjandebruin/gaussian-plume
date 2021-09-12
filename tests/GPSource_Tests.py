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

importlib.reload(GPF)
importlib.reload(GPC)
importlib.reload(GPSO)

class Test_init(unittest.TestCase):

    def setUp(self):
        self.verbose = 1
        
    def test_basic(self):
        S = GPSO.Source(source_id = 0, molecule = "ch4", verbose = self.verbose)
        print(S)
        self.assertEqual(S.label, "0 methane")
        
        
    def test_set_dx(self):
        dx = numpy.arange(3)
        S = GPSO.Source(0, "ch4", dx = dx)
        self.assertTrue(numpy.all(S.dx == dx))
        

    def test_set_df(self):
        dx = numpy.arange(1,7)
        dy = numpy.arange(2,8)
        df = {
            "dx": dx,
            "dy": dy,
        }
        df = pandas.DataFrame(df)
        S = GPSO.Source(0, "ch4", df = df)
        self.assertTrue(numpy.all(S.dx == dx))     
        
    def test_set_df_and_dx(self):
        dx1 = numpy.arange(1,7)
        dx2 = numpy.arange(3,9)
        dy = numpy.arange(2,8)
        df = {
            "dx": dx1,
            "dy": dy,
        }
        df = pandas.DataFrame(df)
        S = GPSO.Source(0, "ch4", df = df, dx = dx2)
        self.assertTrue(numpy.all(S.dx == dx2))             
        
if __name__ == '__main__': 
    verbosity = 1
    
    if 1:
        suite = unittest.TestLoader().loadTestsFromTestCase( Test_init)
        unittest.TextTestRunner(verbosity=verbosity).run(suite)             
        