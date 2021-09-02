import importlib 
import pathlib
import numpy
import pandas
import unittest
import warnings



import GaussianPlume as GP

import GPPlumeModel as GPPM
import GPSource as GPSO
import GPChannel as GPCH
import GPLocationGeometry as GPLG
import GPMolecule as GPM
import GPConstants as GPC

importlib.reload(GPC)
importlib.reload(GP)
importlib.reload(GPSO)
importlib.reload(GPCH)
importlib.reload(GPLG)
importlib.reload(GPM)





class Test_general_operation(unittest.TestCase):

    def setUp(self):
        self.verbose = 1


    def test_basic(self):
        
        locR = GPLG.Location(51.5852, 5.6015)
        locS0 = GPLG.Location(51.5775117, 5.58756835)
        locS1 = GPLG.Location(51.5775117, 5.68756835)
        locS2 = GPLG.Location(51.5775117, 5.78756835)

        ch4 = GPM.Molecule("ch4")
        no2 = GPM.Molecule("no2")
        molecules = [ch4, no2]
        
        source0 = GPSO.Source(0, ch4, locS = locS0, label = "wc", verbose = self.verbose)
        source1 = GPSO.Source(1, no2, locS = locS1, label = "stal", verbose = self.verbose)
        source2 = GPSO.Source(2, [no2, ch4], locS = locS2, label = "schuur", verbose = self.verbose)
        sources = [source0, source1, source2]

        channel0 = GPCH.Channel(0, no2, "QCL")
        channel1 = GPCH.Channel(1, ch4, "MIRA")
        channels = [channel0, channel1]

        locM = numpy.loadtxt(r"C:\Python\GaussianPlume\tests\testdata\inputfiles\locM.dat")
        locM = GPLG.Location(locM[:,1], locM[:,0])
        plume_number = numpy.zeros(110)
        plume_number[30:50] = 1
        plume_number[80:100] = 2
        df = {
            "channel0 ppb": numpy.arange(110)/10,
            "channel1 ppb": numpy.arange(110)/20,
            "wind_speed": numpy.arange(100,210),
            "wind_direction": numpy.arange(200,310),
            "plume_number": plume_number,
            "locM": locM,
        }
        df = pandas.DataFrame(df)

        plume0 = GPPM.Plume(df = df)
        plumes = [plume0]
        
        G = GP.GaussianPlume()
        
        G.sources = sources
        G.channels = channels
        G.molecules = molecules
        G.plumes = plumes



    def test_data(self):
    
        locR = GPLG.Location(51.5852, 5.6015, verbose = self.verbose)
        
        locS0 = GPLG.Location(51.58202, 5.59376, verbose = self.verbose)
        locS1 = GPLG.Location(51.58187, 5.59421, verbose = self.verbose)
        locS2 = GPLG.Location(51.58237, 5.59402, verbose = self.verbose)
        locS3 = GPLG.Location(51.58272, 5.59428, verbose = self.verbose)
        locS4 = GPLG.Location(51.58314, 5.59454, verbose = self.verbose)
        locS5 = GPLG.Location(51.58241, 5.59447, verbose = self.verbose)
        locS6 = GPLG.Location(51.58277, 5.5948,  verbose = self.verbose)
        locS7 = GPLG.Location(51.58203, 5.59447, verbose = self.verbose)
        locS8 = GPLG.Location(51.58222, 5.59577, verbose = self.verbose)

        ch4 = GPM.Molecule("ch4")
        n2o = GPM.Molecule("n2o")
        molecules = [ch4, n2o]
        
        qs_ch4 = 0.125
        qs_n2o = 1.89
        hs_ch4 = 3
        hs_n2o = 1
        z0_ch4 = 0.2
        z0_n2o = 0.2
        offset_sig_ch4 = 30
        offset_sig_n2o = 20
        
    
        sources = [
            GPSO.Source(0, "ch4", locS = locS0, locR = locR, qs = qs_ch4, hs = hs_ch4, z0 = z0_ch4, offset_sigma_z = offset_sig_ch4, label = "wc 0", verbose = self.verbose),
            GPSO.Source(1, "ch4", locS = locS1, locR = locR, qs = qs_ch4, hs = hs_ch4, z0 = z0_ch4, offset_sigma_z = offset_sig_ch4, label = "koeien 1", verbose = self.verbose),
            GPSO.Source(2, "ch4", locS = locS2, locR = locR, qs = qs_ch4, hs = hs_ch4, z0 = z0_ch4, offset_sigma_z = offset_sig_ch4, label = "varkens 2", verbose = self.verbose),
            GPSO.Source(3, "ch4", locS = locS3, locR = locR, qs = qs_ch4, hs = hs_ch4, z0 = z0_ch4, offset_sigma_z = offset_sig_ch4, label = "kippen 3", verbose = self.verbose),
            GPSO.Source(4, "ch4", locS = locS4, locR = locR, qs = qs_ch4, hs = hs_ch4, z0 = z0_ch4, offset_sigma_z = offset_sig_ch4, label = "garage 4", verbose = self.verbose),
            GPSO.Source(5, "ch4", locS = locS5, locR = locR, qs = qs_ch4, hs = hs_ch4, z0 = z0_ch4, offset_sigma_z = offset_sig_ch4, label = "koeien 5", verbose = self.verbose),
            GPSO.Source(6, "ch4", locS = locS6, locR = locR, qs = qs_ch4, hs = hs_ch4, z0 = z0_ch4, offset_sigma_z = offset_sig_ch4, label = "varkens 6", verbose = self.verbose),
            GPSO.Source(7, "ch4", locS = locS7, locR = locR, qs = qs_ch4, hs = hs_ch4, z0 = z0_ch4, offset_sigma_z = offset_sig_ch4, label = "kippen 7", verbose = self.verbose),
            GPSO.Source(8, "n2o", locS = locS8, locR = locR, qs = qs_n2o, hs = hs_n2o, z0 = z0_n2o, offset_sigma_z = offset_sig_n2o, label = "garage 8", verbose = self.verbose),
        ]
        
        channels = [
            GPCH.Channel(0, "ch4", "QCL"),
            GPCH.Channel(1, "n2o", "MIRA"),
        ]

        paf = r"C:\Python\GaussianPlume\tests\testdata\inputfiles\testdata_20200925-1.xlsx"
        with open(paf, "rb") as F:
            sheetname = "data 2"
            df = pandas.read_excel(F, sheetname)
        # print(df)
        plumes = []
        plume_numbers = df.loc[:,"plume_number"].to_numpy()
        for plume_index in range(1,8):
            idx = numpy.where(plume_numbers == plume_index)[0]
            new_df = df.iloc[idx, :]
            plumes.append(GPPM.Plume(df = new_df))
            
        
        
        
        # plumes = [GPPM.Plume(df = df)]
        
        
        G = GP.GaussianPlume()

        G.sources = sources
        G.channels = channels
        G.molecules = molecules
        G.plumes = plumes

        
        
        
        
        # G.locM = locM
        G.locR = locR
        
        
        G.calculate_plume()
        
        
        
        
        
        # =SIN((B6-$F$4)*2*PI()/360)*6356752
        # =COS((B6)*2*PI()/360)*6378137*SIN((C6-$G$4)*2*PI()/360)
        
        
        # GPLG.Geometry(
# 1: N2O 1.89g/s;z0=0.2;Offsig=10
# 6:CH4 1/s; 2 bron; z0=0.2;Offsig=30

        
        
    # def dlatdlon2latlon(self):
        # """
        # This converts back from an incorrect calculation in Excel
        # """
        # dlat = -4572005
        # dlon = 4564700
        
        # latR = 51.5852
        # lonR = 5.6015


        # lon = 5.58756835
        # lat = 51.5775117

        
        # lon_calculated = numpy.arcsin(dlat / GPC.latlon2dxdy_lat_conversion_factor) / GPC.deg2rad + latR
        
        # a = dlon / (GPC.latlon2dxdy_lon_conversion_factor * numpy.cos(lon_calculated * GPC.deg2rad))
        # lat_calculated = numpy.arcsin(a) / GPC.deg2rad + lonR
        
        
        # print(lon_calculated, lat_calculated)


# -4572005	4564700
# -4571970	4564685
# -4571985	4564725
# -4571965	4564750
# -4571945	4564780
# -4571950	4564725 # 5.59447
# -4571925	4564750
# -4571950	4564695
# -4571850	4564700







                
        
if __name__ == '__main__': 
    verbosity = 1
       
       

    if 1:
        suite = unittest.TestLoader().loadTestsFromTestCase( Test_general_operation )
        unittest.TextTestRunner(verbosity=verbosity).run(suite)                     