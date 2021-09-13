import importlib 

import numpy
import ClassTools as CT
import GPFunctions as GPF
import GPMolecule as GPMO

importlib.reload(GPF)
importlib.reload(GPMO)

class Channel(CT.ClassTools):

    def __init__(self, channel_id, molecule, device_name, verbose = 0, **kwargs):
        """
        
        Arguments
        ---------
        channel_id : int
            Identifier of this channel.
        device_name : str
            The name of the device
        molecule : GPMolecule or str
            The molecule measured with this channel. If the input is a string, it will generate a GPMolecule object.
        label : str (opt)
            A short label to be used for this channel. If it is not set, it will be the `channel_id`, `molecule.name`, and `device_name`.
        concentration : ndarray
            The calculated concentration.
        plume_number : ndarray
            The number of the plumes, from the measurement data. 
        
        """
        self.verbose = verbose
        
        verbose = GPF.print_vars(function_name = "GPChannel.Channel.__init__()", function_vars = vars(), verbose = verbose, self_verbose = self.verbose)      
        
        self.channel_id = channel_id
        self.device_name = device_name

        if type(molecule) == str:
            self.molecule = GPMO.Molecule(molecule, verbose = verbose)
        else:
            self.molecule = molecule

        self.label = kwargs.get("label", None)
        if self.label is None:
            self.label = "{:} {:s} {:s}".format(self.channel_id, self.molecule.name, self.device_name)


        self.concentration_measured = kwargs.get("concentration_measured", None)
        self.concentration_model = None
        self.plume_number = kwargs.get("plume_numbers", None)
        

    def get_concentration_for_plume(self, plume, model = True, source_index = None, cumulative = False, verbose = 0, **kwargs):
        """
        
        Arguments
        ---------
        plume : number
            The number of the plume.
        source_index : number or None
            The index of the source. If None, it will return all sources.
        cumulative : bool (default: False)
            If True, sum the concentrations. If False, return the ndarray
            
            
        Notes
        -----
        
        
        
        - When `source_index == N` (where `N` is a number) and `cumulative == False`: return the concentration over time for source `N` (as an array)
        - When `source_index == N` and `cumulative == True`: return the concentration of source `N` integrated over time (as a number)
        - When `source_index == None` and `cumulative == False`: 
        - When `source_index == None` and `cumulative == True`:
        - When `source_index == None` and `cumulative == True`:
        - When `source_index == None` and `cumulative == True`:
            
        
        
        """
        verbose = GPF.print_vars(function_name = "GPChannel.Channel.get_concentration_for_plume()", function_vars = vars(), verbose = verbose, self_verbose = self.verbose)   
        
        self.plume_number = kwargs.get("plume_number", self.plume_number)
        
        if type(plume) in (list, numpy.ndarray):
            idx = numpy.array([], dtype = int)
            for p in plume:
                _idx = numpy.where(p == self.plume_number)[0]
                idx = numpy.concatenate((idx, _idx))
        else:
            idx = numpy.where(plume == self.plume_number)[0]

        concentration_data = self.concentration_model
    
        if source_index is None:
            if cumulative:
                return numpy.sum(concentration_data[idx,:])
            else:
                return concentration_data[idx,:]
                
        elif type(source_index) in (list, numpy.ndarray):
            if cumulative:
                return numpy.sum(concentration_data[:,source_index][idx,:])
            else:
                return concentration_data[:,source_index][idx,:]           
                
        else:
            if cumulative:
                return numpy.sum(concentration_data[idx,source_index])
            else:
                return concentration_data[idx,source_index]
        





















        