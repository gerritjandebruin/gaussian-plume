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












if __name__ == '__main__': 
    lat = 53.2835083
    lon = 6.30388
    latR = 53.28375
    lonR = 6.3024917
    wind_direction = 0

    latlon2dlatdlon(lat, lon, latR, lonR)