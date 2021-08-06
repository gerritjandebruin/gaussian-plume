import importlib 
import pathlib
import numpy
import pandas
import unittest
import warnings



import GaussianPlume as GP


importlib.reload(GP)




class Test_basic(unittest.TestCase):

    def setUp(self):
        self.verbose = 1
        
    def test_basic(self):
        """
        Most basic functionality. 

        """
        G = GP.GaussianPlume(verbose = self.verbose)
        


class Test_add_parameter_files(unittest.TestCase):

    def setUp(self):
        self.verbose = 1

    def test_basic(self):
        
        path_and_filenames = ["a", "b", "c"]
        
        G = GP.GaussianPlume(verbose = self.verbose)
        G.add_parameter_files(path_and_filenames)
        self.assertTrue(len(G.plumes) == 3)


    def test_add_single_file(self):
        
        path_and_filenames = "a"
        
        G = GP.GaussianPlume(verbose = self.verbose)
        G.add_parameter_files(path_and_filenames)
        self.assertTrue(len(G.plumes) == 1)
        
class Test_pickling(unittest.TestCase):

    def setUp(self):
        self.verbose = 1
        
        self.pickle_path = pathlib.Path(r"C:\Python\GaussianPlume\tests\testdata\inputfiles\tempfiles")
        
        if self.pickle_path.exists() == False:
            self.pickle_path.mkdir()        
        
    def tearDown(self):      
        pass

    def test_save_load_plume(self):
        """
        Make some plumes, save a single plume. Then load the plume. It will be added to the plumes. 
        
        """
        path_and_filenames = ["a", "b", "c"]
        
        G = GP.GaussianPlume(verbose = self.verbose)
        G.add_parameter_files(path_and_filenames)    

        for i in range(len(path_and_filenames)):
            G.plumes[i].windspeed = i

        pickle_filename = "tempfile_test_pickling_test_save_load_plume.pickle"
        plume_index = 1

        G.save_plume(pickle_path = self.pickle_path, pickle_filename = pickle_filename, plume_index = plume_index)
        
        G.load_plume(pickle_path = self.pickle_path, pickle_filename = pickle_filename)
        self.assertTrue(len(G.plumes) == 4)
        self.assertTrue(G.plumes[3].windspeed == 1)

        # set the original object to a high windspeed, then check if the re-imported object has the original (low) windspeed
        G.plumes[1].windspeed = 100
        self.assertTrue(G.plumes[3].windspeed == 1)
        self.assertTrue(G.plumes[1].windspeed == 100)

        # remove the pickle
        pickle_paf = self.pickle_path.joinpath(pickle_filename)
        pickle_paf.unlink()


    def test_save_load_plumes(self):
        """
        Make some plumes, save a all plumes. Then load the plumes, replacing the current plumes
        
        """
        path_and_filenames = ["a", "b", "c"]
        
        G = GP.GaussianPlume(verbose = self.verbose)
        G.add_parameter_files(path_and_filenames)    

        for i in range(len(path_and_filenames)):
            G.plumes[i].windspeed = i

        pickle_filename = "tempfile_test_pickling_test_save_load_plumes.pickle"

        G.save_plumes(pickle_path = self.pickle_path, pickle_filename = pickle_filename)

        # change the windspeeds of the objects in memory
        for i in range(len(path_and_filenames)):
            G.plumes[i].windspeed = i + 10
        
        # import plumes, objects in memory are discarded
        G.load_plumes(pickle_path = self.pickle_path, pickle_filename = pickle_filename, append_to_plumes = False)
        
        # check for the original windspeeds 
        self.assertTrue(len(G.plumes) == 3)
        self.assertTrue(G.plumes[1].windspeed == 1)

        # remove the pickle
        pickle_paf = self.pickle_path.joinpath(pickle_filename)
        pickle_paf.unlink()


    def test_save_load_plumes_append(self):
        """
        Make some plumes, save a all plumes. Then load the plumes, appending to the current plumes
        
        """
        path_and_filenames = ["a", "b", "c"]
        
        G = GP.GaussianPlume(verbose = self.verbose)
        G.add_parameter_files(path_and_filenames)    

        for i in range(len(path_and_filenames)):
            G.plumes[i].windspeed = i

        pickle_filename = "tempfile_test_pickling_test_save_load_plumes_append.pickle"

        G.save_plumes(pickle_path = self.pickle_path, pickle_filename = pickle_filename)

        # change the windspeeds of the objects in memory
        for i in range(len(path_and_filenames)):
            G.plumes[i].windspeed = i + 10
        
        # import plumes, objects in memory are discarded
        G.load_plumes(pickle_path = self.pickle_path, pickle_filename = pickle_filename, append_to_plumes = True)
        print(G.plumes)
        # check for the original windspeeds 
        self.assertTrue(len(G.plumes) == 6)
        self.assertTrue(G.plumes[1].windspeed == 11)
        self.assertTrue(G.plumes[4].windspeed == 1)

        # remove the pickle
        pickle_paf = self.pickle_path.joinpath(pickle_filename)
        pickle_paf.unlink()


    def test_save_load_plumes_to_new_GP(self):
        """
        Make some plumes, save a all plumes. Then make a new GaussianPlume object and load the plumes. 
        
        """
        path_and_filenames = ["a", "b", "c"]
        
        G = GP.GaussianPlume(verbose = self.verbose)
        G.add_parameter_files(path_and_filenames)    

        for i in range(len(path_and_filenames)):
            G.plumes[i].windspeed = i

        pickle_filename = "tempfile_test_pickling_test_save_load_plumes_append.pickle"

        G.save_plumes(pickle_path = self.pickle_path, pickle_filename = pickle_filename)
        G = None
        
        P = GP.GaussianPlume(verbose = self.verbose)
        
        # import plumes to P
        P.load_plumes(pickle_path = self.pickle_path, pickle_filename = pickle_filename, append_to_plumes = True)
        print(P.plumes)
        # check for the original windspeeds 
        self.assertTrue(len(G.plumes) == 6)
        self.assertTrue(G.plumes[1].windspeed == 11)
        self.assertTrue(G.plumes[4].windspeed == 1)

        # remove the pickle
        pickle_paf = self.pickle_path.joinpath(pickle_filename)
        pickle_paf.unlink()

        
        
if __name__ == '__main__': 
    verbosity = 1
       
    if 1:
        suite = unittest.TestLoader().loadTestsFromTestCase( Test_basic )
        unittest.TextTestRunner(verbosity=verbosity).run(suite)        

    if 1:
        suite = unittest.TestLoader().loadTestsFromTestCase( Test_add_parameter_files )
        unittest.TextTestRunner(verbosity=verbosity).run(suite)        

    if 1:
        suite = unittest.TestLoader().loadTestsFromTestCase( Test_pickling )
        unittest.TextTestRunner(verbosity=verbosity).run(suite)      