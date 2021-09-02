
import importlib

import numpy
import PythonTools.ClassTools as CT
import GPFunctions as GPF

importlib.reload(GPF)

class Molecule(CT.ClassTools):

    def __init__(self, molecule, verbose = 0, **kwargs):
        """
        
        Arguments
        ---------
        molecule : str
            The name of a molecule
        
        """
        self.verbose = verbose
        
        verbose = GPF.print_vars(function_name = "GPMolecule.Molecule.__init__()", function_vars = vars(), verbose = verbose, self_verbose = self.verbose)   

        self.molecule = molecule
        
        props = GPF.get_molecule_properties(self.molecule, verbose)
        self.aliases = props["aliases"] 
        self.formula = props["formula"]
        self.name = props["name"] 
        self.molecular_mass = props["molecular_mass"]
