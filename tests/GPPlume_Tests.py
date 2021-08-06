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
        P = GPP.Plume(verbose = 0)
        
    def test_stability_setter_getter(self):
        
        stability_index = numpy.array([4,3,1])
        
        P = GPP.Plume(verbose = 0, stability_index = stability_index)
        
        print(P.stability_class)
        
        
if __name__ == '__main__': 
    verbosity = 1
       
    if 1:
        suite = unittest.TestLoader().loadTestsFromTestCase( Test_basic )
        unittest.TextTestRunner(verbosity=verbosity).run(suite)        
