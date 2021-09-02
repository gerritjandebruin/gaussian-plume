
import importlib

import numpy
import PythonTools.ClassTools as CT
import GPFunctions as GPF

importlib.reload(GPF)

class Location(CT.ClassTools):

    def __init__(self, lat, lon, verbose = 0, **kwargs):
        """
        
        Arguments
        ---------
        lat : number, ndarray, list
            Latitude
        lon : number, ndarray, list
            Longitude
        
        """
        self.verbose = verbose
        
        verbose = GPF.print_vars(function_name = "GPLocation.GPLocation.__init__()", function_vars = vars(), verbose = verbose, self_verbose = self.verbose)   
        
        self.lat = lat
        self.lon = lon

        



class Geometry(CT.ClassTools):

    def __init__(self, verbose = 0, **kwargs):
        """
        
        Arguments
        ---------



   
        """
        self.verbose = verbose
        
        verbose = GPF.print_vars(function_name = "GPLocationGeometry.GPGeometry.__init__()", function_vars = vars(), verbose = verbose, self_verbose = self.verbose)
        
        self.locS = kwargs.get("locS", None)
        self.locM = kwargs.get("locM", None)
        self.locR = kwargs.get("locR", None)
        
        self.dlatS = kwargs.get("dlatS", None)
        self.dlonS = kwargs.get("dlonS", None)

        self.dlatM = kwargs.get("dlatM", None)
        self.dlonM = kwargs.get("dlonM", None)        
        
    def calculate_distance_to_reference(self, verbose = 0):
        """
        
        Arguments
        ---------



   
        """        
        self.verbose = verbose
        
        verbose = GPF.print_vars(function_name = "GPGeometry.calculate_distance_to_reference.__init__()", function_vars = vars(), verbose = verbose, self_verbose = self.verbose)  

        if self.locR is None:
            raise ValueError("Reference location should not be None.")
        
        if self.locS is not None:    
            self.dlatS, self.dlonS = GPF.latlon2dlatdlon(self.locS.lat, self.locS.lon, self.locR.lat, self.locR.lon)
            
        if self.locM is not None:    
            self.dlatM, self.dlonM = GPF.latlon2dlatdlon(self.locM.lat, self.locM.lon, self.locR.lat, self.locR.lon)        
        
        

if __name__ == "__main__":

    locationS = Location(51.5775117, 5.58756835)
    locationR = Location(51.5852, 5.6015)

    G = Geometry(locationS = locationS, locationR = locationR)
    G.calculate_distance_to_reference()


















        