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




class Test_basic(unittest.TestCase):

    def setUp(self):
        self.verbose = 1
        
    def test_basic(self):
        C = GPCH.Channel(channel_identifier = 0, molecule = "xyz", device_name = "abc")
        
  


        
if __name__ == '__main__': 
    verbosity = 1

    if 1:
        suite = unittest.TestLoader().loadTestsFromTestCase( Test_basic )
        unittest.TextTestRunner(verbosity=verbosity).run(suite)           