"""



"""

import importlib
import pickle
import pathlib

import numpy

import PythonTools.ClassTools as CT
import GPFunctions as GPF
import GPPlumeModel as GPPM
import GPImportData as GPID
import GPLocationGeometry as GPLG

importlib.reload(GPF)
importlib.reload(GPPM)
importlib.reload(GPID)
importlib.reload(GPLG)


class GaussianPlume(CT.ClassTools):
    """
    
    
    Attributes
    ----------
    plumes : list 
        List with plumes
    sources : list
        List with sources
    molecules : list
        List with molecules
    channels : list
        List with measurement channels
        
    
    """


    def __init__(self, verbose = 0, **kwargs):
        """

     
        
        """
        self.verbose = verbose
        
        verbose = GPF.print_vars(function_name = "GaussianPlume.GaussianPlume.__init__()", function_vars = vars(), verbose = verbose, self_verbose = self.verbose)

        self.plumes = []
        self.sources = []
        self.channels = []
        self.molecules = []
        
        
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
            X = GPPM.Plume(parameter_filename = p, verbose = self.verbose)
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
                
        
    def import_plume(self, plume_index, verbose = 0, **kwargs):
        """
        
        
        """
        verbose = GPF.print_vars(function_name = "GaussianPlume.import_plume()", function_vars = vars(), verbose = verbose, self_verbose = self.verbose)
        

        
        self.plumes[plume_index].import_data(verbose = verbose, **kwargs)


    
    def calculate_plume(self, verbose = 0, **kwargs):
        """
        
        """
        
        verbose = GPF.print_vars(function_name = "GaussianPlume.calculate_plume.__init__()", function_vars = vars(), verbose = verbose, self_verbose = self.verbose)    
        
        
        results = []
        
        logs = []
        
        print()
        for plume_index, plume in enumerate(self.plumes):
        
            print("plume_index: {:d}".format(plume_index))
            
            for channel_index, channel in enumerate(self.channels):
                
                print("  channel_index: {:d} - {:4s} {:s}".format(channel_index, channel.molecule, channel.device_name))
                
                for molecule_index, molecule in enumerate(self.molecules):
                    
                    print("    molecule_index: {:d} - {:s}".format(molecule_index, molecule.name))
                    
                    total_concentration = 0 
                    
                    for source_index, source in enumerate(self.sources):
                        
                        if channel.molecule in molecule.aliases and source.molecules in molecule.aliases:
                            
                            log = {
                                "index p/c/m/s": "{:d}/{:d}/{:d}/{:d}".format(plume_index, channel_index, molecule_index,source_index),
                                "plume": plume_index,
                                "channel identifier": channel.channel_identifier,
                                "molecule name": molecule.name,
                                "source identifier": source.source_identifier,
                                # "molecule": channel.molecule,
                            }
                                
                            
                            self.locM = GPLG.Location(plume.df.loc[:,"latM"].to_numpy(), plume.df.loc[:,"lonM"].to_numpy(), verbose = self.verbose)
                            if type(self.locM.lat) in (list, numpy.ndarray):
                                log["locM [0] (lat, lon)"] = (self.locM.lat[0], self.locM.lon[0])
                            else:
                                log["locM (lat, lon)"] = (self.locM.lat, self.locM.lon)
                            
                            if type(source.locS.lat) in (list, numpy.ndarray):
                                log["locS [0] (lat, lon)"] = (source.locS.lat[0], source.locS.lon[0])
                            else:
                                log["locS (lat, lon)"] = (source.locS.lat, source.locS.lon)
                            
                            dlatS, dlonS = GPF.latlon2dlatdlon(source.locS.lat, source.locS.lon, source.locR.lat, source.locR.lon, verbose = verbose)

                            if type(dlatS) in (list, numpy.ndarray):
                                log["dlatS [0]"] = dlatS[0]
                                log["dlonS [0]"] = dlonS[0]
                            else:
                                log["dlatS"] = dlatS
                                log["dlonS"] = dlonS

                            
                            log["locR (lat, lon)"] = (self.locR.lat, self.locR.lon)
                            
                            dlatM, dlonM = GPF.latlon2dlatdlon(self.locM.lat, self.locM.lon, self.locR.lat, self.locR.lon, verbose = verbose)

                            if type(dlatM)  in (list, numpy.ndarray):
                                log["dlatM [0]"] = dlatM[0]
                                log["dlonM [0]"] = dlonM[0]
                            else:
                                log["dlatM"] = dlatM
                                log["dlonM"] = dlonM
                
                            dx, dy = GPF.dlatdlon2dxdy(dlatS, dlonS, dlatM, dlonM, wind_direction = plume.df.loc[:,"wind_direction"].to_numpy(), verbose = verbose)

                            if type(dx)  in (list, numpy.ndarray):
                                log["dx [0]"] = dx[0]
                                log["dy [0]"] = dy[0]
                                log["dx <>"] = numpy.mean(dx)
                                log["dy <>"] = numpy.mean(dy)
                            else:
                                log["dx"] = dx
                                log["dy"] = dy
                            
                            # tc = GPF.calculate_Tc(dx, plume.df.loc[:,"wind_speed"], verbose = verbose)
                            tc = 0.05
                            dispersion_constants = GPF.get_dispersion_constants(mode = "farm", verbose = verbose)
            
                            sigma_y, sigma_z = GPF.calculate_sigma(
                                dx = dx, 
                                z0 = source.z0, 
                                Tc = tc, 
                                dispersion_constants = dispersion_constants, 
                                stability = 1, 
                                offset_sigma_z = source.offset_sigma_z, 
                                verbose = verbose
                            )
            
                            concentration = GPF.calculate_concentration(
                                Qs = source.qs, 
                                wind_speed = plume.df.loc[:,"wind_speed"].to_numpy(), 
                                sigma_y = sigma_y, 
                                sigma_z = sigma_z, 
                                dy = dy, 
                                Zr = plume.df.loc[:,"zr"].to_numpy(), 
                                Hs = source.hs, 
                                Hm = plume.df.loc[:,"hm"].to_numpy(), 
                                molecular_mass = molecule.molecular_mass, 
                                verbose = verbose
                            )
                            
                            concentration = numpy.sum(concentration)
            
                            print("          source {:d}: sigma Y: {:4.2f}, Z: {:4.2f}, concentration: {:6.2f}, dx: {:5.1f}, dy: {:5.1f}".format(source_index, numpy.mean(sigma_y), numpy.mean(sigma_z), concentration, numpy.mean(dx), numpy.mean(dy)))
            
                            # print("        concentration: {:6.2f} ppb".format(concentration))
                            
                            total_concentration += concentration
                            
                            logs.append(log)
                        # else:
                            # print("        --")
                            
                    print("    total: {:6.2f}".format(total_concentration))
        
        for log in logs:
            for k, v in log.items():
                print("{:20} : {:}".format(k,v))
            print()
                
            # print(log)
        
        # print(logs)
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        

        