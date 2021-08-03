import importlib 
import pathlib
import numpy
import unittest
import warnings

import GPImportMeasurementParameters as GPIMP

importlib.reload(GPIMP)

class Test_import_measurement_parameters(unittest.TestCase):

    def setUp(self):
        self.verbose = 1
        
    def test_basic(self):
        
        paf = pathlib.Path(r"C:\Python\GaussianPlume\tests\testdata\inputfiles\configuration_1.txt")
        print(paf)
        GPIMP.import_measurement_parameters(paf)
        
if __name__ == '__main__': 
    verbosity = 1
    
    if 1:
        suite = unittest.TestLoader().loadTestsFromTestCase( Test_import_measurement_parameters)
        unittest.TextTestRunner(verbosity=verbosity).run(suite)            