"""



"""

import importlib
import pickle

import GPFunctions as GPF
import GPPlumeModel as GPPM
import PythonTools.ClassTools as CT

importlib.reload(GPF)
importlib.reload(GPPM)


class GaussianPlume(CT.ClassTools):
    """
    
    
    """


    def __init__(self, verbose = 0, **kwargs):
        """

     
        
        """
        self.verbose = verbose
        
        GPF.print_vars(function_name = "GaussianPlume.GaussianPlume.__init__()", function_vars = vars(), verbose = verbose, self_verbose = self.verbose)

        self.plumes = []
        
        
    def add_parameter_files(self, filename, path = None, verbose = 0):
        """
        Add the paths and filenames of the parameter files.
        
        Arguments
        ---------
        filename : 
            A single filename or list with filenames. The filename(s) may contain the path as well. They must contain the extension. The filename(s) can be a string or a pathlib object. 
        path : None
            A path or a list with paths. Defaults to None, which means the path is not needed or the path is included in the filename(s). The path(s) can be a string or a pathlib object. 
        
        Notes
        -----
        There are a number of options:
        
        * filename = 'C:/path/filename.ext': 
        * filename = 'filename.ext', path = 'C:/path': the 
        
        
        
        """
        GPF.print_vars(function_name = "GaussianPlume.add_parameter_files()", function_vars = vars(), verbose = verbose, self_verbose = self.verbose)
        
        
        
        
        if type(path_and_filenames) != list:
            path_and_filenames = [path_and_filenames]
        
        for paf in path_and_filenames:
            X = GPPM.Plume(verbose = self.verbose)
            self.plumes.append(X)
            
            
    def save_plume(self, pickle_path, pickle_filename, plume_index, verbose = 0):
        """
        
        """
        GPF.print_vars(function_name = "GaussianPlume.save_plume()", function_vars = vars(), verbose = verbose, self_verbose = self.verbose)

        pickle_paf = pickle_path.joinpath(pickle_filename)
        with open(pickle_paf, "wb") as F:
            pickle.dump(self.plumes[plume_index], F)
        
        
    def load_plume(self, pickle_path, pickle_filename, verbose = 0):
        """
        
        """
        GPF.print_vars(function_name = "GaussianPlume.load_plume()", function_vars = vars(), verbose = verbose, self_verbose = self.verbose)

        pickle_paf = pickle_path.joinpath(pickle_filename)        
        with open(pickle_paf, "rb") as F:
            self.plumes.append(pickle.load(F))
        
        
    def save_plumes(self, pickle_path, pickle_filename, verbose = 0):
        """
        
        """
        GPF.print_vars(function_name = "GaussianPlume.save_plumes()", function_vars = vars(), verbose = verbose, self_verbose = self.verbose)

        pickle_paf = pickle_path.joinpath(pickle_filename)
        with open(pickle_paf, "wb") as F:
            pickle.dump(self.plumes, F)
        
        
    def load_plumes(self, pickle_path, pickle_filename, append_to_plumes = False, verbose = 0):
        """
        
        """
        GPF.print_vars(function_name = "GaussianPlume.load_plumes()", function_vars = vars(), verbose = verbose, self_verbose = self.verbose)

        pickle_paf = pickle_path.joinpath(pickle_filename)        
        with open(pickle_paf, "rb") as F:
            if append_to_plumes:
                self.plumes += pickle.load(F)
            else:
                self.plumes = pickle.load(F)
                
        
        
        
        
        
        
        
        

        