"""
ClassTools

Some very general tools for working with classes. Most notably is a way to print a class neatly.

"""

import numpy
import pandas
import time

##############
# CLASSTOOLS #
##############

class ClassTools(object):
    """
    A way to print the whole class in one go. It prints the key and the value. Adapted from 'Learning Python', 4th edition, by Mark Lutz.
    
    """

    def gatherAttrs(self):
        """
        Gathers the attributes of a class, so that they can be printed.
        
        Notes
        -----
        
        - 2011-??-??/RB: copied function from book
        """
        attrs=[]
        for key in sorted(self.__dict__):
            attrs.append("\t%20s  =  %s\n" % (format_key(key), format_print(getattr(self, key))))
        return " ".join(attrs)

    def __str__(self):
        """
        Defines that the class can be printed as a string.

        Notes
        -----
        
        - 2011-??-??/RB: copied function from book
        """
        return "[%s:\n %s]" % (self.__class__.__name__, self.gatherAttrs())


       
def format_print(var):
    """
    format_print is a helper function for the gatherAttrs function to print variables in a neat way. There are a few situations:
    
    1. var is not a list or an ndarray, it will print the value. This include tuples
    2. var is an ndarray, the shape will be printed
    3. var is a time. It will return a readable string with the time.
    4. the var is a list, it will do recursion to print either 1 or 2
        
    Examples
    --------
    - 42          => 42
    - "car"       => "car"
    - [1,2]       => [1,2]
    - ndarray     => shape
    - [1,ndarray] => [1, shape]
    
    
    Notes
    ---------
    
    - 2011-??-??/RB: started function  
    
    """
    # list
    if type(var) == list:
        typ = list(range(len(var)))
        for i in range(0, len(var)):
            typ[i] = (format_print(var[i]))
        return typ
    # ndarray
    # memmap is when the array is imported a file, but not actually read until it is used (saves a lot of time for large data sets). 
    elif type(var) == numpy.ndarray or type(var) == numpy.core.memmap:
        a = numpy.shape(var)
        if len(a) == 1: 
            return str(a[0]) + " x 1"
        else:
            s = "{a}".format(a = a[0])
            a = a[1:]
            for _a in a:
                s = "{s} x {a}".format(s = s, a = _a)
            return s
    elif type(var) == pandas.core.frame.DataFrame:
        s = "Pandas DataFrame {:}".format(var.shape)
        return s
    elif type(var) == pandas.core.frame.Series:
        s = "Pandas Series {:}".format(var.shape)
        return s        
    # time
    elif type(var) == time.struct_time: 
        var = time.strftime("%a, %d %b %Y %H:%M:%S", var)
        return var
    elif type(var) == float:
        return round(var, 2)
    elif type(var) == numpy.float64:
        return round(var, 2)
    # the rest
    else:
        return var



def format_key(key):
    """
    Strips keys from _. These keys are semi-protected and should be run through the getter and setter methods.
    
    Notes
    -----
    
    - 20??-??-??/RB: started function
    """
    if key[0] == "_":
        key = key[1:]

    return key









