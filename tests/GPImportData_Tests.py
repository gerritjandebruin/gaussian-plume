import importlib 
import pathlib
import numpy
import pandas
import unittest
import warnings



import GPImportData as GPID

importlib.reload(GPID)




class Test_import_measurement_parameters_excel(unittest.TestCase):

    def setUp(self):
        self.verbose = 1
        
    def test_basic(self):
        """
        Most basic functionality. 
        Roughness: NaN, D, NaN, E, F -> NaN, D, D, E, F
        Windspeed: 5, 7, 11, NaN, 16 -> 5, 7, 11, 11, 16
        """
        
        paf = pathlib.Path(r"testdata\inputfiles\configuration_1.xlsx")
        df_static, df_dynamic = GPID.import_measurement_parameters_excel(paf, verbose = self.verbose)
        
        # empty parameter was removed
        self.assertFalse("var C" in df_static.columns)

        # first row is NaN
        self.assertTrue(pandas.isna(df_dynamic.loc[0,"roughness"]))
        self.assertFalse(pandas.isna(df_dynamic.loc[1,"roughness"]))
        self.assertFalse(pandas.isna(df_dynamic.loc[2,"roughness"]))
        self.assertTrue(numpy.all(df_dynamic.loc[1:,"roughness"] == ["D", "D", "E", "F"]))

        self.assertFalse(pandas.isna(df_dynamic.loc[2,"windspeed"]))
        self.assertFalse(pandas.isna(df_dynamic.loc[3,"windspeed"]))
        self.assertTrue(numpy.all(df_dynamic.loc[:,"windspeed"] == [5,7,11,11,16]))

    def test_no_static(self):
        """
        Only import dynamic parameters, static parameters should be None.
        """
        paf = pathlib.Path(r"C:\Python\GaussianPlume\tests\testdata\inputfiles\configuration_1.xlsx")
        df_static, df_dynamic = GPID.import_measurement_parameters_excel(paf, static_parameters = False, dynamic_parameters = True, verbose = self.verbose)
        self.assertTrue(df_static is None)


    def test_no_dynamic(self):
        """
        Only import static parameters, dynamic parameters should be None.
        """        
        paf = pathlib.Path(r"testdata\inputfiles\configuration_1.xlsx")
        df_static, df_dynamic = GPID.import_measurement_parameters_excel(paf, static_parameters = True, dynamic_parameters = False, verbose = self.verbose)
        self.assertTrue(df_dynamic is None)        

    def test_wrong_paf(self):
        """
        paf (path and filename) points to the wrong / non-existing file. Should give a warning and return (None, None). 
        
        """
        paf = pathlib.Path(r"testdata\inputfiles\does_not_exist.xlsx")
        
        # test without the path
        test = "GPImportData.import_measurement_parameters_excel(): parameter file does not exist (at this location):"
        test_length = len(test)
        
        with warnings.catch_warnings(record=True) as w:
            df_static, df_dynamic = GPID.import_measurement_parameters_excel(paf, verbose = self.verbose)
            self.assertIsNone(df_static)
            self.assertIsNone(df_dynamic)              
            self.assertTrue(issubclass(w[-1].category, UserWarning))

        self.assertEqual(str(w[0].message)[:test_length], test)

    def test_paf_is_str(self):
        """
        paf is supposed to be a Pathlib Path, but for convenience it can also be a string. 
        """
        paf = r"testdata\inputfiles\configuration_1.xlsx"

        # test without the path
        test = "GPImportData.import_measurement_parameters_excel(): please give paf (path and filename) as pathlib path, not as string:"
        test_length = len(test)
        
        with warnings.catch_warnings(record=True) as w:
            df_static, df_dynamic = GPID.import_measurement_parameters_excel(paf, verbose = self.verbose)
            self.assertIsNotNone(df_static)
            self.assertIsNotNone(df_dynamic)
            self.assertTrue(issubclass(w[-1].category, UserWarning))

        self.assertEqual(str(w[0].message)[:test_length], test)

        
    def test_wrong_sheetname(self):
        """
        If the sheet name is wrong, Pandas will raise an error. 
        """
        paf = pathlib.Path(r"testdata\inputfiles\configuration_1.xlsx")
        
        
        with self.assertRaises(ValueError) as cm:
            df_static, df_dynamic = GPID.import_measurement_parameters_excel(paf, static_parameters = "wrong sheet name",verbose = self.verbose)
          
        self.assertEqual(str(cm.exception), "Worksheet named 'wrong sheet name' not found")


class Test_import_measurement_data(unittest.TestCase):

    def setUp(self):
        self.verbose = 1

    def test_basic(self):
        """
        Most basic case.
        """
        paf = pathlib.Path(r"testdata\inputfiles\data_peaksonly_1.csv")
        df = GPID.import_measurement_data(paf, verbose = self.verbose)
        
    def test_wrong_paf(self):
        """
        paf (path and filename) points to the wrong / non-existing file. Should give a warning and return None.
        """
        paf = pathlib.Path(r"testdata\inputfiles\does_not_exist.csv")
        
        # test without the path
        test = "GPImportData.import_measurement_data(): measurement file does not exist (at this location):"
        test_length = len(test)
        
        with warnings.catch_warnings(record=True) as w:
            df = GPID.import_measurement_data(paf, verbose = self.verbose)
            self.assertIsNone(df)
            self.assertTrue(issubclass(w[-1].category, UserWarning))

        self.assertEqual(str(w[0].message)[:test_length], test)

    def test_paf_is_str(self):
        """
        paf is supposed to be a Pathlib Path, but for convenience it can also be a string. 
        """
        paf = r"testdata\inputfiles\data_peaksonly_1.csv"

        # test without the path
        test = "GPImportData.import_measurement_data(): please give paf (path and filename) as pathlib path, not as string:"
        test_length = len(test)
        
        with warnings.catch_warnings(record=True) as w:
            df = GPID.import_measurement_data(paf, verbose = self.verbose)
            self.assertTrue(issubclass(w[-1].category, UserWarning))
            self.assertIsNotNone(df)
        self.assertEqual(str(w[0].message)[:test_length], test)        
        
        
if __name__ == '__main__': 
    verbosity = 1
       
    if 0:
        suite = unittest.TestLoader().loadTestsFromTestCase( Test_import_measurement_parameters_excel )
        unittest.TextTestRunner(verbosity=verbosity).run(suite)        

    
    if 1:
        suite = unittest.TestLoader().loadTestsFromTestCase( Test_import_measurement_data )
        unittest.TextTestRunner(verbosity=verbosity).run(suite)     
        