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

importlib.reload(GPF)
importlib.reload(GPC)

class Test_latlon2dlatdlon(unittest.TestCase):

    def setUp(self):
        self.verbose = 1
        
    def test_series(self):
        """
        Except for "from Excel", the dlat and dlon were calculated using this function. An error indicates that the calculation changed, not that the result is wrong. 
        """
        tests = [
            # From the Excel
            {"lat": 53.2835083, "lon": 6.30388, "latR": 53.28375, "lonR": 6.3024917, "dlat": -26.8157, "dlon": 92.3955, "description": "From the Excel"},
            
            # systematic
            {"lat": 52.0, "lon": 0, "latR": 50, "lonR": 0, "dlat": 221847, "dlon": 0, "description": "Point is north of reference"},
            {"lat": 52.0, "lon": 3, "latR": 52, "lonR": 1, "dlat": 0, "dlon": 137042, "description": "Point is east of reference"},
            {"lat": 1, "lon": 0, "latR": -1, "lonR": 0, "dlat": 221847, "dlon": 0, "description": "Point is north of reference, equator"},
            {"lat": 52.0, "lon": 1, "latR": 52, "lonR": -1, "dlat": 0, "dlon": 137042, "description": "Point is east of reference, meridian"},
            
            # switch lat with latR and lon with lonR
            {"lat": 50.0, "lon": 0, "latR": 52, "lonR": 0, "dlat": -221847, "dlon": 0, "description": "Point is south of reference"},
            {"lat": 52.0, "lon": 1, "latR": 52, "lonR": 3, "dlat": 0, "dlon": -137042, "description": "Point is west of reference"},
            {"lat": -1, "lon": 0, "latR": 1, "lonR": 0, "dlat": -221847, "dlon": 0, "description": "Point is south of reference, equator"},
            {"lat": 52.0, "lon": -1, "latR": 52, "lonR": 1, "dlat": 0, "dlon": -137042, "description": "Point is west of reference, meridian"},         
            
            # {"lat": , "lon": , "latR": , "lonR": , "dlat": , "dlon": , "description": ""},
            # {"lat": , "lon": , "latR": , "lonR": , "dlat": , "dlon": , "description": ""},
        ]

        for test in tests:
            with self.subTest(test["description"]):   
        
                dlat, dlon = GPF.latlon2dlatdlon(lat = test["lat"], lon = test["lon"], latR = test["latR"], lonR = test["lonR"], verbose = self.verbose)
            # print(dlat, dlon)
            self.assertTrue(numpy.allclose(dlat, test["dlat"]))
            self.assertTrue(numpy.allclose(dlon, test["dlon"]))
            
    def test_with_ndarray(self):
        """
        Same as test_with_series, but with ndarray.
        
        dlat and dlon were calculated using this function. An error indicates that the calculation changed, not that the result is wrong. 
        """
        lat = numpy.array([52.0,52.0,1,52.0])
        lon = numpy.array([0,3,0,1])
        latR = numpy.array([50,52,-1,52])
        lonR = numpy.array([0,1,0,-1])
        
        dlat_expected = numpy.array([221847,0,221847,0])
        dlon_expected = numpy.array([0,137042,0,137042])

        dlat, dlon = GPF.latlon2dlatdlon(lat, lon, latR, lonR, verbose = self.verbose)

        self.assertTrue(numpy.allclose(dlat, dlat_expected))
        self.assertTrue(numpy.allclose(dlon, dlon_expected))


    def test_with_ndarray_with_fixed_reference(self):
        """
        Reference as a fixed number, point as an ndarray. 
        
        dlat and dlon were calculated using this function. An error indicates that the calculation changed, not that the result is wrong. 
        """
        lat = numpy.array([52.0, 52.1, 52.2, 52.3])
        lon = numpy.array([1,1.1,1.2,1.3])
        latR = 51
        lonR = 1.15

        dlat_expected = numpy.array([110940.61952501, 122033.38036911, 133125.76947837, 144217.75306344] )
        dlon_expected = numpy.array([-10280.25654684, -3419.09534988, 3411.42462282, 10211.22014353])

        dlat, dlon = GPF.latlon2dlatdlon(lat, lon, latR, lonR, verbose = self.verbose)

        self.assertTrue(numpy.allclose(dlat, dlat_expected))
        self.assertTrue(numpy.allclose(dlon, dlon_expected))

    def test_with_ndarray_with_fixed_reference_opposite(self):
        """
        Point as a fixed number, reference as an ndarray. 
        
        The dlat has the opposite sign. dlon has different values, because it is a trapezium. 
        
        dlat and dlon were calculated using this function. An error indicates that the calculation changed, not that the result is wrong. 
        """
        latR = numpy.array([52.0, 52.1, 52.2, 52.3])
        lonR = numpy.array([1,1.1,1.2,1.3])
        lat = 51
        lon = 1.15

        dlat_expected = numpy.array([-110940.61952501, -122033.38036911, -133125.76947837, -144217.75306344] )
        # dlon_expected = numpy.array([10280.25654684, 3419.09534988, -3411.42462282, -10211.22014353])
        dlon_expected = numpy.array([10508.33181779, 3502.78082929, -3502.78082929, -10508.33181779])
        
        dlat, dlon = GPF.latlon2dlatdlon(lat, lon, latR, lonR, verbose = self.verbose)
        # print(dlat, dlon)
        self.assertTrue(numpy.allclose(dlat, dlat_expected))
        self.assertTrue(numpy.allclose(dlon, dlon_expected))


    def test_with_list(self):
        """
        As test_with_ndarray, but with a list. 
        """ 
        lat = [52.0,52.0,1,52.0]
        lon = [0,3,0,1]
        latR = [50,52,-1,52]
        lonR = [0,1,0,-1]
        
        dlat_expected = numpy.array([221847,0,221847,0])
        dlon_expected = numpy.array([0,137042,0,137042])

        dlat, dlon = GPF.latlon2dlatdlon(lat, lon, latR, lonR, verbose = self.verbose)

        self.assertTrue(numpy.allclose(dlat, dlat_expected))
        self.assertTrue(numpy.allclose(dlon, dlon_expected))

    def test_factor_as_argument_from_gpc(self):

        lat = numpy.array([52.0,52.0,1,52.0])
        lon = numpy.array([0,3,0,1])
        latR = numpy.array([50,52,-1,52])
        lonR = numpy.array([0,1,0,-1])
        
        dlat_expected = numpy.array([221847,0,221847,0])
        dlon_expected = numpy.array([0,137042,0,137042])
    
        # latlon2dxdy_lon_conversion_factor = 6378137
        # latlon2dxdy_lat_conversion_factor = 6356752
        
        dlat, dlon = GPF.latlon2dlatdlon(lat, lon, latR, lonR, verbose = self.verbose, latlon2dxdy_lon_conversion_factor = GPC.latlon2dxdy_lon_conversion_factor, latlon2dxdy_lat_conversion_factor = GPC.latlon2dxdy_lat_conversion_factor)

        self.assertTrue(numpy.allclose(dlat, dlat_expected))
        self.assertTrue(numpy.allclose(dlon, dlon_expected))
        
    def test_factor_as_argument_AS_gpc(self):

        lat = numpy.array([52.0,52.0,1,52.0])
        lon = numpy.array([0,3,0,1])
        latR = numpy.array([50,52,-1,52])
        lonR = numpy.array([0,1,0,-1])
        
        dlat_expected = numpy.array([221847,0,221847,0])
        dlon_expected = numpy.array([0,137042,0,137042])
    
        latlon2dxdy_lat_conversion_factor = 6356752
        latlon2dxdy_lon_conversion_factor = 6378137
        
        dlat, dlon = GPF.latlon2dlatdlon(lat, lon, latR, lonR, verbose = self.verbose, latlon2dxdy_lon_conversion_factor = latlon2dxdy_lon_conversion_factor, latlon2dxdy_lat_conversion_factor = latlon2dxdy_lat_conversion_factor)

        self.assertTrue(numpy.allclose(dlat, dlat_expected))
        self.assertTrue(numpy.allclose(dlon, dlon_expected))


    def test_factor_as_argument_NON_gpc(self):

        lat = numpy.array([52.0,52.0,1,52.0])
        lon = numpy.array([0,3,0,1])
        latR = numpy.array([50,52,-1,52])
        lonR = numpy.array([0,1,0,-1])
        
        dlat_expected = numpy.array([221847,0,221847,0])
        dlon_expected = numpy.array([0,137042,0,137042])
    
        latlon2dxdy_lat_conversion_factor = 6378137 + 1000
        latlon2dxdy_lon_conversion_factor = 6356752 + 1000
        
        dlat, dlon = GPF.latlon2dlatdlon(lat, lon, latR, lonR, verbose = self.verbose, latlon2dxdy_lon_conversion_factor = latlon2dxdy_lon_conversion_factor, latlon2dxdy_lat_conversion_factor = latlon2dxdy_lat_conversion_factor)

        self.assertFalse(numpy.allclose(dlat, dlat_expected))
        self.assertFalse(numpy.allclose(dlon, dlon_expected))



class Test_dlatdlon2dxdy(unittest.TestCase):

    def setUp(self):
        self.verbose = 1
        
    def test_series(self):
        tests = [
            # {"dlatS": , "dlonS": , "dlatM": , "dlonM": , "wind_direction": , "dx":, "dy": ,"description": ""},
            {"dlatS": 0, "dlonS": 0, "dlatM": 100, "dlonM": 0, "wind_direction": 0, "dx": -100, "dy": 0, "description": "basic (origin = source)"}, # measurement is 100 m north of source, wind is from the north
            {"dlatS": 0, "dlonS": 0, "dlatM": 100, "dlonM": 0, "wind_direction": 180, "dx": 100, "dy": 0, "description": "basic 180 (origin = source)"}, # measurement is 100 m north of source, wind is from the south
            {"dlatS": -50, "dlonS": 0, "dlatM": 50, "dlonM": 0, "wind_direction": 180, "dx": 100, "dy": 0, "description": "basic 180  (origin = in between source and measurement)"}, # measurement is 100 m north of source, wind is from the south. Origin is in the middle.
            {"dlatS": -100, "dlonS": 0, "dlatM": 0, "dlonM": 0, "wind_direction": 180, "dx": 100, "dy": 0, "description": "basic 180 (origin = measurement)"}, # measurement is 100 m north of source, wind is from the north. Origin is the measurement
            {"dlatS": 0, "dlonS": 0, "dlatM": 0, "dlonM": 100, "wind_direction": 270, "dx": 100, "dy": 0, "description": "basic (origin = source), east"}, # measurement is 100 m east of the source. Wind is from the west. 
            {"dlatS": 0, "dlonS": 0, "dlatM": 100, "dlonM": 100, "wind_direction": 225, "dx": numpy.sqrt(20000), "dy": 0, "description": "45 degrees"}, # measurement is 100 m north 100 m east of the source. Wind is from the south west. 
            {"dlatS": 0, "dlonS": 0, "dlatM": 100, "dlonM": 0, "wind_direction": 270, "dx": 0, "dy": 100, "description": "Wind perpendicular to line source - measurement"}, # Wind perpendicular to line source - measurement
            
            
            # {"dlatS": , "dlonS": , "dlatM": , "dlonM": , "wind_direction": , "dx":, "dy": , "description": ""},
            
            # {"dlatS": , "dlonS": , "dlatM": , "dlonM": , "wind_direction": , "dx":, "dy": , "description": ""},
        
        ]
        
        for test in tests:
            with self.subTest(test["description"]):        
                dx, dy = GPF.dlatdlon2dxdy(dlatS = test["dlatS"], dlonS = test["dlonS"], dlatM  = test["dlatM"], dlonM = test["dlonM"], wind_direction = test["wind_direction"], verbose = self.verbose)
                # print(dx, dy)
                self.assertTrue(numpy.allclose(test["dx"], dx))
                self.assertTrue(numpy.allclose(test["dy"], dy))
        
    def test_with_ndarray(self):

        dlatS = numpy.array([0,0,-50,-100, 0,0,0])
        dlonS = numpy.array([0,0,0,0, 0,0,0])
        dlatM = numpy.array([100,100,50,0, 0,100,100])
        dlonM = numpy.array([0,0,0,0, 100,100,0])
        wind_direction = numpy.array([0,180,180,180, 270,225,270])
        
        dx_expected = numpy.array([-100,100,100,100, 100, numpy.sqrt(20000),0])
        dy_expected = numpy.array([0,0,0,0, 0,0,100])
    
        dx, dy = GPF.dlatdlon2dxdy(dlatS, dlonS, dlatM, dlonM, wind_direction, verbose = self.verbose)

        self.assertTrue(numpy.allclose(dx_expected, dx))
        self.assertTrue(numpy.allclose(dy_expected, dy))




    def test_with_list(self):

        dlatS = [0,0,-50,-100, 0,0,0]
        dlonS = [0,0,0,0, 0,0,0]
        dlatM = [100,100,50,0, 0,100,100]
        dlonM = [0,0,0,0, 100,100,0]
        wind_direction = [0,180,180,180, 270,225,270]
        
        dx_expected = numpy.array([-100,100,100,100, 100, numpy.sqrt(20000),0])
        dy_expected = numpy.array([0,0,0,0, 0,0,100])
    
        dx, dy = GPF.dlatdlon2dxdy(dlatS, dlonS, dlatM, dlonM, wind_direction, verbose = self.verbose)

        self.assertTrue(numpy.allclose(dx_expected, dx))
        self.assertTrue(numpy.allclose(dy_expected, dy))

    def test_with_ndarray_with_fixed_M(self):

        dlatS = numpy.array([-50,25,0,25,100])
        dlonS = numpy.array([10,20,30,40,50])
        dlatM = 200
        dlonM = 100
        wind_direction = 0
        
        dx_expected = numpy.array([-250, -175, -200, -175, -100])
        dy_expected = numpy.array([90, 80, 70, 60, 50])
    
        dx, dy = GPF.dlatdlon2dxdy(dlatS, dlonS, dlatM, dlonM, wind_direction, verbose = self.verbose)
        
        self.assertTrue(numpy.allclose(dx_expected, dx))
        self.assertTrue(numpy.allclose(dy_expected, dy))


    def test_with_ndarray_with_fixed_S(self):

        dlatM = numpy.array([-50,25,0,25,100])
        dlonM = numpy.array([10,20,30,40,50])
        dlatS = 200
        dlonS = 100
        wind_direction = 0
        
        dx_expected = numpy.array([250, 175, 200, 175, 100])
        dy_expected = numpy.array([-90, -80, -70, -60, -50])
    
        dx, dy = GPF.dlatdlon2dxdy(dlatS, dlonS, dlatM, dlonM, wind_direction, verbose = self.verbose)
        # print(dx, dy)
        self.assertTrue(numpy.allclose(dx_expected, dx))
        self.assertTrue(numpy.allclose(dy_expected, dy))


class Test_calculate_sigma(unittest.TestCase):

    def setUp(self):
        self.verbose = 1

    def test_1(self):

        dx = 100
        z0 = 50
        Tc = 20
        ca = 0.53
        cb = -0.22
        mode = "NOGEPA"
        stability = 0
        
        sigma_y_expected = 457.8185733798507 #297.55575321823056
        sigma_z_expected = 38.11486000170984 #27.643039073928154
        
        dispersion_constants = GPF.get_dispersion_constants(mode, verbose = self.verbose)
        
        sigma_y, sigma_z = GPF.calculate_sigma(dx, z0, Tc, dispersion_constants, stability, verbose = self.verbose, ca = ca, cb = cb)
        
        # print(sigma_y, sigma_z)

        self.assertTrue(numpy.allclose(sigma_y, sigma_y_expected))
        self.assertTrue(numpy.allclose(sigma_z, sigma_z_expected))

    def test_ca_cb_from_GPC(self):

        dx = 100
        z0 = 50
        Tc = 20
        mode = "NOGEPA"
        stability = 0
        
        sigma_y_expected = 457.8185733798507 #297.55575321823056
        sigma_z_expected = 38.11486000170984 #27.643039073928154
        
        dispersion_constants = GPF.get_dispersion_constants(mode, verbose = self.verbose)
        
        sigma_y, sigma_z = GPF.calculate_sigma(dx, z0, Tc, dispersion_constants, stability, verbose = self.verbose)
        
        

        self.assertTrue(numpy.allclose(sigma_y, sigma_y_expected))
        self.assertTrue(numpy.allclose(sigma_z, sigma_z_expected))
        

class Test_calculate_concentration(unittest.TestCase):

    def setUp(self):
        self.verbose = 1

    def test_1(self):
        
        Qs = 1
        wind_speed = 1
        sigma_y = 200
        sigma_z = 10
        dy = 50 
        Zr = 5
        Hs = 5
        Hm = 500
        molecular_mass = 16
        
        c = GPF.calculate_concentration(Qs, wind_speed, sigma_y, sigma_z, dy, Zr, Hs, Hm, molecular_mass, verbose = self.verbose)
        # print(c)


    def test_function_parts(self):
        
        Qs = 1
        wind_speed = 1
        sigma_y = 1
        sigma_z = 1
        dy = 0 
        Zr = 5
        Hs = 5
        Hm = 500
        molecular_mass = 16
        
        A = Qs / (2 * numpy.pi * wind_speed * sigma_y * sigma_z)
        B = numpy.exp(-dy**2 / (2 * sigma_y**2))
        C = 2 * sigma_z**2
        D = numpy.exp(-(Zr - Hs)**2 / C)
        E = numpy.exp(-(Zr + Hs)**2 / C)
        F = numpy.exp(-(Zr - (2 * Hm - Hs))**2 / C)    
        
        # print("A: {:15.14f}".format(A))
        # print("B: {:f}".format(B))
        # print("C: {:f}".format(C))
        # print("D: {:f}".format(D))
        # print("E: {:f}".format(E))
        # print("F: {:15.14f}".format(F))
        
        c = GPF.calculate_concentration(Qs, wind_speed, sigma_y, sigma_z, dy, Zr, Hs, Hm, molecular_mass, verbose = self.verbose)
        # print(c)


        

class Test_small_functions(unittest.TestCase):

    def setUp(self):
        self.verbose = 1
        
        
    def test_calculate_Tc_1(self):
        
        tests = [
            # {"dx": , "wind_speed": , "Tc_expected": , "description": ""},
            {"dx": 100, "wind_speed": 10, "Tc_expected": 0.0027778, "description": "Basic case"},
            # {"dx": , "wind_speed": , "Tc_expected": , "description": ""},
            # {"dx": , "wind_speed": , "Tc_expected": , "description": ""},
            # {"dx": , "wind_speed": , "Tc_expected": , "description": ""},
            # {"dx": , "wind_speed": , "Tc_expected": , "description": ""},
        ]

        for test in tests:
            with self.subTest(test["description"]):              
        
                Tc = GPF.calculate_tc(test["dx"], test["wind_speed"], verbose = self.verbose)
                # print(Tc)
                self.assertTrue(numpy.allclose(test["Tc_expected"], Tc))


    def test_calculate_Tc_pandas(self):
        
        dx = numpy.arange(5) * 10 
        wind_speed = numpy.arange(5) + 1
        df = pandas.DataFrame(data = {"dx": dx, "wind_speed": wind_speed})

        Tc = GPF.calculate_tc(df["dx"], df["wind_speed"], verbose = self.verbose).to_numpy()
        
        test = numpy.array([0., 0.00138889, 0.00185185, 0.00208333, 0.00222222])

        self.assertTrue(numpy.allclose(test, Tc))
        



class Test_stability_conversion(unittest.TestCase):

    def setUp(self):
        self.verbose = 1

    def test_stability_index2class(self):
    
        tests = [
            {"i": 0, "c": "A"},
            {"i": 1, "c": "B"},
            {"i": 2, "c": "C"},
            {"i": 3, "c": "D"},
            {"i": 4, "c": "E"},
            {"i": 5, "c": "F"},
        ]
        
        for test in tests:
            description = "{:d} -> {:s}".format(test["i"], test["c"])
            with self.subTest(description):  
                c = GPF.stability_index2class(test["i"])
                self.assertTrue(c == test["c"])

    def test_stability_index2class_ndarray(self):
        i = numpy.arange(6)
        c = GPF.stability_index2class(i)
        self.assertTrue(numpy.all(c == numpy.array(["A", "B", "C", "D", "E", "F"])))

    def test_stability_index2class_index_out_of_range(self):
    
        i = 6
        with self.assertRaises(IndexError) as cm:
            c = GPF.stability_index2class(i)
        self.assertTrue(str(cm.exception) == "stability_index is 6, which is out of range, it has to be 0, 1, 2, 3, 4, or 5.")

        i = -10
        with self.assertRaises(IndexError) as cm:
            c = GPF.stability_index2class(i)
        self.assertTrue(str(cm.exception) == "stability_index is -10, which is out of range, it has to be 0, 1, 2, 3, 4, or 5.")
        
    def test_stability_index2class_ndarray_out_of_range(self):
        i = numpy.arange(-2,8)
        
        with self.assertRaises(IndexError) as cm:
            c = GPF.stability_index2class(i)
        self.assertTrue(str(cm.exception) == "stability_index is out of range, it has to be 0, 1, 2, 3, 4, or 5.")        

    def test_stability_class2index(self):
    

        tests = [
            {"i": 0, "c": "A"},
            {"i": 1, "c": "B"},
            {"i": 2, "c": "C"},
            {"i": 3, "c": "D"},
            {"i": 4, "c": "E"},
            {"i": 5, "c": "F"},
        ]
        
        for test in tests:
            description = "{:s} -> {:d}".format(test["c"], test["i"])
            with self.subTest(description):  
                i = GPF.stability_class2index(test["c"])
                # print(i)
                self.assertTrue(i == test["i"])


    def test_stability_class2index_ndarray(self):
        c = numpy.array(["D", "A", "B", "C", "A", "c"])
        i = GPF.stability_class2index(c)
        self.assertTrue(numpy.all(i == numpy.array([3,0,1,2,0,2])))

    def test_stability_class2index_list(self):
        c = ["D", "A", "B", "C", "A", "c"]
        i = GPF.stability_class2index(c)
        self.assertTrue(numpy.all(i == numpy.array([3,0,1,2,0,2])))        

    def test_stability_class2index_index_out_of_range(self):
    
        c = "X"
        with self.assertRaises(ValueError) as cm:
            i = GPF.stability_class2index(c)
        self.assertTrue(str(cm.exception) == "stability_class X does not exist")

    def test_stability_class2index_ndarray_out_of_range(self):
        c = numpy.array(["A", "x", "y", "B"])
        with self.assertRaises(ValueError) as cm:
            i = GPF.stability_class2index(c)
        self.assertTrue(str(cm.exception) == "Invalid inputs for stability_class: x y")

    def test_stability_class2index_ndarray_out_of_range_many(self):
        c = numpy.array(["A", "x", "y", "B", "C", "4", "d", "t"])
        with self.assertRaises(ValueError) as cm:
            i = GPF.stability_class2index(c)
        self.assertTrue(str(cm.exception) == "4 invalid inputs for stability_class")


class Test_get_molecule_properties(unittest.TestCase):

    def setUp(self):
        self.verbose = 1
        
    def test_get_molecule_properties(self):
        
        tests = [
            # {"molecule": "", "name_expected": "", "description": ""},
            {"molecule": "CH4", "name_expected": "methane", "description": ""},
            {"molecule": "ch4", "name_expected": "methane", "description": ""},
            {"molecule": "Ch4", "name_expected": "methane", "description": ""},
            {"molecule": "cH4", "name_expected": "methane", "description": ""},
            {"molecule": "MeThAnE", "name_expected": "methane", "description": ""},
            # {"molecule": "", "name_expected": "", "description": ""},
            # {"molecule": "", "name_expected": "", "description": ""},
            # {"molecule": "", "name_expected": "", "description": ""},
        
        ]
        for test in tests:
            with self.subTest(test["description"]): 
                res = GPF.get_molecule_properties(test["molecule"], verbose = self.verbose)
                self.assertTrue(res["name"] == test["name_expected"])

    def test_get_molecule_properties_wrong_name(self):
        
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            res = GPF.get_molecule_properties("fiets")
            self.assertTrue(res is None) 
            assert "GPConstants.molecule_properties(): fiets is not a valid name for a molecule" in str(w[-1].message)
            # print(w[-1].message)

class Test_get_dispersion_constants(unittest.TestCase):

    def setUp(self):
        self.verbose = 1

    def test_basic(self):
        dc = GPF.get_dispersion_constants(dispersion_mode = "NOGEPA", verbose = self.verbose)
        self.assertTrue(dc[0][0] == 1.36)
        self.assertTrue(len(dc) == 6)
        self.assertTrue(len(dc[0]) == 4)

    def test_lowercase(self):
        dc = GPF.get_dispersion_constants(dispersion_mode = "nogepa", verbose = self.verbose)
        self.assertTrue(dc[0][0] == 1.36)
        self.assertTrue(len(dc) == 6)
        self.assertTrue(len(dc[0]) == 4)


    def test_invalid_mode(self):
    
        test_error = "Mode fiets is invalid for dispersion_constants. Valid options are: 'farm', 'nogepa', 'sea'."
    
        with self.assertRaises(IndexError) as cm:
            dc = GPF.get_dispersion_constants(dispersion_mode = "fiets", verbose = self.verbose)
        self.assertTrue(str(cm.exception) == test_error)

        

class Test_print_vars(unittest.TestCase):

    def setUp(self):
        self.verbose = 1
    
    def funA(self, varA, verbose = 0, self_verbose = 0):
        GPF.print_vars(function_name = "funA", function_vars = vars(), verbose = verbose, self_verbose = self_verbose)

    def funB(self, varA, verbose = 0, self_verbose = 0, **kwargs):
        GPF.print_vars(function_name = "funB", function_vars = vars(), verbose = verbose, self_verbose = self_verbose)
    
    # try logging tests first
    # def test_basic(self):
        # self.funA("x", verbose = 3, self_verbose = 0)
        # self.funB("x", verbose = 3, self_verbose = 0, fiets = "A")


    def test_logging_A(self):
        test_string = "funA\n    self : test_logging_A (__main__.Test_print_vars)\n    varA : x\n    verbose : 3\n    self_verbose : 0\n"    
        with patch('sys.stdout', new_callable = StringIO) as mock_stdout:
            self.funA("x", verbose = 3, self_verbose = 0)
        self.assertTrue(mock_stdout.getvalue() == test_string)

    def test_logging_B(self):
        test_string = "funB\n    self : test_logging_B (__main__.Test_print_vars)\n    varA : x\n    verbose : 3\n    self_verbose : 0\n    kwargs:\n        fiets : A\n"
        with patch('sys.stdout', new_callable = StringIO) as mock_stdout:
            self.funB("x", verbose = 3, self_verbose = 0, fiets = "A")
            
        self.assertTrue(mock_stdout.getvalue() == test_string)        



class Test_handle_filename_path(unittest.TestCase):

    def setUp(self):
        self.verbose = 1


    def test_cases(self):
    
        out_xx = pathlib.Path('C:/path/filename.ext')
        out_x1 = pathlib.Path('C:/path/filename_1.ext')
        out_x2 = pathlib.Path('C:/path/filename_2.ext')
        out_11 = pathlib.Path('C:/path_1/filename_1.ext')
        out_12 = pathlib.Path('C:/path_1/filename_2.ext')
        out_21 = pathlib.Path('C:/path_2/filename_1.ext')
        out_22 = pathlib.Path('C:/path_2/filename_2.ext')
    
        tests = [
            {"filename": 'C:/path/filename.ext', "path": None, "output": [out_xx]},
            {"filename": ['C:/path/filename.ext'], "path": None, "output": [out_xx]},
            {"filename": 'filename.ext', "path": "C:/path", "output": [out_xx]},
            {"filename": ['C:/path/filename_1.ext', 'C:/path/filename_2.ext'], "path": None, "output": [out_x1, out_x2]},
            {"filename": ['filename_1.ext', 'filename_2.ext'], "path": 'C:/path', "output": [out_x1, out_x2]},
            {"filename": ['filename_1.ext', 'filename_2.ext'], "path": ['C:/path_1', 'C:/path_2'], "output": [out_11, out_22]},
            
            {"filename": pathlib.Path('C:/path/filename.ext'), "path": None, "output": [out_xx]},
            {"filename": [pathlib.Path('C:/path/filename.ext')], "path": None, "output": [out_xx]},
            
            {"filename": pathlib.Path('filename.ext'), "path": "C:/path", "output": [out_xx]},
            {"filename": 'filename.ext', "path": pathlib.Path("C:/path"), "output": [out_xx]},
            {"filename": pathlib.Path('filename.ext'), "path": pathlib.Path("C:/path"), "output": [out_xx]},
            
            {"filename": [pathlib.Path('C:/path/filename_1.ext'), 'C:/path/filename_2.ext'], "path": None, "output": [out_x1, out_x2]},
            {"filename": [pathlib.Path('filename_1.ext'), 'filename_2.ext'], "path": 'C:/path', "output": [out_x1, out_x2]},
            {"filename": [pathlib.Path('filename_1.ext'), 'filename_2.ext'], "path": ['C:/path_1', pathlib.Path('C:/path_2')], "output": [out_11, out_22]},            
            {"filename": None, "path": None, "output": None},
            # {"filename": , "path": , "output": },
            # {"filename": , "path": , "output": },
        ]

        for test in tests:
            with self.subTest():            
                result = GPF.handle_filename_path(filename = test["filename"], path = test["path"])
                self.assertTrue(result == test["output"])

        
    def test_different_lengths(self):
        
        filename = ['filename_1.ext', 'filename_2.ext', 'filename_3.ext']
        path = ['C:/path_1', 'C:/path_2']
        
        test_error = "Length of filename (3) and path (2) is not the same."
        
        with self.assertRaises(IndexError) as cm:
            result = GPF.handle_filename_path(filename = filename, path = path)
        self.assertTrue(str(cm.exception) == test_error)

        filename = ['filename_1.ext', 'filename_2.ext']
        path = ['C:/path_1', 'C:/path_2', 'C:/path_3']
        
        test_error = "Length of filename (2) and path (3) is not the same."
        
        with self.assertRaises(IndexError) as cm:
            result = GPF.handle_filename_path(filename = filename, path = path)
        self.assertTrue(str(cm.exception) == test_error)

    def test_type_errors(self):
        
        tests = [
            # {"filename": None, "path": None},
            {"filename": 5, "path": None},        
            {"filename": "fiets", "path": 5},
            # {"filename": , "path": },
            # {"filename": , "path": },
            # {"filename": , "path": },
            # {"filename": , "path": },
            # {"filename": , "path": },            
        ]

        for test in tests:
            with self.subTest():     
                with self.assertRaises(TypeError) as cm:
                    result = GPF.handle_filename_path(filename = test["filename"], path = test["path"])
                self.assertTrue(len(str(cm.exception)) > 0)




                
     
if __name__ == '__main__': 
    verbosity = 1
    
    if 1:
        suite = unittest.TestLoader().loadTestsFromTestCase( Test_latlon2dlatdlon)
        unittest.TextTestRunner(verbosity=verbosity).run(suite)      

    if 1:
        suite = unittest.TestLoader().loadTestsFromTestCase( Test_dlatdlon2dxdy)
        unittest.TextTestRunner(verbosity=verbosity).run(suite)    

    if 1:
        suite = unittest.TestLoader().loadTestsFromTestCase( Test_calculate_sigma)
        unittest.TextTestRunner(verbosity=verbosity).run(suite)        

    if 1:
        suite = unittest.TestLoader().loadTestsFromTestCase( Test_calculate_concentration)
        unittest.TextTestRunner(verbosity=verbosity).run(suite)  

    if 1:
        suite = unittest.TestLoader().loadTestsFromTestCase( Test_small_functions)
        unittest.TextTestRunner(verbosity=verbosity).run(suite)  

    if 1:
        suite = unittest.TestLoader().loadTestsFromTestCase( Test_stability_conversion)
        unittest.TextTestRunner(verbosity=verbosity).run(suite)  

    if 1:
        suite = unittest.TestLoader().loadTestsFromTestCase( Test_get_molecule_properties)
        unittest.TextTestRunner(verbosity=verbosity).run(suite)  
        
    if 1:
        suite = unittest.TestLoader().loadTestsFromTestCase( Test_get_dispersion_constants)
        unittest.TextTestRunner(verbosity=verbosity).run(suite)          
        
    if 1:
        suite = unittest.TestLoader().loadTestsFromTestCase( Test_print_vars )
        unittest.TextTestRunner(verbosity=verbosity).run(suite)  

    if 1:
        suite = unittest.TestLoader().loadTestsFromTestCase( Test_handle_filename_path)
        unittest.TextTestRunner(verbosity=verbosity).run(suite)               