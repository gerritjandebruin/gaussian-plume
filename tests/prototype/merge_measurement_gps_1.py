import pathlib

import numpy
import matplotlib 
import matplotlib.pyplot as plt

import pandas

# 19, 20, 21, 22, 24, 25, 26, 27, 28, 29, 30,1, 2,3,4 , 5, 6, 9, 10, 11, 12, 13, 14, 15, 16, 17
# niet: 23, 7,8

reload_measurement_to_pickle = True

measurement_paf = pathlib.Path(r"C:\Measurements\CLINSH\Plumes_data_Campagne2.csv")
measurement_pickle_paf = pathlib.Path(r"C:\Measurements\CLINSH\Plumes_data_Campagne2.pickle")

if reload_measurement_to_pickle or measurement_pickle_paf.exists() == False:
    with open(measurement_paf, "rb") as F:
        df = pandas.read_csv(F, header = 0, delimiter = ",", parse_dates = [0], index_col = 0) 
    df.to_pickle(measurement_pickle_paf)

else:   
    df = pandas.read_pickle(measurement_pickle_paf)


print(df.dtypes)

pickle_paf = pathlib.Path(r"C:\Measurements\CLINSH\AIS\GPS_20191119.pickle")
gps_df = pandas.read_pickle(pickle_paf)

print(gps_df.dtypes)

# result = df.join(gps_df, how="inner")
result = pandas.merge(df, gps_df, left_index=True, right_index=True, how="inner")

print(result)