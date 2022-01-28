import importlib 
from io import StringIO
import numpy
import unittest
from unittest.mock import patch
import warnings
import logging
import pathlib
import pandas

import GPImportData as GPID

importlib.reload(GPID)

class Test_basic(unittest.TestCase):

    def setUp(self):
        self.verbose = 1
        
    def test_basic(self):

        paf = pathlib.Path(r"C:\Python\GaussianPlume\tests\testdata\inputfiles\testdata_20200925-3.xlsx")
        GPID.import_measurement_data(paf)
          

        
if __name__ == '__main__': 
    verbosity = 1
    
    if 1:
        suite = unittest.TestLoader().loadTestsFromTestCase( Test_basic)
        unittest.TextTestRunner(verbosity=verbosity).run(suite)     