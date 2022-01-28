import importlib

import numpy

import pandas

import ClassTools as CT
import GPFunctions as GPF
import GPMolecule as GPMO

importlib.reload(GPF)
importlib.reload(GPMO)

class Plume(CT.ClassTools):
    """
    Arguments
    ---------
    plume_id : int
        The id of the plume. Each plume must have its own number.
    label : str, optional
        The name of the source. If no label is given, it is given as sourceX, where X is the `source_identifier`. 
    plume_idx : ndarray
        Indices of the plume
    
    wind_direction ; number or ndarray
    """

    def __init__(self, plume_id, verbose = 0, **kwargs):
        """
        

            
            
        
        """
        self.verbose = verbose
        
        verbose = GPF.print_vars(function_name = "GPPlume.Plume.__init__()", function_vars = vars(), verbose = verbose, self_verbose = self.verbose)  

        self.plume_id = plume_id
        
        self.label = kwargs.get("label", None)
        if self.label is None:
            self.label = "Plume {:}".format(self.plume_id)
        
        self.plume_idx = kwargs.get("plume_idx", None)
        
        self.plume_length = None
        if self.plume_idx is not None:
            self.plume_length = len(self.plume_idx)
        
        self.wind_direction = kwargs.get("wind_direction", None)
        self.wind_direction_plus = kwargs.get("wind_direction_plus", None)
        
        self.wind_speed = kwargs.get("wind_speed", None)
        self.wind_speed_plus = kwargs.get("wind_speed_plus", None)
        self.wind_speed_times = kwargs.get("wind_speed_times", None)
        
        background_length_times = kwargs.get("background_length_times", None)
        background_length_before_plume = kwargs.get("background_length_before_plume", None)
        background_length_after_plume = kwargs.get("background_length_after_plume", None)
        
        

    
