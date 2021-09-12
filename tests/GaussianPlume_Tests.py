import importlib 
from io import StringIO
import numpy
import unittest
from unittest.mock import patch
import warnings
import logging
import pathlib
import pandas

import GaussianPlume as GP
import GPFunctions as GPF
import GPConstants as GPC
import GPSource as GPSO
import GPChannel as GPCH
import GPMolecule as GPMO

importlib.reload(GP)
importlib.reload(GPF)
importlib.reload(GPC)
importlib.reload(GPSO)
importlib.reload(GPCH)
importlib.reload(GPMO)

def data(verbose = 0):

    channels = [
        GPCH.Channel(0, "ch4", "QCL", verbose = verbose),
        GPCH.Channel(1, "n2o", "MIRA", verbose = verbose),
    ]     
    
    molecules = [
        GPMO.Molecule("ch4", verbose = verbose),
        GPMO.Molecule("n2o", verbose = verbose),
    ]

    qs_ch4 = 0.125
    qs_n2o = 1.89
    hs_ch4 = 3
    hs_n2o = 1
    z0_ch4 = 0.2
    z0_n2o = 0.2
    offset_sig_ch4 = 30
    offset_sig_n2o = 20
    

    
    sources = [
        GPSO.Source(0, "ch4", latS = 51.58202, lonS = 5.59376, latR = 51.5852, lonR = 5.6015, qs = qs_ch4, hs = hs_ch4, z0 = z0_ch4, offset_sigma_z = offset_sig_ch4, label = "wc 0", verbose = verbose),
        GPSO.Source(1, "ch4", latS = 51.58187, lonS = 5.59421, latR = 51.5852, lonR = 5.6015, qs = qs_ch4, hs = hs_ch4, z0 = z0_ch4, offset_sigma_z = offset_sig_ch4, label = "koeien 1", verbose = verbose),
        GPSO.Source(2, "ch4", latS = 51.58237, lonS = 5.59402, latR = 51.5852, lonR = 5.6015, qs = qs_ch4, hs = hs_ch4, z0 = z0_ch4, offset_sigma_z = offset_sig_ch4, label = "varkens 2", verbose = verbose),
        GPSO.Source(3, "ch4", latS = 51.58272, lonS = 5.59428, latR = 51.5852, lonR = 5.6015, qs = qs_ch4, hs = hs_ch4, z0 = z0_ch4, offset_sigma_z = offset_sig_ch4, label = "kippen 3", verbose = verbose),
        GPSO.Source(4, "ch4", latS = 51.58314, lonS = 5.59454, latR = 51.5852, lonR = 5.6015, qs = qs_ch4, hs = hs_ch4, z0 = z0_ch4, offset_sigma_z = offset_sig_ch4, label = "garage 4", verbose = verbose),
        GPSO.Source(5, "ch4", latS = 51.58241, lonS = 5.59447, latR = 51.5852, lonR = 5.6015, qs = qs_ch4, hs = hs_ch4, z0 = z0_ch4, offset_sigma_z = offset_sig_ch4, label = "koeien 5", verbose = verbose),
        GPSO.Source(6, "ch4", latS = 51.58277, lonS = 5.59480, latR = 51.5852, lonR = 5.6015, qs = qs_ch4, hs = hs_ch4, z0 = z0_ch4, offset_sigma_z = offset_sig_ch4, label = "varkens 6", verbose = verbose),
        GPSO.Source(7, "ch4", latS = 51.58203, lonS = 5.59447, latR = 51.5852, lonR = 5.6015, qs = qs_ch4, hs = hs_ch4, z0 = z0_ch4, offset_sigma_z = offset_sig_ch4, label = "kippen 7", verbose = verbose),
        GPSO.Source(8, "n2o", latS = 51.58222, lonS = 5.59577, latR = 51.5852, lonR = 5.6015, qs = qs_n2o, hs = hs_n2o, z0 = z0_n2o, offset_sigma_z = offset_sig_n2o, label = "garage 8", verbose = verbose),
    ]
    
    # print(sources[0])
    
    return channels, sources, molecules



class Test_init(unittest.TestCase):

    def setUp(self):
        self.verbose = 1
        self.channels, self.sources, self.molecules = data()
        
    def test_basic(self):
        S = GP.GaussianPlume()
        
    def test_set_channels(self):
        
        channels = [
            GPCH.Channel(0, "ch4", "QCL"),
            GPCH.Channel(1, "n2o", "MIRA"),
        ]    
        S = GP.GaussianPlume(channels = channels)        

    def test_set_molecules(self):
        ch4 = GPMO.Molecule("ch4")
        n2o = GPMO.Molecule("n2o")
        molecules = [ch4, n2o]
        S = GP.GaussianPlume(molecules = molecules)   

    def test_comment(self):

        S = GP.GaussianPlume(comment = "boo")   
        print(S.log["comment"])



        




        
        

class Test_import_data_from_Excel(unittest.TestCase):

    def setUp(self):
        self.verbose = 1
        self.channels, self.sources, self.molecules = data()


        
        
    def test_import_measurement_data_Excel(self):
    
        S = GP.GaussianPlume(channels = self.channels, molecules = self.molecules, sources = self.sources, dispersion_mode  = "farm", verbose = self.verbose)
        sheetname = "data 3"
        filename = r"C:\Python\GaussianPlume\tests\testdata\inputfiles\testdata_20200925-1.xlsx"

        S.import_measurement_data_from_Excel(sheetname = sheetname, filename = filename, verbose = self.verbose)
        print(S.df.shape)
        
    def test_import_measurement_data_Excel_drop_non_plume(self):
    
        S = GP.GaussianPlume(channels = self.channels, molecules = self.molecules, sources = self.sources, dispersion_mode  = "farm", verbose = self.verbose)
        sheetname = "data 3"
        filename = r"C:\Python\GaussianPlume\tests\testdata\inputfiles\testdata_20200925-1.xlsx"

        S.import_measurement_data_from_Excel(sheetname = sheetname, filename = filename, verbose = self.verbose, drop_non_plume = True)    

        print(S.df.shape)

           
    def test_import_source_data_Excel(self):

        S = GP.GaussianPlume(channels = self.channels, molecules = self.molecules, dispersion_mode  = "farm", verbose = self.verbose)
        sheetname = "sources"
        filename = r"C:\Python\GaussianPlume\tests\testdata\inputfiles\testdata_20200925-1.xlsx"
        S.import_sources_from_Excel(sheetname = sheetname, filename = filename, verbose = self.verbose)
    
    def test_import_channel_data(self):
        S = GP.GaussianPlume(molecules = self.molecules, dispersion_mode  = "farm", verbose = self.verbose)
        sheetname = "channels"
        filename = r"C:\Python\GaussianPlume\tests\testdata\inputfiles\testdata_20200925-1.xlsx"
        S.import_channels_from_Excel(sheetname = sheetname, filename = filename, verbose = self.verbose)        


    def test_import_static_parameters(self):
        
        S = GP.GaussianPlume(verbose = self.verbose)
        sheetname = "static parameters"
        filename = r"C:\Python\GaussianPlume\tests\testdata\inputfiles\testdata_20200925-3.xlsx"
        S.import_static_parameters(sheetname, filename = filename, verbose = self.verbose)
        print(S)
        



class Test_parse_data(unittest.TestCase):

    def setUp(self):
        self.verbose = 1
        self.channels, self.sources, self.molecules = data()

    def test_source_dxdy_None(self):
        S = GP.GaussianPlume(sources = self.sources, verbose = self.verbose)
        
        source = self.sources[0]
        source_index = 0
        S.parse_dx_dy(source_index, source, verbose = self.verbose)
        
        self.assertIsNone(S.sources[0].dx)
        self.assertIsNone(S.sources[0].dy)
        
    def test_source_dxdy_set_manually(self):
        
        S = GP.GaussianPlume(sources = self.sources, verbose = self.verbose)
        S.sources[0].dx = 1
        S.sources[0].dy = 2
        source = self.sources[0]
        source_index = 0
        S.parse_dx_dy(source_index, source, verbose = self.verbose)
        self.assertEqual(S.sources[0].dx, 1)
        self.assertEqual(S.sources[0].dy, 2)
        
    def test_source_dxdy_from_df_SX(self):
        temp = {
            "dxS0": numpy.arange(10),
            "dyS0": numpy.arange(10)+10,
        }
        df = pandas.DataFrame(temp)
        S = GP.GaussianPlume(sources = self.sources, verbose = self.verbose, df = df)
 
        source = self.sources[0]
        source_index = 0
        S.parse_dx_dy(source_index, source, verbose = self.verbose)
        self.assertTrue(numpy.allclose(S.sources[0].dx, temp["dxS0"]))
        self.assertTrue(numpy.allclose(S.sources[0].dy, temp["dyS0"]))

    def test_source_dxdy_from_source_df(self):
        temp = {
            "source_id": numpy.arange(9),
            "dx": numpy.arange(9)+10,
            "dy": numpy.arange(9)+20,
        }
        df_sources = pandas.DataFrame(temp)
        S = GP.GaussianPlume(df_sources = df_sources, verbose = self.verbose, sources = self.sources)
 
        source = self.sources[0]
        source_index = 0
        S.parse_dx_dy(source_index, source, verbose = self.verbose)
        self.assertTrue(numpy.isclose(S.sources[0].dx, 10))
        self.assertTrue(numpy.isclose(S.sources[0].dy, 20))

    def test_source_dxdy_from_df_S(self):
        temp = {
            "dxS": numpy.arange(10),
            "dyS": numpy.arange(10)+10,
        }
        df = pandas.DataFrame(temp)
        S = GP.GaussianPlume(sources = self.sources, verbose = self.verbose, df = df)
 
        source = self.sources[0]
        source_index = 0
        S.parse_dx_dy(source_index, source, verbose = self.verbose)
        self.assertTrue(numpy.allclose(S.sources[0].dx, temp["dxS"]))
        self.assertTrue(numpy.allclose(S.sources[0].dy, temp["dyS"]))
        

    def test_source_dxdy_set_manually_preference_above_df_SX(self):
        temp = {
            "dxS0": numpy.arange(10),
            "dyS0": numpy.arange(10)+10,
        }
        df = pandas.DataFrame(temp)
        
        S = GP.GaussianPlume(sources = self.sources, verbose = self.verbose, df = df)
        S.sources[0].dx = 1
        S.sources[0].dy = 2
        source = self.sources[0]
        source_index = 0
        S.parse_dx_dy(source_index, source, verbose = self.verbose)
        self.assertEqual(S.sources[0].dx, 1)
        self.assertEqual(S.sources[0].dy, 2)


    def test_source_dxdy_from_df_SX_above_source_df(self):
        df_temp = {
            "dxS0": numpy.arange(10),
            "dyS0": numpy.arange(10)+10,
        }
        df = pandas.DataFrame(df_temp)
        source_temp = {
            "source_id": numpy.arange(9),
            "dx": numpy.arange(9)+100,
            "dy": numpy.arange(9)+200,
        }
        df_sources = pandas.DataFrame(source_temp)        
        S = GP.GaussianPlume(sources = self.sources, verbose = self.verbose, df = df)
 
        source = self.sources[0]
        source_index = 0
        S.parse_dx_dy(source_index, source, verbose = self.verbose)
        self.assertTrue(numpy.allclose(S.sources[0].dx, df_temp["dxS0"]))
        self.assertTrue(numpy.allclose(S.sources[0].dy, df_temp["dyS0"]))
    

    def test_source_dxdy_from_source_df_above_df_S(self):
        df_temp = {
            "dxS": numpy.arange(10),
            "dyS": numpy.arange(10)+10,
        }
        df = pandas.DataFrame(df_temp)    
        source_temp = {
            "source_id": numpy.arange(9),
            "dx": numpy.arange(9)+100,
            "dy": numpy.arange(9)+200,
        }
        df_sources = pandas.DataFrame(source_temp)  
        S = GP.GaussianPlume(df_sources = df_sources, verbose = self.verbose, sources = self.sources, df = df)
 
        source = self.sources[0]
        source_index = 0
        S.parse_dx_dy(source_index, source, verbose = self.verbose)
        self.assertTrue(numpy.isclose(S.sources[0].dx, 100))
        self.assertTrue(numpy.isclose(S.sources[0].dy, 200))



    def test_dlat_dlon_1(self):
    
        S = GP.GaussianPlume(sources = self.sources, verbose = self.verbose)
        
        source = self.sources[0]
        source_index = 0
        out = S.parse_dlat_dlon(source_index, source, verbose = self.verbose)
        
        self.assertIsNone(S.sources[0].dlatS)
        self.assertIsNone(S.sources[0].dlonS)    
        
        self.assertFalse(out[0])
        self.assertFalse(out[1])


    def test_dlat_dlon_set_manually(self):
    
        S = GP.GaussianPlume(sources = self.sources, verbose = self.verbose)
        
        source = self.sources[0]
        source_index = 0
        
        S.sources[0].dlatS = 1
        S.sources[0].dlonS = 2
        
        out = S.parse_dlat_dlon(source_index, source, verbose = self.verbose)
        
        self.assertTrue(S.sources[0].dlatS == 1)
        self.assertTrue(S.sources[0].dlonS == 2)    
        
        self.assertTrue(out[0])
        self.assertFalse(out[1])


        S.sources[0].dlatM = 3
        S.sources[0].dlonM = 4
        
        out = S.parse_dlat_dlon(source_index, source, verbose = self.verbose)
        
        self.assertTrue(S.sources[0].dlatM == 3)
        self.assertTrue(S.sources[0].dlonM == 4)    
        
        self.assertTrue(out[0])
        self.assertTrue(out[1])


    def test_parse_wind(self):
        temp = {
            "wind_direction": numpy.arange(10),
            "wind_speed": numpy.arange(10)+10,
        }
        df = pandas.DataFrame(temp)
        S = GP.GaussianPlume(sources = self.sources, verbose = self.verbose, df = df)
 
        source = self.sources[0]
        source_index = 0
        S.parse_wind(source_index, source, verbose = self.verbose)
        self.assertTrue(numpy.allclose(S.sources[0].wind_direction, temp["wind_direction"]))
        self.assertTrue(numpy.allclose(S.sources[0].wind_speed, temp["wind_speed"]))


class Test_calculate_concentration(unittest.TestCase):

    def setUp(self):
        self.verbose = 1
        self.channels, self.sources, self.molecules = data()


    def test_integration(self):
        S = GP.GaussianPlume(verbose = self.verbose)
        paf = r"C:\Python\GaussianPlume\tests\testdata\inputfiles\testdata_20200925-3.xlsx"
        
        S.import_static_parameters(filename = paf)
        S.import_sources_from_Excel(filename = paf)
        S.import_channels_from_Excel(filename = paf)
        
        paf = r"C:\Python\GaussianPlume\tests\testdata\inputfiles\testdata_20200925-3_data.csv"
        S.import_measurement_data_from_csv(filename = paf)
        
        S.parse_data()
        # for source in S.sources:
            # print(source.dispersion_mode)
        # print(S.sources[0])
        S.calculate_concentration()
        
        
if __name__ == '__main__': 
    verbosity = 1
    
    # if 1:
        # suite = unittest.TestLoader().loadTestsFromTestCase( Test_init)
        # unittest.TextTestRunner(verbosity=verbosity).run(suite)             


 

    # if 1:
        # suite = unittest.TestLoader().loadTestsFromTestCase( Test_import_data_from_Excel)
        # unittest.TextTestRunner(verbosity=verbosity).run(suite)   


    # if 1:
        # suite = unittest.TestLoader().loadTestsFromTestCase( Test_parse_data)
        # unittest.TextTestRunner(verbosity=verbosity).run(suite)           

    if 1:
        suite = unittest.TestLoader().loadTestsFromTestCase( Test_calculate_concentration)
        unittest.TextTestRunner(verbosity=verbosity).run(suite)          