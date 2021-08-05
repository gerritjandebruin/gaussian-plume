import importlib 
import pathlib
import numpy
import pandas
import unittest
import warnings



import GPImportData as GPID
import GPPlume as GPP

importlib.reload(GPID)
importlib.reload(GPP)



class Test_basic(unittest.TestCase):

    def setUp(self):
        self.verbose = 1
        
    def test_basic(self):
        """
        Most basic functionality. 

        """
        P = GPP.Plume()
        
        
if __name__ == '__main__': 
    verbosity = 1
       
    if 1:
        suite = unittest.TestLoader().loadTestsFromTestCase( Test_basic )
        unittest.TextTestRunner(verbosity=verbosity).run(suite)        
