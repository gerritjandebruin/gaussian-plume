import importlib

import numpy

import pandas

import ClassTools as CT
import GPFunctions as GPF
import GPMolecule as GPMO

importlib.reload(GPF)
importlib.reload(GPMO)

class Source(CT.ClassTools):

    def __init__(self, source_id, molecule = None, verbose = 0, **kwargs):
        """
        
        Arguments
        ---------
        source_id : int
            The id of the source. Each source must have its own number.
        molecule : string
            The name of the molecule emitted by the source.
        label : str, optional
            The name of the source. If no label is given, it is given as sourceX, where X is the `source_identifier`. 
        
        """
        self.verbose = verbose
        
        verbose = GPF.print_vars(function_name = "GPSource.Source.__init__()", function_vars = vars(), verbose = verbose, self_verbose = self.verbose)  

        self.source_id = source_id

        if type(molecule) == str:            
            self.molecule = GPMO.Molecule(molecule, verbose = verbose)
        elif molecule is None:
            self.molecule = molecule
        else:
            self.molecule = molecule
        
        self.label = kwargs.get("label", None)
        if self.label is None:
            if self.molecule is None:
                self.label = "{:}".format(self.source_id)
            else:
                self.label = "{:} {:s}".format(self.source_id, self.molecule.name)
    
        self.dx = kwargs.get("dx", None)
        self.dy = kwargs.get("dy", None)
        
        self.dlatS = kwargs.get("dlatS", None)
        self.dlonS = kwargs.get("dlonS", None)
        self.dlatM = kwargs.get("dlatM", None)
        self.dlonM = kwargs.get("dlonM", None)  
        
        self.latS = kwargs.get("latS", None)
        self.lonS = kwargs.get("lonS", None)        
        self.latR = kwargs.get("latR", None)
        self.lonR = kwargs.get("lonR", None)     
        self.latM = kwargs.get("latM", None)
        self.lonM = kwargs.get("lonM", None)  
        
        self.warn_distance_above_meter = kwargs.get("warn_distance_above_meter", None)
        
        self.wind_direction = kwargs.get("wind_direction", None)
        self.wind_speed = kwargs.get("wind_speed", None)
        self.qs = kwargs.get("qs", None)
        self.hs = kwargs.get("hs", None)
        self.hm = kwargs.get("hm", None)
        self.z0 = kwargs.get("z0", None)
        self.zr = kwargs.get("zr", None)
        self.offset_sigma_z = kwargs.get("offset_sigma_z", None)
        self.dispersion_mode = kwargs.get("dispersion_mode", None)
        self.dispersion_constants = kwargs.get("dispersion_constants", None)

        self.tc = kwargs.get("tc", None)
        self.tc_minimum = kwargs.get("tc_minimum", None)

        self.sigma_y = kwargs.get("sigma_y", None)
        self.sigma_z = kwargs.get("sigma_z", None)        
        
        self._stability_index = None
        self._stability_class = None
        if "stability_index" in kwargs:
            self.stability_index = kwargs["stability_index"]
        if "stability_class" in kwargs:
            self.stability_class = kwargs["stability_class"]
                
        

    @property
    def stability_index(self):
        """
        Index of the stability class. 0 equals class A, 5 equals class F.
        """
        return self._stability_index

    @stability_index.setter
    def stability_index(self, value):
        self._stability_index = value
        self._stability_class = GPF.stability_index2class(value)

    @property
    def stability_class(self):
        """
        Stability class. Class A equals index 0, class F equals index 5. 
        """    
        return self._stability_class

    @stability_class.setter
    def stability_class(self, value):
        self._stability_class = value
        self._stability_index = GPF.stability_class2index(value) 



    def calculate_dxdy(self, verbose = 0):
        """
        
        Arguments
        ---------

        
        """
        verbose = GPF.print_vars(function_name = "GPSource.Source.calculate_dxdy()", function_vars = vars(), verbose = verbose, self_verbose = self.verbose)  
        
        if verbose > 2:
            print("latS: {:}".format(self.latS))
            print("lonS: {:}".format(self.lonS))
            print("latR: {:}".format(self.latR))
            print("lonR: {:}".format(self.lonR))
            print("latM: {:}".format(self.latM))
            print("lonM: {:}".format(self.lonM))
        
        if self.dx is not None and self.dy is not None:
            pass
        else:
        
            if self.dlatS is None or self.dlonS is None:
                if self.latS is not None and self.lonS is not None and self.latR is not None and self.lonR is not None:
                    self.dlatS, self.dlonS = GPF.latlon2dlatdlon(lat = self.latS, lon = self.lonS, latR = self.latR, lonR = self.lonR, verbose = verbose) 
                else:
                    
                    error_string = "GPSource.calculate_dxdy(): no location data for: "
                    if self.dlatS is None:
                        error_string = "{:s} dlatS, ".format(error_string)
                    if self.dlonS is None:
                        error_string = "{:s} dlonS, ".format(error_string)
                    if self.latS is None:
                        error_string = "{:s} latS, ".format(error_string)
                    if self.lonS is None:
                        error_string = "{:s} lonS, ".format(error_string)
                    if self.latR is None:
                        error_string = "{:s} latR, ".format(error_string)
                    if self.lonR is None:
                        error_string = "{:s} lonR, ".format(error_string)
                    raise ValueError(error_string)
                    
            if self.dlatM is None or self.dlonM is None:
                if self.latM is not None and self.lonM is not None and self.latR is not None and self.lonR is not None:
                    self.dlatM, self.dlonM = GPF.latlon2dlatdlon(lat = self.latM, lon = self.lonM, latR = self.latR, lonR = self.lonR, verbose = verbose) 
                else:
                    error_string = "GPSource.calculate_dxdy(): no location data for: "
                    if self.dlatM is None:
                        error_string = "{:s} dlatM, ".format(error_string)
                    if self.dlonM is None:
                        error_string = "{:s} dlonM, ".format(error_string)
                    if self.latM is None:
                        error_string = "{:s} latM, ".format(error_string)
                    if self.lonM is None:
                        error_string = "{:s} lonM, ".format(error_string)
                    if self.latR is None:
                        error_string = "{:s} latR, ".format(error_string)
                    if self.lonR is None:
                        error_string = "{:s} lonR, ".format(error_string)
                    raise ValueError(error_string)
            
            if self.wind_direction is None:
                raise ValueError("GPSource.calculate_dxdy(): no data for wind_direction")
            
            self.dx, self.dy = GPF.dlatdlon2dxdy(dlatS = self.dlatS, dlonS = self.dlonS, dlatM = self.dlatM, dlonM = self.dlonM, wind_direction = self.wind_direction, verbose = verbose)
        
    def calculate_sigma_y_z(self, verbose = 0, **kwargs):
        """
        
        """
    
        verbose = GPF.print_vars(function_name = "GPSource.Source.calculate_sigma_y_z()", function_vars = vars(), verbose = verbose, self_verbose = self.verbose)          

        if self.dx is None:
            raise ValueError("GPSource.Source.calculate_sigma_y_z(): variable dx is missing")
        if self.z0 is None:
            raise ValueError("GPSource.Source.calculate_sigma_y_z(): variable z0 is missing")
        if self.wind_speed is None:
            raise ValueError("GPSource.Source.calculate_sigma_y_z(): variable wind_speed is missing")                 
        
            
        if self.tc is None:
            self.tc = GPF.calculate_tc(self.dx, self.wind_speed, verbose = verbose)

        if self.dispersion_constants is None:
            if self.dispersion_mode is None:
                raise ValueError("GPSource.Source.calculate_sigma_y_z(): variable dx is missing")  
            self.dispersion_constants = GPF.get_dispersion_constants(dispersion_mode = self.dispersion_mode)
       
        if self.stability_index is None:
            raise ValueError("GPSource.Source.calculate_sigma_y_z(): variable stability_index is missing")        
            
        self.sigma_y, self.sigma_z = GPF.calculate_sigma(dx = self.dx, z0 = self.z0, tc = self.tc, dispersion_constants = self.dispersion_constants, stability_index = self.stability_index, offset_sigma_z = self.offset_sigma_z, tc_minimum = self.tc_minimum, verbose = verbose)
            
    def calculate_concentration(self, molecule = None, verbose = 0, **kwargs):
        """
         
        """
    
        verbose = GPF.print_vars(function_name = "GPSource.Source.calculate_sigma_y_z()", function_vars = vars(), verbose = verbose, self_verbose = self.verbose)   
        
        if molecule is None:
            if self.molecule is None:
                raise ValueError("GPSource.calculate_concentration(): no molecule is defined")   
            else:
                molecule = self.molecule

        return GPF.calculate_concentration(qs = self.qs, wind_speed = self.wind_speed, sigma_y = self.sigma_y, sigma_z = self.sigma_z, dy = self.dy, zr = self.zr, hs = self.hs, hm = self.hm, molecular_mass = molecule.molecular_mass, verbose = verbose)
        