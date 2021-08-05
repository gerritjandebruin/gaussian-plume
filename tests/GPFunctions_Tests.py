import importlib 
import numpy
import unittest
import warnings

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
        
        sigma_y, sigma_z = GPF.calculate_sigma(dx, z0, Tc, ca, cb, dispersion_constants, stability, verbose = self.verbose)
        
        print(sigma_y, sigma_z)

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
        print(c)


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
        
        print("A: {:15.14f}".format(A))
        print("B: {:f}".format(B))
        print("C: {:f}".format(C))
        print("D: {:f}".format(D))
        print("E: {:f}".format(E))
        print("F: {:15.14f}".format(F))
        
        c = GPF.calculate_concentration(Qs, wind_speed, sigma_y, sigma_z, dy, Zr, Hs, Hm, molecular_mass, verbose = self.verbose)
        print(c)


        

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
        
                Tc = GPF.calculate_Tc(test["dx"], test["wind_speed"], verbose = self.verbose)
                # print(Tc)
                self.assertTrue(numpy.allclose(test["Tc_expected"], Tc))


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
            assert "Molecule is not implemented" in str(w[-1].message)
            # print(w[-1].message)

class Test_get_dispersion_constants(unittest.TestCase):

    def setUp(self):
        self.verbose = 1

    def test_basic(self):
        dc = GPF.get_dispersion_constants(mode = "NOGEPA", verbose = self.verbose)
        self.assertTrue(dc[0][0] == 1.36)
        self.assertTrue(len(dc) == 6)
        self.assertTrue(len(dc[0]) == 4)
        


     
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
        suite = unittest.TestLoader().loadTestsFromTestCase( Test_get_molecule_properties)
        unittest.TextTestRunner(verbosity=verbosity).run(suite)  
        
    if 1:
        suite = unittest.TestLoader().loadTestsFromTestCase( Test_get_dispersion_constants)
        unittest.TextTestRunner(verbosity=verbosity).run(suite)          
        


        