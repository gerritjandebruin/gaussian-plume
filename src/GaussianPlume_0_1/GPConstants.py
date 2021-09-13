import warnings 
import numpy

latlon2dxdy_lon_conversion_factor = 6378137
latlon2dxdy_lat_conversion_factor = 6356752

deg2rad = numpy.pi / 180
rad2deg = 180 / numpy.pi

liter_per_mole_air = 22.36

sigma_ca = 0.53
sigma_cb = -0.22

def dispersion_constants(mode):
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

    if mode.lower() == "farm":
        dispersion = numpy.array([
            [0.82, 1.02 * 0.865, 0.21, 0.8],
            [0.53, 1.02 * 0.866, 0.18, 0.76],
            [0.35, 1.02 * 0.897, 0.15, 0.72],
            [0.23, 1.02 * 0.907, 0.13, 0.68],
            [0.15, 1.02 * 0.902, 0.11, 0.64],
            [0.096,1.02 * 0.902, 0.09, 0.6],
        ])
    elif mode.lower() in ["nogepa", "sea"]:
        dispersion = numpy.array([
            [1.36,  0.866, 0.23, 0.85],
            [0.768, 0.897, 0.22, 0.8],
            [0.47,  0.907, 0.2,  0.76],
            [0.359, 0.902, 0.15, 0.73],
            [0.238, 0.902, 0.12, 0.67],
            [0.2,   0.902, 0.1,  0.62],
        ])
    else:
        raise IndexError("Mode {:s} is invalid for dispersion_constants. Valid options are: 'farm', 'nogepa', 'sea'.".format(mode))
        
    return dispersion

implemented_molecules = ["ch4", "n2o", "no2", "no", "c2h6"]
        
def molecule_properties(molecule):
    """
    
    Arguments
    ---------
    molecule : string
        Name of the molecule
        
    Returns
    -------
    molecule_properties : dict
        A dictionary with molecule properties. 
    
    """
    molecule = molecule.lower()

    if molecule in ["methane", "ch4"]:
        return {
            "aliases": ["methane", "ch4"],
            "formula": "CH4",
            "name": "methane",
            "molecular_mass": 16,
        }
    elif molecule in ["n2o", "nitrous oxide"]:
        return {
            "aliases": ["n2o", "nitrous oxide"],
            "formula": "N2O",
            "name": "nitrous oxide",
            "molecular_mass": 44,
        }        
    elif molecule in ["no2", "nitrogen dioxide"]:
        return {
            "aliases": ["no2", "nitrogen dioxide"],
            "formula": "NO2",
            "name": "nitrogen dioxide",
            "molecular_mass": 46,
        }        
    elif molecule in ["no", "nitrogen oxide"]:
        return {
            "aliases": ["no", "nitrogen oxide"],
            "formula": "NO",
            "name": "nitrogen oxide",
            "molecular_mass": 30,
        }                
    # elif molecule in ["nox", "ethane"]:
        # return {
            # "formula": "C2H6",
            # "name": "ethane",
            # "molecular_mass": 30,
        # }  
    elif molecule in ["c2h6", "ethane"]:
        return {
            "aliases": ["c2h6", "ethane"],
            "formula": "C2H6",
            "name": "ethane",
            "molecular_mass": 30,
        }  
    # elif molecule in ["PM10"]:
        # return {
            # "formula": "PM10",
            # "name": "PM10",
            # "molecular_mass": 30,
        # }          
    else:
        warnings.warn("Molecule is not implemented")
        return None
        
        
        
        
        
if __name__ == '__main__': 
    dispersion = dispersion_constants("x")