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
        verbose = GPF.print_vars(function_name = "GaussianPlume.add_parameter_files()", function_vars = vars(), verbose = verbose, self_verbose = self.verbose)
        
        paf = GPF.handle_filename_path(filename, path, verbose = verbose)
        
        for p in paf:
            X = GPPM.Plume(verbose = self.verbose)
            self.plumes.append(X)
            
            
    def save_plume(self, pickle_filename, plume_index, pickle_path = None, verbose = 0):
        """
        Save one or more plumes as a pickle.
        
        Arguments
        ---------
        pickle_filename : (list with) Pathlib or str
            A single filename or list with filenames. The filename(s) may contain the path as well. They must contain the extension. The filename(s) can be a string or a pathlib object. 
        plume_index : (list with) int
            The index/indices you want to save
        pickle_path : (list with) Pathlib or str, or None
            A path or a list with paths. Defaults to None, which means the path is not needed or the path is included in the filename(s). The path(s) can be a string or a pathlib object. 
        
        Raises
        -----
        IndexError
            If the length of the path-and-filenames is not the same as the length of the indices
        
        See Also
        --------
        load_plume : load the plume(s) 
        load_plumes : load a list with plumes
        save_plumes : save the complete list with plumes
        GPFunctions.handle_filename_path : function used to generate the path(s) and filename(s)
        
        """
        verbose = GPF.print_vars(function_name = "GaussianPlume.save_plume()", function_vars = vars(), verbose = verbose, self_verbose = self.verbose)

        paf = GPF.handle_filename_path(filename = pickle_filename, path = pickle_path, verbose = verbose)
        if type(plume_index) == int:
            plume_index = [plume_index]
        
        if len(plume_index) != len(paf):
            raise IndexError("The length of the path-and-filenames ({:d}) and of the indices ({:d}) is not the same.".format(len(paf), len(plume_index)))
        
        for p_i, p_idx in enumerate(plume_index):
            with open(paf[p_i], "wb") as F:
                pickle.dump(self.plumes[p_idx], F)
        
        
    def load_plume(self, pickle_filename, pickle_path = None, verbose = 0):
        """
        Load one or more 

        Arguments
        ---------        
        pickle_filename : (list with) Pathlib or str
            A single filename or list with filenames. The filename(s) may contain the path as well. They must contain the extension. The filename(s) can be a string or a pathlib object. 
        plume_index : (list with) int
            The index/indices you want to save
        pickle_path : (list with) Pathlib or str, or None
            A path or a list with paths. Defaults to None, which means the path is not needed or the path is included in the filename(s). The path(s) can be a string or a pathlib object.         

        See Also
        --------
        save_plume : save the plume(s) 
        load_plumes : load a list with plumes
        save_plumes : save the complete list with plumes
        GPFunctions.handle_filename_path : function used to generate the path(s) and filename(s)
        
        """
        verbose = GPF.print_vars(function_name = "GaussianPlume.load_plume()", function_vars = vars(), verbose = verbose, self_verbose = self.verbose)

        pafs = GPF.handle_filename_path(filename = pickle_filename, path = pickle_path, verbose = verbose)      
        for paf in pafs:
            with open(paf, "rb") as F:
                self.plumes.append(pickle.load(F))
        
        
    def save_plumes(self, pickle_filename, pickle_path = None, verbose = 0):
        """
        Save the list with plumes. 

        Arguments
        ---------        
        pickle_filename : Pathlib or str
            A single filename. It may contain the path, it must contain the extension. 
        pickle_path : Pathlib or str, or None
            A path. Defaults to None, which means the path is not needed or the path is included in the filename. The path can be a string or a pathlib object.    

        Raises
        -----
        ValueError
            If pickle_filename and/or pickle_path is a list with more than 1 item. 

        See Also
        --------        
        load_plume : load the plume(s) 
        save_plume : save the plume(s) 
        load_plumes : load a list with plumes
        GPFunctions.handle_filename_path : function used to generate the path(s) and filename(s)
        
        """
        verbose = GPF.print_vars(function_name = "GaussianPlume.save_plumes()", function_vars = vars(), verbose = verbose, self_verbose = self.verbose)

        paf = GPF.handle_filename_path(filename = pickle_filename, path = pickle_path, verbose = verbose)
        if len(paf) > 1:    
            raise ValueError
        
        with open(paf[0], "wb") as F:
            pickle.dump(self.plumes, F)
        
        
    def load_plumes(self, pickle_filename, pickle_path = None, append_to_plumes = False, verbose = 0):
        """
        Load one or more lists with plumes. 
        
        Arguments
        ---------        
        pickle_filename : (list with) Pathlib or str
            A single filename or list with filenames. The filename(s) may contain the path as well. They must contain the extension. The filename(s) can be a string or a pathlib object. 
        pickle_path : (list with) Pathlib or str, or None
            A path or a list with paths. Defaults to None, which means the path is not needed or the path is included in the filename(s). The path(s) can be a string or a pathlib object.    
        append_to_plumes : bool (False)
            If true, append the imported objects to the current plumes. If False (default), discard the current objects. 
        
        See Also
        --------        
        load_plume : load the plume(s) 
        save_plume : save the plume(s) 
        save_plumes : save the complete list with plumes
        GPFunctions.handle_filename_path : function used to generate the path(s) and filename(s)
        
        """
        verbose = GPF.print_vars(function_name = "GaussianPlume.load_plumes()", function_vars = vars(), verbose = verbose, self_verbose = self.verbose)

        pafs = GPF.handle_filename_path(filename = pickle_filename, path = pickle_path, verbose = verbose)

        if append_to_plumes == False:
            self.plumes = []

        for paf in pafs:
            with open(paf, "rb") as F:
                self.plumes += pickle.load(F)
                
        
        
        
        
        
        
        
        

        