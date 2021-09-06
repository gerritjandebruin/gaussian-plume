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

import GPFunctions as GPF
    

def import_measurement_parameters_excel_helper(paf, static_parameters = True, dynamic_parameters = True, verbose = 0):
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
    verbose = GPF.print_vars(function_name = "GPImportData.import_measurement_parameters_excel_helper()", function_vars = vars(), verbose = verbose, self_verbose = 0)
    
    if type(paf) == str:
        # for lazy people 
        warnings.warn("GPImportData.import_measurement_parameters_excel_helper(): please give paf (path and filename) as pathlib path, not as string: {:}".format(paf))
        paf = pathlib.Path(paf)
    
    if paf.exists() == False:
        warnings.warn("GPImportData.import_measurement_parameters_excel_helper(): parameter file does not exist (at this location): {:}".format(paf))
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
            
            # reduces memory usage, especially when added to measurement data
            df_static = df_static.astype("category")
            
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
            
            # reduces memory usage, especially when added to measurement data
            df_dynamic = df_dynamic.astype("category")
        else:
            df_dynamic = None
          
    return df_static, df_dynamic
            


def import_measurement_parameters_excel(paf, static_parameters = True, dynamic_parameters = True, verbose = 0):
    """
    Import a list with Excel files with measurement parameters.
    
    Arguments
    ---------
    paf : pathlib.Path
        A list with path and filename of the Excel file with parameters
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

    
    """
    verbose = GPF.print_vars(function_name = "GPImportData.import_measurement_parameters_excel()", function_vars = vars(), verbose = verbose, self_verbose = 0)
    
    if type(paf) != list:
        paf = [paf]
    
    df_static = None
    df_dynamic = None
    for p in paf:
        _df_static, _df_dynamic = import_measurement_parameters_excel_helper(p, static_parameters = static_parameters, dynamic_parameters = dynamic_parameters, verbose = verbose)
        
        if _df_static is not None:
            if df_static is None:
                df_static = _df_static
            else:
                df_static = pandas.concat([df_static, _df_static], axis = 1)
                df_static = df_static.reset_index(drop = True)
            
        if df_dynamic is None:
            df_dynamic = _df_dynamic                
        else:
            df_dynamic = pandas.concat([df_dynamic, _df_dynamic]) 

    if df_static is not None:
        df_static = df_static.loc[:,~df_static.columns.duplicated()]
        lower_case_column_names(df_static)

    if df_dynamic is not None:
        lower_case_column_names(df_dynamic)
    
    return df_static, df_dynamic
    
    
def import_measurement_data_helper(paf, verbose = 0):
    """
    Import csv with measurement data.
    
    Arguments
    ---------
    paf : pathlib.Path
        Path and filename of the Excel file with parameters
    
    Returns
    -------
    Pandas dataframe or None
        DataFrame with measurement data

    """
    verbose = GPF.print_vars(function_name = "GPImportData.import_measurement_data_helper()", function_vars = vars(), verbose = verbose, self_verbose = 0)  

    if type(paf) == str:
        # for lazy people 
        warnings.warn("GPImportData.import_measurement_data_helper(): please give paf (path and filename) as pathlib path, not as string: {:}".format(paf))
        paf = pathlib.Path(paf)

    if paf.exists() == False:
        warnings.warn("GPImportData.import_measurement_data_helper(): measurement file does not exist (at this location): {:}".format(paf))
        return None

    with open(paf, "rb") as F:
        df = pandas.read_csv(F, header = 0, parse_dates = ["datetime"]) 
    
    return df

    
def import_measurement_data(paf, verbose = 0):
    """
    Import a list with csv's with measurement data.
    
    Arguments
    ---------
    paf : pathlib.Path
        Path and filename of the Excel file with parameters
    
    Returns
    -------
    Pandas dataframe or None
        DataFrame with measurement data

    """
    verbose = GPF.print_vars(function_name = "GPImportData.import_measurement_data()", function_vars = vars(), verbose = verbose, self_verbose = 0)  
    
    if type(paf) != list:
        paf = [paf]
    
    df = None
    for p in paf:
        _df = import_measurement_data_helper(p, verbose = 0)
        
        if df is None:
            df = _df
        else:
            if numpy.all(df.columns == _df.columns):
                df = pandas.concat([df, _df])
            else:
                raise pandas.errors.InvalidIndexError
            
    df = df.reset_index(drop = True)
    
    lower_case_column_names(df)
    
    return df 
    
    
    
def merge_measurement_static_dynamic_df(df, df_static, df_dynamic, verbose = 0):
    """
    
    
    """
    verbose = GPF.print_vars(function_name = "GPImportData.merge_measurement_static_dynamic_df()", function_vars = vars(), verbose = verbose, self_verbose = 0)  
    
    if df is None:
        print("GPImportData.merge_measurement_static_dynamic_df(): df can not be None.")
        raise ValueError

    df_rows, df_cols = df.shape
        
    if df_static is not None:
        df_s_rows, df_s_cols = df_static.shape
        # add the static parameters. Concat adds it as a row to the end, it is then backfilled. Finally the last (added) row is removed. 
        df_static = df_static.astype("category")
        df = pandas.concat([df, df_static]).reset_index(drop = True)
        df.fillna(method = "bfill", inplace = True) 
        df.drop(index = df_rows, axis = 0, inplace = True)
    
    if df_dynamic is not None:
    
        df_d_rows, df_d_cols = df_dynamic.shape

        # make a new dataframe, size is the number of columns in df_dynamic, minus to column for datetime
        df_times = pandas.to_datetime(df.loc[:,"datetime"])
        df_d_times = pandas.to_datetime(df_dynamic.loc[:,"datetime"])
        df_d_colnames = df_dynamic.columns

        temp = numpy.zeros((df_rows, df_d_cols-1))
        temp[:,:] = numpy.nan

        temp_df = pandas.DataFrame(temp, columns = df_d_colnames[1:])

        for t_i, t in enumerate(df_d_times):
            idx = numpy.where(df_times > t)[0][0]
            temp_df.loc[idx, df_d_colnames[1:]] = df_dynamic.loc[t_i, df_d_colnames[1:]]

        temp_df.fillna(method = "ffill", inplace = True) 
        temp_df = temp_df.astype("category")
        df = pandas.concat([df, temp_df], axis = 1)
        
        lower_case_column_names(df)
    
    return df
    
    
    
def lower_case_column_names(df):

    old_col_names = df.columns
    new_col_names = []
    for old_name in old_col_names:
        new_col_names.append(old_name.lower())
    df.columns = new_col_names

    
    
    
    
    
    
    
    