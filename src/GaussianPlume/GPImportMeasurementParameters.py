import importlib

import numpy

def import_measurement_parameters(paf):
    """
    
    
    """
    
    parameters = {}
    array = 
    with open(paf, "r") as F:
        for line in F:
            parse_lines(line, parameters)            
    
    print(parameters)



def parse_lines(line, parameters, array):
    """
    
    
    """
    key, value = line.split(":")

    # remove white spaces at start and end of the string
    key = key.strip()
    value = value.strip()
    
    if value == "start":
        

    parameters[key] = value
    
    
    
    
    
    

    

    
    