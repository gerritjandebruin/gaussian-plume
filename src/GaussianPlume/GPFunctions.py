import importlib
import numpy



import GPConstants as GPC

importlib.reload(GPC)

def latlon2dlatdlon(lat, lon, latR, lonR):
    """
    Calculate the distance in meter in north-south and east-west direction for two coordinates. 
    
    `lat` and `lon` are the coordinates of a point. `latR` and `lonR` are the coordinates of a reference. 
    
    Latitude is the north-south position (positive is north). Longitude the east-west position (positive is east). 
    
    Input can be a number, ndarray or a list. Output is a number or a ndarray. A list is converted to an ndarray. 
    
    Arguments
    ---------
    lat : number, ndarray, list
        Latitude
    lon : number, ndarray, list
        Longitude
    latR : number, ndarray, list
        Latitude of the reference
    lonR : number, ndarray
        Longitude of the reference
    
    Returns
    -------
    dlat : number or ndarray
        If the point is north of the reference, it is positive
    dlon : number or ndarray
        If the point is east of the reference, it is positive
    
    
    """
    if type(lat) == list:
        lat = numpy.array(lat)
    if type(lon) == list:
        lon = numpy.array(lon)
    if type(latR) == list:
        latR = numpy.array(latR)
    if type(lonR) == list:
        lonR = numpy.array(lonR)        
    
    dlat = numpy.sin((lat - latR) * GPC.deg2rad) * GPC.latlon2dxdy_lon_conversion_factor
    dlon = numpy.cos(lat * GPC.deg2rad) * numpy.sin((lon - lonR) * GPC.deg2rad) * GPC.latlon2dxdy_lat_conversion_factor 
    
    return dlat, dlon 





def dlatdlon2dxdy(dlatS, dlonS, dlatM, dlonM, wind_direction):
    """
    Calculate dx and dy.     
    
    dlatS : number, ndarray, list
        North-south distance between source and reference, where positive means the source is north of the reference
    dlonS : number, ndarray, list
        East-west distance between source and reference, where positive means the source is east of the reference
    dlatM : number, ndarray, list
        North-south distance between measurement and reference, where positive means the measurement is north of the reference
    dlonM : number, ndarray, list
        East-west distance between measurement and reference, where positive means the measurement is east of the reference
    wind_direction : number, ndarray, list
        Direction from which the wind comes, in degrees
    
    
    """
    if type(dlatS) == list:
        dlatS = numpy.array(dlatS)
    if type(dlonS) == list:
        dlonS = numpy.array(dlonS)
    if type(dlatM) == list:
        dlatM = numpy.array(dlatM)
    if type(dlonM) == list:
        dlonM = numpy.array(dlonM)        
    if type(wind_direction) == list:
        wind_direction = numpy.array(wind_direction)

 
    
    
    dx = (dlatS - dlatM) * numpy.cos(wind_direction * GPC.deg2rad) + (dlonS - dlonM) * numpy.sin(wind_direction * GPC.deg2rad)
    dy = (dlatS - dlatM) * numpy.sin(wind_direction * GPC.deg2rad) - (dlonS - dlonM) * numpy.cos(wind_direction * GPC.deg2rad)
    
    return dx, dy


def get_dispersion_constants(mode):
    """
    Select the right dispersion mode.
    
    Argument
    --------
    mode : string
        The required mode.
        
    Returns
    -------
    dispersion_constants : ndarray
        A table with constants. Rows are the stability classes, columns the factors. 
    
    """
    return GPC.dispersion_constants(mode)


def get_molecule_properties(molecule):
    """

    Get a dictionary with molecule properties. 
    
    Argument
    --------
    molecule : string
        Name of the molecule. 
        
    Returns
    -------
    molecule_properties : dict
        Dictionary with molecule properties
    
    """
    return GPC.molecule_properties(molecule)


def calculate_Tc(dx, wind_speed):   
    """
    Calculate the travel time in seconds(?)
    
    Arguments
    ---------
    dx : number
        Distance between the source and the measurement in meters. 
    wind_speed : number
        Wind speed in m/s
    
    Returns
    -------
    travel_time : number
        Travel time in seconds. 
    
    """
    return dx / (wind_speed)


def calculate_sigma(dx, z0, Tc, ca, cb, dispersion_constants, stability):
    """
    Calculate the plume width and height at dx. 
    
    
    
    Arguments
    ---------
    dx : number
        Distance between the source and the measurement in meter
    z0 : number
        Source height in meter
    Tc : number
        Travel time between source and measurement in seconds
    ca : number
        Some exponent
    cb : number
        Some exponent
    dispersion_constants : ndarray
        Table with dispersion constants
    stability : number
        Index 0-5 for stability, where 0 is most stable.
    
    Returns
    -------
    sigma_y, sigma_z : number
        Values for the disk diameter in y and z direction.
    
    """
    
    sigma_y = dispersion_constants[stability,0] * dx**dispersion_constants[stability,1] * z0**0.2 * Tc**0.35
    sigma_z = dispersion_constants[stability,2] * dx**dispersion_constants[stability,3] * (10*z0)**(ca * dx**cb)
    
    return sigma_y, sigma_z





def calculate_concentration(Qs, wind_speed, sigma_y, sigma_z, dy, Zr, Hs, Hm, molecular_mass):
    """
    Calculate the concentration
    
    
    Arguments
    ---------
    Qs : number
        Source strength in gram / second
    wind_speed : number
        Wind speed in m/s.
    sigma_y : number
        Plume width in m. 
    sigma_z : number
        Plume height in m. 
    dy : number
        Distance perpendicular. 
    Zr : number
        Height of the measurement in m. 
    Hs : number
        Height of the source in m. 
    Hm : number
        Height of the mixing layer in m. 
    molecular_mass : number
        Molecular mass in g/mol. 
        
    """

    A = Qs / (2 * numpy.pi * wind_speed * sigma_y * sigma_z)
    B = numpy.exp(-dy**2 / (2 * sigma_y**2))
    C = 2 * sigma_z**2
    D = numpy.exp(-(Zr - Hs)**2 / C)
    E = numpy.exp(-(Zr + Hs)**2 / C)
    F = numpy.exp(-(Zr - (2 * Hm - Hs))**2 / C)    
    
    return GPC.liter_per_mole_air * 1e6 * A * B * (D + E + F) / molecular_mass








if __name__ == '__main__': 
    lat = 53.2835083
    lon = 6.30388
    latR = 53.28375
    lonR = 6.3024917
    wind_direction = 0

    latlon2dlatdlon(lat, lon, latR, lonR)