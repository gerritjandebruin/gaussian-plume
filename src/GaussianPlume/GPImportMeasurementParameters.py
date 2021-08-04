"""


"""

import importlib
import pathlib
import numpy
import pandas

def import_measurement_parameters_txt(paf):
    """
    
    
    """
    
    parameters = {}
    array = []
    with open(paf, "r") as F:
        for line in F:
            parse_lines_txt(line, parameters)            
    
    print(parameters)



def parse_lines_txt(line, parameters, array):
    """
    
    
    """
    key, value = line.split(":")

    # remove white spaces at start and end of the string
    key = key.strip()
    value = value.strip()
    
    if value == "start":
        pass

    parameters[key] = value
    
    

def import_measurement_parameters_excel(paf, fixed_parameters = True, dynamic_parameters = True):
    """
    
    
    Arguments
    ---------
    paf : pathlib.Path
        Path and filename of the Excel file with parameters
    fixed_parameters : Bool (True)
        Read the fixed parameters sheet in the Excel file
    dynamic_parameters : Bool (True)
        Read the dynamic parameters sheet in the Excel file
    
    """
    
    with open(paf, "rb") as F:
        if fixed_parameters:
            df_fixed = pandas.read_excel(F, "fixed parameters", index_col = 0, header = None) 
        if dynamic_parameters:
            df_dynamic = pandas.read_excel(F, "dynamic parameters", header = 0, parse_dates = ["datetime"]) 

    df_fixed = df_fixed.transpose().reset_index(drop = True)
            
    print(df_fixed)
    # print("---")
    # print(df_dynamic)
    # print(df_dynamic.dtypes)
    
    
    
    

    

    
    