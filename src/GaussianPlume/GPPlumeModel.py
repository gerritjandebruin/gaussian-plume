"""
To calculate the concentration, the following input is required:

* `Qs`: Source strength in gram / second
* `wind_speed`: Wind speed in m/s.
* `dx`: Distance between the source and the measurement in meters. 
* `dy`: Perpendicular distance between source and measurement in meters
* `z0`: Source height in meters
* `Zr`: Height of the measurement in meters
* `Hs`: Height of the source in meters
* `Hm`: Height of the mixing layer in meters 
* `mode`: select dispersion constants (NOGEPA / farm)
* `stability`: Index 0-5 for stability, where 0 is most stable.
* 'molecular_mass`: Molecular mass in g/mol.

Intermediate calculations are done:

* `sigma_y`: Plume width in meters, calculated from dx, z0, Tc, ca, cb, dispersion_constants, stability
* `sigma_z`: Plume height in meters, calculated from dx, z0, Tc, ca, cb, dispersion_constants, stability
* `Tc`: Travel time between source and measurement in seconds, calculated using dx and wind_speed. 

Some are constants

* `molecule`: A dictionary with the molecule formula, a nice (standardized) name, and the molecular mass in g/mol.
* `ca`: Some exponent used to calculate sigma_y and sigma_z
* `cb`: Some exponent used to calculate sigma_y and sigma_z
* `dispersion_constants`: Table with dispersion constants, selected from mode and stability

"""
import importlib
import pathlib

import GPFunctions as GPF
import GPImportData as GPID
import PythonTools.ClassTools as CT

importlib.reload(GPF)
importlib.reload(GPID)

class Plume(CT.ClassTools):
    """
    Arguments
    ---------
    Qs : number-like
        Source strength in gram / second
    wind_speed : number-like
        Wind speed in m/s.
    wind_direction : number-like
        Wind direction in degrees.
    dx : number-like
        Distance between the source and the measurement in meters. This can be set itself, but is recalculated when latS, lonS, latM, and lonM are all set. 
    dy : number-like
        Perpendicular distance between source and measurement in meters
    latS : number-like  
        Latitude of the source.
    lonS : number-like  
        Longitude of the source.
    lonS : number-like  
        Longitude of the source.        
    latM : number-like  
        Latitude of the measurement.
    lonM : number-like  
        Longitude of the measurement.               
    z0 : number-like
        Source height in meters
    Zr : number-like
        Height of the measurement in meters
    Hs : number-like
        Height of the source in meters
    Hm : number-like
        Height of the mixing layer in meters 
    mode : number-like
        Select dispersion constants (NOGEPA / farm)
    stability_index : number-like
        Index 0-5 for stability, where 0 is most stable. If both `stability_index` and `stability_class` are given during initialization, `stability_index` is used. 
    stability_class : str-like
        Class A-F for stability, where A is most stable. If both `stability_index` and `stability_class` are given during initialization, `stability_index` is used.            
    molecular_mass : 
        Molecular mass in g/mol.   
    
    """
    def __init__(self, verbose = 0, **kwargs):
        """

     
        
        """
        self.verbose = verbose
        
        GPF.print_vars(function_name = "GPPlume.Plume.__init__()", function_vars = vars(), verbose = verbose, self_verbose = self.verbose)

        self.df = kwargs.get("df", None)

        self.parameter_filename = kwargs.get("parameter_filename", None)
        self.parameter_path = kwargs.get("parameter_path", None)
        self.parameter_paf = GPF.handle_filename_path(filename = self.parameter_filename, path = self.parameter_path, verbose = self.verbose)
        
        self.measurement_filename = kwargs.get("measurement_filename", None)
        self.measurement_path = kwargs.get("measurement_path", None)
        self.measurement_paf = GPF.handle_filename_path(filename = self.measurement_filename, path = self.measurement_path, verbose = self.verbose)

        self.qs = kwargs.get("qs", None)
        self.wind_speed = kwargs.get("wind_speed", None)
        self.wind_direction = kwargs.get("wind_direction", None)
        self.latS = kwargs.get("latS", None)
        self.lonS = kwargs.get("lonS", None)
        self.latM = kwargs.get("latM", None)
        self.lonM = kwargs.get("lonM", None)
        self.dx = kwargs.get("dx", None)
        self.dy = kwargs.get("dy", None)
        self.z0 = kwargs.get("z0", None)
        self.zr = kwargs.get("zr", None)
        self.hs = kwargs.get("hs", None)
        self.hm = kwargs.get("hm", None)
        self.molecular_mass = kwargs.get("molecular_mass", None)
        self.mode = kwargs.get("mode", None)
        if "stability_index" in kwargs:
            self.stability_index = kwargs["stability_index"]
        elif "stability_class" in kwargs:
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
    



    def import_data(self, static_parameters = True, dynamic_parameters = True, verbose = 0, **kwargs):
        """
        
        """
        verbose = GPF.print_vars(function_name = "GPPlumeModel.import_data()", function_vars = vars(), verbose = verbose, self_verbose = self.verbose)

        parameter_paf = kwargs.get("parameter_paf", self.parameter_paf)
        measurement_paf = kwargs.get("measurement_paf", self.measurement_paf)

        df_static, df_dynamic = GPID.import_measurement_parameters_excel(parameter_paf, static_parameters = static_parameters, dynamic_parameters = dynamic_parameters, verbose = verbose)

        if measurement_paf is None:
            measurement_paf = [pathlib.Path(df_static.loc[0,"measurement_data_path_and_filename"])]

        df = GPID.import_measurement_data(measurement_paf, verbose = verbose)

        self.df = GPID.merge_measurement_static_dynamic_df(df, df_static, df_dynamic, verbose = verbose)










