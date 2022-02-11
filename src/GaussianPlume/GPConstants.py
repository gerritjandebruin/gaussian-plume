import warnings 
import numpy

latlon2dxdy_lon_conversion_factor = 6378137
latlon2dxdy_lat_conversion_factor = 6356752

deg2rad = numpy.pi / 180
rad2deg = 180 / numpy.pi

liter_per_mole_air = 22.36

sigma_ca = 0.53
sigma_cb = -0.22

def dispersion_constants(dispersion_mode):
    """
    Return the dispersion values. 
    
    Arguments
    ---------
    mode : string
        Name of the dispersion constant set. 
        
    Returns
    -------
    dispersion: a table with dispersion constants, where rows are stabilities. Each row consists of: dispersion factor Y, dispersion exponent Y, dispersion factor Z, dispersion exponent Z. 
    
    """

    if dispersion_mode.lower() == "farm":
        dispersion_constants = numpy.array([
            [0.82, 1.02 * 0.865, 0.21, 0.8],
            [0.53, 1.02 * 0.866, 0.18, 0.76],
            [0.35, 1.02 * 0.897, 0.15, 0.72],
            [0.23, 1.02 * 0.907, 0.13, 0.68],
            [0.15, 1.02 * 0.902, 0.11, 0.64],
            [0.096,1.02 * 0.902, 0.09, 0.6],
        ])
    elif dispersion_mode.lower() in ["nogepa", "sea"]:
        dispersion_constants = numpy.array([
            [1.36,  0.866, 0.23, 0.85],
            [0.768, 0.897, 0.22, 0.8],
            [0.47,  0.907, 0.2,  0.76],
            [0.359, 0.902, 0.15, 0.73],
            [0.238, 0.902, 0.12, 0.67],
            [0.2,   0.902, 0.1,  0.62],
        ])
    else:
        raise IndexError("Mode {:s} is invalid for dispersion_mode. Valid options are: 'farm', 'nogepa', 'sea'.".format(dispersion_mode))
        
    return dispersion_constants


def implemented_molecules():
    """
    List with molecule that are implemented. The order of the list has to match with the order of molecule_properties().
    
    """
    return [
            ["co2", "carbon dioxide"],
            ["methane", "ch4"],
            ["no", "nitrogen oxide"],
            ["nox"],
            ["n2o", "nitrous oxide"],
            ["no2", "nitrogen dioxide"],
            ["c2h6", "ethane"],
        ]
        
def molecule_properties(molecule, invalid = "warning"):
    """
    
    Arguments
    ---------
    molecule : string
        Name of the molecule
    invalid : string
        What do if `molecule` is invalid. It can be `error`, `none`, or `warning` (default and catch-all)
    
    Returns
    -------
    molecule_properties : dict
        A dictionary with molecule properties. 
    
    """

    if  molecule is None:
        if invalid == "error":
            raise ValueError ("GPConstants.molecule_properties(): None is not a valid name for a molecule")
        elif invalid == "none":
            return None
        else:
            warnings.warn("GPConstants.molecule_properties(): None is not a valid name for a molecule")
    
    molecule = molecule.lower()

    molecules = implemented_molecules()

    if molecule in molecules[0]:
        return {
            "id": "co2",
            "aliases": ["co2", "carbon dioxide"],
            "formula": "CO2",
            "name": "carbon dioxide",
            "molecular_mass": 44.009,
        }
    elif molecule in molecules[1] :
        return {
            "id": "ch4",
            "aliases": ["methane", "ch4"],
            "formula": "CH4",
            "name": "methane",
            "molecular_mass": 16,
        }
    elif molecule in molecules[2]:
        return {
            "id": "no",
            "aliases": ["no", "nitrogen oxide"],
            "formula": "NO",
            "name": "nitrogen oxide",
            "molecular_mass": 30,
        }  
    elif molecule in molecules[3]:
        return {
            "id": "nox",
            "aliases": ["nox"],
            "formula": "NOx",
            "name": "nitrogen oxides",
            "molecular_mass": 30,
        }   

    elif molecule in molecules[4]:
        return {
            "id": "n2o",
            "aliases": ["n2o", "nitrous oxide"],
            "formula": "N2O",
            "name": "nitrous oxide",
            "molecular_mass": 44,
        }        
    elif molecule in molecules[5]:
        return {
            "id": "no2",
            "aliases": ["no2", "nitrogen dioxide"],
            "formula": "NO2",
            "name": "nitrogen dioxide",
            "molecular_mass": 46,
        }        
    elif molecule in molecules[6] :
        return {
            "id": "c2h6",
            "aliases": ["c2h6", "ethane"],
            "formula": "C2H6",
            "name": "ethane",
            "molecular_mass": 30,
        }       
    else:
        if invalid == "error":
            raise ValueError ("GPConstants.molecule_properties(): {:} is not a valid name for a molecule".format(molecule))
        elif invalid == "none":
            return None
        else:
            warnings.warn("GPConstants.molecule_properties(): {:} is not a valid name for a molecule".format(molecule))
        
        
        
        
if __name__ == '__main__': 
    dispersion = dispersion_constants("x")