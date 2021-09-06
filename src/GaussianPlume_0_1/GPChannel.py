
import importlib

import numpy
import PythonTools.ClassTools as CT
import GPFunctions as GPF

importlib.reload(GPF)

class Channel(CT.ClassTools):

    def __init__(self, channel_identifier, molecule, device_name, verbose = 0, **kwargs):
        """
        
        Arguments
        ---------

        
        """
        self.verbose = verbose
        
        verbose = GPF.print_vars(function_name = "GPChannel.Channel.__init__()", function_vars = vars(), verbose = verbose, self_verbose = self.verbose)   
        
        self.channel_identifier = channel_identifier
        self.molecule = molecule
        self.device_name = device_name
        