import importlib
import pandas

import GPFunctions as GPF

importlib.reload(GPF)

def import_df_from_Excel(paf, sheetname, **kwargs):
    
    with open(paf, "rb") as F:
        df = pandas.read_excel(F, sheetname, **kwargs)
        
    return df
    
def import_df_from_csv(paf, **kwargs):
    
    with open(paf, "rb") as F:
        df = pandas.read_csv(F, **kwargs)
        
    return df


def merge_dynamic_data(df, df_dynamic, verbose = 0):
    """
    
    
    """
    verbose = GPF.print_vars(function_name = "GPImport.merge_dynamic_data()", function_vars = vars(), verbose = verbose, self_verbose = 0)  
    
    if df is None:
        raise ValueError("GPImport.merge_dynamic_data(): df can not be None.")

    df_rows, df_cols = df.shape
    
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
    