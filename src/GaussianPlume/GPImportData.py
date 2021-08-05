"""
Data comes in three forms:

* Measurement data: this is recorded often, typically automatically
* Dynamic parameters: parameters that change a few times during a measurement. Maybe the terrain roughness. 
* Static parameters: parameters that do no change during a measurement, for example the type of device used.  

Measurement data is similar to dynamic parameters, but changes more frequently. Measurement data is recorded automatically, dynamic parameters are typed into an Excel spreadsheet. Temperature may be an edge case. If it is recorded automatically, it is measurement data. If it is recorded twice during a measurement it is a dynamic parameter. If it is recorded only once, it is a static parameter. 

Dynamic and static parameters
=============================
Static parameters are stored in a sheet named `static parameters' (the sheet names are important). Column A contains the parameter names, column B the parameter values. If a parameter name or value is missing, it is ignored.

This data:

============ =======
Device       TNO XYZ
Operator      
Stack height 5
============ =======

Will be read as:

============ =======
Device       TNO XYZ
Stack height 5
============ =======

Dynamic parameters are stored in a sheet named "dynamic parameters". Column A contains a time stamp, the other columns the parameters. Row 1 contains the parameter names. The idea is that you only need to fill in the value of the parameter that has changed. If a value is missing, it will use the last valid value. If there is no last valid value it will be set to NaN. Note that data is not interpolated. 

This data:

================ ========= =========
datetime         Roughness Windspeed
================ ========= =========
02/08/2018 7:00            5
02/08/2018 9:40  C         
02/08/2018 10:33           11
02/08/2018 11:22 E          	
02/08/2018 12:25 F         16
================ ========= =========

Will be read as:

================ ========= =========
datetime         Roughness Windspeed
================ ========= =========
02/08/2018 7:00  **NaN**   5
02/08/2018 9:40  C         **5**
02/08/2018 10:33 **C**     11
02/08/2018 11:22 E         **11**	
02/08/2018 12:25 F         16
================ ========= =========

Note that if a dynamic parameter value is recorded only once, it effectively becomes a static parameter, but as explained in the Technical details, it is treated differently. 

Technical details
=================
Data is treated as numpy-arrays (ndarrays) or as a number (integer, float). Numpy works similar to Matlab. You can multiply two ndarrays of the same size, to get a ndarray with the same size. You can also multiply an ndarray with a number, to get an ndarray with the same size:

* distance (ndarray with size = n) / windspeed (ndarray with size = n) = time (ndarray with size = n)
* distance (number) / windspeed (ndarray with size = n) = time (ndarray with size = n)
* distance (ndarray with size = n) / windspeed (number) = time (ndarray with size = n)
* distance (number) / windspeed (number) = time (number)

Measurement data is an ndarray. A static parameter is a number. Dynamic parameters are changed into an ndarray of the same length as the measurement data. 


"""

import importlib
import pathlib
import numpy
import pandas
import warnings
    

def import_measurement_parameters_excel(paf, static_parameters = True, dynamic_parameters = True, verbose = 0):
    """
    Import an Excel file with measurement parameters.
    
    Arguments
    ---------
    paf : pathlib.Path
        Path and filename of the Excel file with parameters
    static_parameters : bool (True) or str
        Read the fixed parameters sheet in the Excel file. If this is a string, it will be used as the sheet name.
    dynamic_parameters : bool (True) or str
        Read the dynamic parameters sheet in the Excel file. If this is a string, it will be used as the sheet name.
    
    Returns
    -------
    Pandas dataframe or None
        DataFrame with static parameters. None if static_parameters is False
    Pandas dataframe or None
        DataFrame with dynamic parameters.None if dynamic_parameters is False
    
    Raises
    ------
    ValueError
        If the sheet name is incorrect.
    UserWarning
        If the file is not found at the paf. 
    
    """
    if verbose > 1:
        print("GPImportData.import_measurement_parameters_excel()")
    if verbose > 2:
        print("    paf (path and filename): {:}".format(paf))
        print("    static_parameters: {:}".format(static_parameters))
        print("    dynamic_parameters: {:}".format(dynamic_parameters))
    
    if paf.exists() == False:
        warnings.warn("GPImportData.import_measurement_parameters_excel(): parameter file does not exist (at this location): {:}".format(paf))
        return None, None
    
    with open(paf, "rb") as F:
    
        if static_parameters:
            if type(static_parameters) == str:
                sheetname = static_parameters
            else:
                sheetname = "static parameters"
        
            df_static = pandas.read_excel(F, sheetname, index_col = 0, header = None) 
            
            # transpose data and make a new index
            df_static = df_static.transpose()
            df_static = df_static.reset_index(drop = True)
            
            # remove parameters without a value
            for cl in df_static.columns:
                if pandas.isna(df_static.loc[0,cl]): 
                    df_static.drop(cl, axis=1, inplace = True)            
            
        else:
            df_static = None

        if dynamic_parameters:
            if type(dynamic_parameters) == str:
                sheetname = dynamic_parameters
            else:
                sheetname = "dynamic parameters"        
        
            df_dynamic = pandas.read_excel(F, sheetname, header = 0, parse_dates = ["datetime"]) 
            
            # forward fill data
            df_dynamic.fillna(method = "ffill", inplace = True) 
        else:
            df_dynamic = None
          
    return df_static, df_dynamic
            

    
def import_measurement_data(paf):
    """


    """
    
    
    

    

    
    