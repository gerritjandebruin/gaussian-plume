import warnings

import numpy
import matplotlib 
import matplotlib.pyplot as plt


def make_numpy_ndarray(val):
    """
    make a numpy.ndarray out of val, used by make_coordinates()
    
    Types of val that are accepted:        
    
    - int, float, string: make it a list and then numpy.ndarray.
    - list: make it a numpy.ndarray
    - tuple: convert to a list, then numpy.ndarray
    - numpy.ndarray: return directly
    
    Not accepted:
    
    - dict
    
    Notes
    -----
    
    - 2013-03-17/RB: started
    - 2019-02-14/RB: changed call to DEBUG with a simple print statement
    """
            
    if type(val) == numpy.ndarray:
        return val
    elif type(val) == list:
        return numpy.array(val)
    elif type(val) == dict:
        print("Value shouldn't be a dict or tuple")
        return False
    elif type(val) == tuple:
        return numpy.array(list(val))
    else:
        return numpy.array([val])  
        

def find_longest_list(*kwargs):

    """
    Helper function to find the longest in a series of lists.
    It does not check if it is actually a list.
    Used by make_coordinates()
    
    Notes
    -----
    
    - 2013-03-17/RB: started
    
    """
    
    length = 0
    
    for l in kwargs:        
        temp = len(l)
        if temp > length:
            length = temp
    
    return length


def make_coordinates(inch_per_unit, x_units, y_units, left, bottom, width, 
height, flag_verbose = False):
    
    """
    Simplifies formatting of plots. 
 
    matplotlib.figure.add_axes() requires coordinates (left, bottom, width, 
    height) for each axes instance. The values are between 0 and 1. There are 
    two problems. 
    
    First is that the aspect ratio may be off. If the figure is a rectangle and 
    the subplot is 0.5 wide and 0.5 high, the subplot is also a rectangle. 
    Second is that if the figure size changes all the carefully planned margins 
    are lost. 
    
    This function works with units. The x-axis is x_units long. Each unit has a 
    defined length inch_per_unit. The left edges are at [left]. This solves the 
    two problems. If your plot is N units wide and N units high, it will be a 
    square. When you resize the figure (change x_units) the margins, which are 
    in units, will remain the same.     
    
    Arguments
    ---------
    
    inch_per_unit : number 
        used to scale to inches
    x_units, y_units : number 
        width and height of the figure, in units
    left, bottom, width, height : numpy.ndarray 
        with ints and/or floats, also accepts list or int or float) the positions of the axes. The longest list determines the number of plots. Shorter lists are cycled. 
    
    Returns
    -------
    figsize : tuple
        a tuple that is accepted by plt.figure(figsize = figsize)
    coords : list with tuples 
        a list with tuples with (l,b,w,h) for the axes. The tuples are accepted by fig.add_axes((l,b,w,h)). 

   
    Examples
    --------

    1. Three plots next to each other. 
    
    ::
    
        01234567
        1 x  x x
        0xxxxxxx

        x_units = 8
        y_units = 3
        left = [1,3,6]  #
        bottom = 1      # [1], [1,1], [1,1,1] 
                        # not [1,1,1,1], that gives extra subplot
        width = [1,2]   # [1,2,1]
        height = 1      # [1], [1,1], [1,1,1]
    
    
    2. Four equally sized and spaced plots.
    
    ::
    
        01234
        3 x x
        2xxxx
        1 x x 
        0xxxx
        
        inch_per_unit = 1.0
        x_units = 5
        y_units = 5
        left = [1,3]        # [1,3,1,3]
                            # not [1,3,1], that would give: [1,3,1,1]
        bottom = [3,3,1,1]  #
        width = 1           # [1], [1,1], [1,1,1], [1,1,1,1]
        height = 1          # [1], [1,1], [1,1,1], [1,1,1,1]
    

    3. A complex arrangement. All coordinates are explicitly given. 
    
    ::
        
        01234567
        6   x  x
        5   x  x
        4xxxx  x
        3  xxxxx
        2  x   x
        1  x   x
        0xxxxxxx   

        x_units = 8
        y_units = 8
        left = [1,5,1,4]
        bottom = [5,4,1,1]
        width = [3,2,2,3]
        height = [2,3,3,2]    
    
    
    
    Notes
    -----
    
    - 2013-03-17/RB: started   
    
     
    """ 
    # calculate figure size
    figsize = (x_units * inch_per_unit, y_units * inch_per_unit)

    # change all values to values between 0 and 1
    left = make_numpy_ndarray(left) / x_units
    bottom = make_numpy_ndarray(bottom) / y_units
    width = make_numpy_ndarray(width) / x_units
    height = make_numpy_ndarray(height) / y_units
    
    # find longest list, determines number of sub plots
    N = find_longest_list(left, bottom, width, height)
    
    # determine the coordinates
    coords = []
    for i in range(N):
        
        l = left[i % len(left)]
        b = bottom[i % len(bottom)]
        w = width[i % len(width)]
        h = height[i % len(height)]
        
        coords.append((l,b,w,h))
        
    return figsize, coords



    
def figure_sizes(name):
    """
    Returns a dictionary with the coordinates for standard figure sizes. 
    
    Arguments
    ---------
    name : str {"standard", "wide", "A4_landscape", "A4_portrait"}
        Name of the size.
    
    """
    if name == "wide":
        f = {"u": 1/2.54, "fig_w": 25, "fig_h": 15, "l": 1.8, "b": 1.2, "ax_w": 22.5, "ax_h": 13}
    elif name == "A4_landscape":
        f = {"u": 1/2.54, "fig_w": 29.7, "fig_h": 21.0, "l": 1.8, "b": 1.2, "ax_w": 27.2, "ax_h": 19}
    elif name == "A4_portrait":
        f = {"u": 1/2.54, "fig_w": 21.0, "fig_h": 29.7, "l": 1.8, "b": 1.2, "ax_w": 18.5, "ax_h": 27.7}
    elif name in ["standard", "std", "normal"]:
        f = {"u": 1/2.54, "fig_w": 20, "fig_h": 15, "l": 1.8, "b": 1.2, "ax_w": 17.5, "ax_h": 13}
    else:
        warnings.warn("Unknown size format ({:}), use 'standard', 'wide', 'A4_landscape', or 'A4_portrait'. Will use default size.".format(name))
        f = {"u": 1/2.54, "fig_w": 20, "fig_h": 15, "l": 1.8, "b": 1.2, "ax_w": 17.5, "ax_h": 13} 
    return f



def make_figures(figures, label = False):
    """
    Make a list with figures and axes. 
    
    Arguments
    ---------
    figures : list  
        List with a dictionary with sizes, or a name for a pre-defined format. 
    label : bool (False)
        Label the numbers of the figures and axes, handy for debugging.
        
    Notes
    -----
    Predefined formats are: "standard" (25x15 cm), "wide" (29.7x21 cm), "A4_landscape", "A4_portrait". An unknown string will return a warning and the standard size.
    
    The dictionary contains:
    
    - `u`: units (optional). Use 1 for inches (default) and 1/2.54 for cm. The origin is that it means 'inch per unit'. 
    - `fig_w`: width of the figure
    - `fig_h`: height of the figure
    - `l`: left side of the axis
    - `b`: bottom of the axis
    - `ax_w`: width of the axis
    - `ax_h`: height of the axis
    - `twinx`: (optional) list with y axes to be doubled 
    - `twiny`: (optional) list with x axes to be doubled 
    
    For `twinx` and `twiny` the axis that is doubled is used. It is inserted after the original axis. 
    
    ::
        figures = [
            {"u": 1/2.54, "fig_w": 20, "fig_h": 15, "l": 1.8, "b": [5, 1.2], "ax_w": 17.5, "ax_h": [6,3], "twinx": [0]},  
        ]

    """

    if type(figures) == dict:
        figures = [figures]

    n_fig = len(figures)
        
    fig = [0] * n_fig
    ax = [0] * n_fig    
    
    for fig_i, f in enumerate(figures):
    
        if type(f) == str:
            f = figure_sizes(f)
        
        if "u" not in f:
            f["u"] = 1/2.54
    
        figsize, coords = make_coordinates(f["u"], f["fig_w"], f["fig_h"], f["l"], f["b"], f["ax_w"], f["ax_h"])
        
        n_ax = len(coords)
        
        if "twiny" in f:
            n_ax += len(f["twiny"])
            for i in f["twiny"]:
                coords.insert(i+1, "twiny")          
        
        if "twinx" in f:
            n_ax += len(f["twinx"])
            for i in f["twinx"]:
                coords.insert(i+1, "twinx")

        fig[fig_i] = plt.figure(figsize = figsize)
        ax[fig_i] = [0] * n_ax

        for ax_i in range(n_ax):
            if coords[ax_i] == "twinx":
                ax[fig_i][ax_i] = ax[fig_i][ax_i-1].twinx()
            elif coords[ax_i] == "twiny":
                ax[fig_i][ax_i] = ax[fig_i][ax_i-1].twiny()
            else:
                ax[fig_i][ax_i] = fig[fig_i].add_axes(coords[ax_i])

    if label:
        for fig_i in range(len(fig)):
            fig[fig_i].suptitle("Figure = {:}".format(fig_i))
            for ax_i in range(len(ax[fig_i])):
                ax[fig_i][ax_i].set_xlabel("Axis = {:}".format(ax_i))
                ax[fig_i][ax_i].set_ylabel("Axis = {:}".format(ax_i))
                
                
    return fig, ax


    
if __name__ == '__main__': 
    pass
    



 