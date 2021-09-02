import numpy
import PythonTools.ClassTools as CT
import GPFunctions as GPF


class Source(CT.ClassTools):

    def __init__(self, source_identifier, molecules, verbose = 0, **kwargs):
        """
        
        Arguments
        ---------
        source_identifier : int
            The number of the source. Each source must have its own number.
        molecule : string or array with strings
            The names of the molecules emitted by the source.
        label : str, optional
            The name of the source. If no label is given, it is given as sourceX, where X is the `source_identifier`. 
        
        """
        self.verbose = verbose
        
        verbose = GPF.print_vars(function_name = "GPSource.Source.__init__()", function_vars = vars(), verbose = verbose, self_verbose = self.verbose)        
        
        self.source_identifier = source_identifier
        self.molecules = molecules
        
        self.label = kwargs.get("label", None)
        self.locS = kwargs.get("locS", None)
        self.locR = kwargs.get("locR", None)
        
        self.qs = kwargs.get("qs", None)
        self.hs = kwargs.get("hs", None)
        self.z0 = kwargs.get("z0", None)
        self.offset_sigma_z = kwargs.get("offset_sigma_z", None)
        