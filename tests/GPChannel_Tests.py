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
import GPChannel as GPCH

importlib.reload(GPF)
importlib.reload(GPC)
importlib.reload(GPCH)

class Test_init(unittest.TestCase):

    def setUp(self):
        self.verbose = 1
        
    def test_basic(self):
        C = GPCH.Channel(0, "ch4", "QCL")
        self.assertEqual(C.label, "0 methane QCL")
          


class Test_get_concentration_for_plume(unittest.TestCase):

    def setUp(self):
        self.verbose = 1

        C = GPCH.Channel(0, "ch4", "QCL")
        C.concentration_model = numpy.zeros((100,4))
        for i in range(4):
            C.concentration_model[:,i] = numpy.arange(100) + 100 * i
        
        C.plume_number = numpy.zeros(100)
        C.plume_number[:] = numpy.nan
        C.plume_number[10:20] = 1
        C.plume_number[40:60] = 2
        C.plume_number[70] = 3    

        self.C = C
        
    def test_plume_idx_source_idx_cumu_False(self):
        plume = 1
        source_index = 1
        cumulative = False
        test = numpy.arange(110,120)
        conc = self.C.get_concentration_for_plume(plume, model = True, source_index = source_index, cumulative = cumulative, verbose = self.verbose)
        self.assertTrue(numpy.allclose(conc, test))

    def test_plume_idx_source_idx_cumu_True(self):
        plume = 1
        source_index = 1
        cumulative = True
        test = numpy.sum(numpy.arange(110,120))
        conc = self.C.get_concentration_for_plume(plume, model = True, source_index = source_index, cumulative = cumulative, verbose = self.verbose)
        self.assertTrue(conc == test)        
        

    def test_plume_idx_source_None_cumu_False(self):
        plume = 1
        source_index = None
        cumulative = False
        
        test = numpy.zeros((10,4))
        for i in range(4):
            test[:,i] = numpy.arange(10,20) + 100 * i        
        
        conc = self.C.get_concentration_for_plume(plume, model = True, source_index = source_index, cumulative = cumulative, verbose = self.verbose)
        self.assertTrue(numpy.allclose(conc, test))

    def test_plume_idx_source_None_cumu_True(self):
        plume = 1
        source_index = None
        cumulative = True
        
        test = numpy.zeros((10,4))
        for i in range(4):
            test[:,i] = numpy.arange(10,20) + 100 * i        
        test = numpy.sum(test)
        conc = self.C.get_concentration_for_plume(plume, model = True, source_index = source_index, cumulative = cumulative, verbose = self.verbose)
        self.assertTrue(conc == test)

    def test_plume_ndarray_source_idx_cumu_False(self):
        plume = numpy.array([1,2])
        source_index = 1
        cumulative = False
        test = numpy.concatenate((numpy.arange(110,120), numpy.arange(140,160)))
        conc = self.C.get_concentration_for_plume(plume, model = True, source_index = source_index, cumulative = cumulative, verbose = self.verbose)
        self.assertTrue(numpy.allclose(conc, test))


    def test_plume_list_source_idx_cumu_False(self):
        plume = [1,2]
        source_index = 1
        cumulative = False
        test = numpy.concatenate((numpy.arange(110,120), numpy.arange(140,160)))
        conc = self.C.get_concentration_for_plume(plume, model = True, source_index = source_index, cumulative = cumulative, verbose = self.verbose)
        self.assertTrue(numpy.allclose(conc, test))

    def test_plume_ndarray_source_idx_cumu_True(self):
        plume = numpy.array([1,2])
        source_index = 1
        cumulative = True
        test = numpy.sum(numpy.concatenate((numpy.arange(110,120), numpy.arange(140,160))))
        conc = self.C.get_concentration_for_plume(plume, model = True, source_index = source_index, cumulative = cumulative, verbose = self.verbose)
        self.assertTrue(conc == test)

    def test_plume_idx_source_ndarray_cumu_False(self):
        plume = 1
        source_index = numpy.array([1,2])
        cumulative = False
        test = numpy.zeros((10,2))
        for i in range(2):
            test[:,i] = numpy.arange(10,20) + 100 * (i+1)
        conc = self.C.get_concentration_for_plume(plume, model = True, source_index = source_index, cumulative = cumulative, verbose = self.verbose)
        self.assertTrue(numpy.allclose(conc, test))

    def test_plume_idx_source_ndarray_cumu_True(self):
        plume = 1
        source_index = numpy.array([1,2])
        cumulative = True
        test = numpy.zeros((10,2))
        for i in range(2):
            test[:,i] = numpy.arange(10,20) + 100 * (i+1)
        test = numpy.sum(test)
        conc = self.C.get_concentration_for_plume(plume, model = True, source_index = source_index, cumulative = cumulative, verbose = self.verbose)
        self.assertTrue(conc == test)
        
if __name__ == '__main__': 
    verbosity = 1
    
    if 1:
        suite = unittest.TestLoader().loadTestsFromTestCase( Test_init)
        unittest.TextTestRunner(verbosity=verbosity).run(suite)             


    if 1:
        suite = unittest.TestLoader().loadTestsFromTestCase( Test_get_concentration_for_plume)
        unittest.TextTestRunner(verbosity=verbosity).run(suite)       
        