import importlib 
from io import StringIO
import pathlib
import numpy
import pandas
import unittest
from unittest.mock import patch
import warnings



import GPImportData as GPID

importlib.reload(GPID)




class Test_import_measurement_parameters_excel_helper(unittest.TestCase):

    def setUp(self):
        self.verbose = 1
        
    def test_basic(self):
        """
        Most basic functionality. 
        Roughness: NaN, D, NaN, E, F -> NaN, D, D, E, F
        Windspeed: 5, 7, 11, NaN, 16 -> 5, 7, 11, 11, 16
        """
        
        paf = pathlib.Path(r"testdata\inputfiles\configuration_1.xlsx")
        df_static, df_dynamic = GPID.import_measurement_parameters_excel_helper(paf, verbose = self.verbose)
        
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
        df_static, df_dynamic = GPID.import_measurement_parameters_excel_helper(paf, static_parameters = False, dynamic_parameters = True, verbose = self.verbose)
        self.assertTrue(df_static is None)


    def test_no_dynamic(self):
        """
        Only import static parameters, dynamic parameters should be None.
        """        
        paf = pathlib.Path(r"testdata\inputfiles\configuration_1.xlsx")
        df_static, df_dynamic = GPID.import_measurement_parameters_excel_helper(paf, static_parameters = True, dynamic_parameters = False, verbose = self.verbose)
        self.assertTrue(df_dynamic is None)        

    def test_wrong_paf(self):
        """
        paf (path and filename) points to the wrong / non-existing file. Should give a warning and return (None, None). 
        
        """
        paf = pathlib.Path(r"testdata\inputfiles\does_not_exist.xlsx")
        
        # test without the path
        test = "GPImportData.import_measurement_parameters_excel_helper(): parameter file does not exist (at this location):"
        test_length = len(test)
        
        with warnings.catch_warnings(record=True) as w:
            df_static, df_dynamic = GPID.import_measurement_parameters_excel_helper(paf, verbose = self.verbose)
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
        test = "GPImportData.import_measurement_parameters_excel_helper(): please give paf (path and filename) as pathlib path, not as string:"
        test_length = len(test)
        
        with warnings.catch_warnings(record=True) as w:
            df_static, df_dynamic = GPID.import_measurement_parameters_excel_helper(paf, verbose = self.verbose)
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
            df_static, df_dynamic = GPID.import_measurement_parameters_excel_helper(paf, static_parameters = "wrong sheet name",verbose = self.verbose)
          
        self.assertEqual(str(cm.exception), "Worksheet named 'wrong sheet name' not found")


class Test_import_measurement_parameters_excel(unittest.TestCase):

    def setUp(self):
        self.verbose = 1

    def test_basic(self):
    
        paf = [pathlib.Path(r"testdata\inputfiles\configuration_3a.xlsx"), pathlib.Path(r"testdata\inputfiles\configuration_3b.xlsx")]
    
        df_static, df_dynamic = GPID.import_measurement_parameters_excel(paf, verbose = self.verbose)
        
        # print(df_static)
        # print(df_dynamic)


    def test_static_same_data(self):
    
        paf = [pathlib.Path(r"testdata\inputfiles\configuration_3a.xlsx"), pathlib.Path(r"testdata\inputfiles\configuration_3c.xlsx")]
    
        df_static, df_dynamic = GPID.import_measurement_parameters_excel(paf, verbose = self.verbose)
        col_names = ['varA', 'varB', 'varC', 'varD', 'varE', 'varF']
        self.assertTrue(numpy.all(df_static.columns == col_names))
        self.assertTrue(df_static.shape == (1,6))
        
        
    def test_dynamic(self):
    
        paf = [pathlib.Path(r"testdata\inputfiles\configuration_3a.xlsx"), pathlib.Path(r"testdata\inputfiles\configuration_3d.xlsx")]
    
        df_static, df_dynamic = GPID.import_measurement_parameters_excel(paf, verbose = self.verbose)
        col_names = ['datetime', 'stability_class', 'wind_speed', 'varX', 'wind_direction']
        self.assertTrue(numpy.all(df_dynamic.columns == col_names))
        self.assertTrue(df_dynamic.shape == (11,5))        
        # print(df_dynamic.shape)        
        # print(df_dynamic.columns)        
         

class Test_import_measurement_data_helper(unittest.TestCase):

    def setUp(self):
        self.verbose = 1

    def test_basic(self):
        """
        Most basic case.
        """
        paf = pathlib.Path(r"testdata\inputfiles\data_peaksonly_1.csv")
        df = GPID.import_measurement_data_helper(paf, verbose = self.verbose)
        
    def test_wrong_paf(self):
        """
        paf (path and filename) points to the wrong / non-existing file. Should give a warning and return None.
        """
        paf = pathlib.Path(r"testdata\inputfiles\does_not_exist.csv")
        
        # test without the path
        test = "GPImportData.import_measurement_data_helper(): measurement file does not exist (at this location):"
        test_length = len(test)
        
        with warnings.catch_warnings(record=True) as w:
            df = GPID.import_measurement_data_helper(paf, verbose = self.verbose)
            self.assertIsNone(df)
            self.assertTrue(issubclass(w[-1].category, UserWarning))

        self.assertEqual(str(w[0].message)[:test_length], test)

    def test_paf_is_str(self):
        """
        paf is supposed to be a Pathlib Path, but for convenience it can also be a string. 
        """
        paf = r"testdata\inputfiles\data_peaksonly_1.csv"

        # test without the path
        test = "GPImportData.import_measurement_data_helper(): please give paf (path and filename) as pathlib path, not as string:"
        test_length = len(test)
        
        with warnings.catch_warnings(record=True) as w:
            df = GPID.import_measurement_data_helper(paf, verbose = self.verbose)
            self.assertTrue(issubclass(w[-1].category, UserWarning))
            self.assertIsNotNone(df)
        self.assertEqual(str(w[0].message)[:test_length], test)        
        

class Test_import_measurement_data(unittest.TestCase):

    def setUp(self):
        self.verbose = 1

    def test_basic(self):
        """
        Most basic case.
        """
        paf = [pathlib.Path(r"testdata\inputfiles\data_peaksonly_1.csv"), pathlib.Path(r"testdata\inputfiles\data_peaksonly_2.csv")]
        df = GPID.import_measurement_data(paf, verbose = self.verbose)
        self.assertTrue(numpy.all(['datetime', 'NOx', 'NO', 'NO2', 'CO2', 'PM10', 'PeakNumber'] == df.columns))
        self.assertTrue(df.shape == (2842,7))


    def test_invalid_column_name(self):
        """
        The columns of the two measurement files needs to match
        """
        paf = [pathlib.Path(r"testdata\inputfiles\data_peaksonly_1.csv"), pathlib.Path(r"testdata\inputfiles\data_peaksonly_2_invalid_columnname.csv")]
        
        with self.assertRaises(pandas.errors.InvalidIndexError) as cm:
            df = GPID.import_measurement_data(paf, verbose = self.verbose)



class Test_merge_measurement_static_dynamic_df(unittest.TestCase):

    def setUp(self):
        self.verbose = 1

    def test_basic(self):
    
        measurement_paf = [pathlib.Path(r"testdata\inputfiles\data_peaksonly_1.csv")]
        df = GPID.import_measurement_data(measurement_paf, verbose = self.verbose)

        parameter_paf = [pathlib.Path(r"testdata\inputfiles\configuration_3a.xlsx")]
        df_static, df_dynamic = GPID.import_measurement_parameters_excel(parameter_paf, verbose = self.verbose)

        df = GPID.merge_measurement_static_dynamic_df(df, df_static, df_dynamic, verbose = self.verbose)
        self.assertTrue(df.shape == (1715,12))
        
    def test_dynamic_is_None(self):
    
        measurement_paf = [pathlib.Path(r"testdata\inputfiles\data_peaksonly_1.csv")]
        df = GPID.import_measurement_data(measurement_paf, verbose = self.verbose)

        parameter_paf = [pathlib.Path(r"testdata\inputfiles\configuration_3a.xlsx")]
        df_static, df_dynamic = GPID.import_measurement_parameters_excel(parameter_paf, static_parameters = True, dynamic_parameters = False, verbose = self.verbose)

        df = GPID.merge_measurement_static_dynamic_df(df, df_static, df_dynamic, verbose = self.verbose)
        self.assertTrue(df.shape == (1715,10))
        
    def test_static_is_None(self):
    
        measurement_paf = [pathlib.Path(r"testdata\inputfiles\data_peaksonly_1.csv")]
        df = GPID.import_measurement_data(measurement_paf, verbose = self.verbose)

        parameter_paf = [pathlib.Path(r"testdata\inputfiles\configuration_3a.xlsx")]
        df_static, df_dynamic = GPID.import_measurement_parameters_excel(parameter_paf, static_parameters = False, dynamic_parameters = True, verbose = self.verbose)

        df = GPID.merge_measurement_static_dynamic_df(df, df_static, df_dynamic, verbose = self.verbose)
        self.assertTrue(df.shape == (1715,9))        
        
    def test_df_is_None(self):
    
        df = None 

        parameter_paf = [pathlib.Path(r"testdata\inputfiles\configuration_3a.xlsx")]
        df_static, df_dynamic = GPID.import_measurement_parameters_excel(parameter_paf, static_parameters = True, dynamic_parameters = True, verbose = self.verbose)

        test_string = "GPImportData.merge_measurement_static_dynamic_df(): df can not be None."

        with self.assertRaises(ValueError) as cm:
            with patch('sys.stdout', new_callable = StringIO) as mock_stdout:
                df = GPID.merge_measurement_static_dynamic_df(df, df_static, df_dynamic, verbose = self.verbose)
        
            self.assertTrue(mock_stdout.getvalue() == test_string)        
        
        
if __name__ == '__main__': 
    verbosity = 1
       
    # if 1:
        # suite = unittest.TestLoader().loadTestsFromTestCase( Test_import_measurement_parameters_excel_helper )
        # unittest.TextTestRunner(verbosity=verbosity).run(suite)        

    # if 1:
        # suite = unittest.TestLoader().loadTestsFromTestCase( Test_import_measurement_parameters_excel )
        # unittest.TextTestRunner(verbosity=verbosity).run(suite)        

    
    # if 1:
        # suite = unittest.TestLoader().loadTestsFromTestCase( Test_import_measurement_data_helper )
        # unittest.TextTestRunner(verbosity=verbosity).run(suite)     
        
        
    # if 1:
        # suite = unittest.TestLoader().loadTestsFromTestCase( Test_import_measurement_data )
        # unittest.TextTestRunner(verbosity=verbosity).run(suite)   

    if 1:
        suite = unittest.TestLoader().loadTestsFromTestCase( Test_merge_measurement_static_dynamic_df )
        unittest.TextTestRunner(verbosity=verbosity).run(suite)           