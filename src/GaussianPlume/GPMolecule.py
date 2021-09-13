import numpy
import ClassTools as CT
import GPFunctions as GPF
import GPConstants as GPC

class Molecule(CT.ClassTools):

    def __init__(self, molecule, verbose = 0, **kwargs):
        """
        
        Arguments
        ---------
        molecule : str
            The name of the molecule
        """
        self.verbose = verbose
        
        verbose = GPF.print_vars(function_name = "GPMolecule.Molecule.__init__()", function_vars = vars(), verbose = verbose, self_verbose = self.verbose)   

        self.molecule = molecule
        
        props = GPC.molecule_properties(molecule, invalid = "error")
        
        self.molecule_id = props["id"]
        self.aliases = props["aliases"]
        self.formula = props["formula"]
        self.name = props["name"]
        self.molecular_mass = props["molecular_mass"]