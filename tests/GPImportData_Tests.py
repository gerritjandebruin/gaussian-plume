import importlib 
import pathlib
import numpy
import pandas
import unittest
import warnings



import GPImportMeasurementParameters as GPIMP

importlib.reload(GPIMP)

class Test_import_measurement_parameters_txt(unittest.TestCase):

    def setUp(self):
        self.verbose = 1
        
    def test_basic(self):
        
        paf = pathlib.Path(r"C:\Python\GaussianPlume\tests\testdata\inputfiles\configuration_1.txt")
        # print(paf)
        GPIMP.import_measurement_parameters_txt(paf)


class Test_import_measurement_parameters_excel(unittest.TestCase):

    def setUp(self):
        self.verbose = 1
        
    def test_basic(self):
        
        paf = pathlib.Path(r"C:\Python\GaussianPlume\tests\testdata\inputfiles\configuration_1.xlsx")
        df_static, df_dynamic = GPIMP.import_measurement_parameters_excel(paf, verbose = self.verbose)
        
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
        
        paf = pathlib.Path(r"C:\Python\GaussianPlume\tests\testdata\inputfiles\configuration_1.xlsx")
        df_static, df_dynamic = GPIMP.import_measurement_parameters_excel(paf, static_parameters = False, dynamic_parameters = True, verbose = self.verbose)
        self.assertTrue(df_static is None)


    def test_no_dynamic(self):
        
        paf = pathlib.Path(r"C:\Python\GaussianPlume\tests\testdata\inputfiles\configuration_1.xlsx")
        df_static, df_dynamic = GPIMP.import_measurement_parameters_excel(paf, static_parameters = True, dynamic_parameters = False, verbose = self.verbose)
        self.assertTrue(df_dynamic is None)        

    def test_wrong_paf(self):
        
        paf = pathlib.Path(r"C:\Python\GaussianPlume\tests\testdata\inputfiles\does_not_exist.xlsx")
        
        # test without the path
        test = "GPImportMeasurementParameters.import_measurement_parameters_excel(): parameter file does not exist (at this location):"
        test_length = len(test)
        
        with warnings.catch_warnings(record=True) as w:
            df_static, df_dynamic = GPIMP.import_measurement_parameters_excel(paf, verbose = self.verbose)
            self.assertTrue(issubclass(w[-1].category, UserWarning))

        self.assertEqual(str(w[0].message)[:test_length], test)
        
    def test_wrong_sheetname(self):
        
        paf = pathlib.Path(r"C:\Python\GaussianPlume\tests\testdata\inputfiles\configuration_1.xlsx")
        
        
        with self.assertRaises(ValueError) as cm:
            df_static, df_dynamic = GPIMP.import_measurement_parameters_excel(paf, static_parameters = "wrong sheet name",verbose = self.verbose)
        self.assertEqual(str(cm.exception), "Worksheet named 'wrong sheet name' not found")
        
        
if __name__ == '__main__': 
    verbosity = 1
    
    if 0:
        suite = unittest.TestLoader().loadTestsFromTestCase( Test_import_measurement_parameters_txt )
        unittest.TextTestRunner(verbosity=verbosity).run(suite)            

    if 1:
        suite = unittest.TestLoader().loadTestsFromTestCase( Test_import_measurement_parameters_excel )
        unittest.TextTestRunner(verbosity=verbosity).run(suite)          