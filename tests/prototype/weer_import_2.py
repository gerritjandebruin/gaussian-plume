import pathlib

import numpy
import matplotlib 
import matplotlib.pyplot as plt

import pandas


plt.close("all")


weather_path = pathlib.Path(r"C:\Measurements\CLINSH\Vaisala")

weather_pickle_paf = weather_path.joinpath("weather.pickle")

wx_df = pandas.read_pickle(weather_pickle_paf)


measurement_pickle_paf = pathlib.Path(r"C:\Measurements\CLINSH\Plumes_data_Campagne2.pickle")

mess_df = pandas.read_pickle(measurement_pickle_paf)

result = pandas.merge(mess_df, wx_df, left_index=True, right_index=True, how="inner")


# weather_filename = [
    # pathlib.Path(r"C:\Measurements\CLINSH\Vaisala\VaisalaWXT201911301451.txt"),
    # pathlib.Path(r"C:\Measurements\CLINSH\Vaisala\VaisalaWXT201912011451.txt"),
    # pathlib.Path(r"C:\Measurements\CLINSH\Vaisala\VaisalaWXT201912021451.txt"),
    # pathlib.Path(r"C:\Measurements\CLINSH\Vaisala\VaisalaWXT201912031451.txt"),
    # pathlib.Path(r"C:\Measurements\CLINSH\Vaisala\VaisalaWXT201912041451.txt"),
    # pathlib.Path(r"C:\Measurements\CLINSH\Vaisala\VaisalaWXT201912051451.txt"),
    # pathlib.Path(r"C:\Measurements\CLINSH\Vaisala\VaisalaWXT201912061451.txt"),
    # pathlib.Path(r"C:\Measurements\CLINSH\Vaisala\VaisalaWXT201912071451.txt"),
    # pathlib.Path(r"C:\Measurements\CLINSH\Vaisala\VaisalaWXT201912081451.txt"),
    # pathlib.Path(r"C:\Measurements\CLINSH\Vaisala\VaisalaWXT201912091451.txt"),
    # pathlib.Path(r"C:\Measurements\CLINSH\Vaisala\VaisalaWXT201912101451.txt"),
    # pathlib.Path(r"C:\Measurements\CLINSH\Vaisala\VaisalaWXT201912111451.txt"),
    # pathlib.Path(r"C:\Measurements\CLINSH\Vaisala\VaisalaWXT201912121451.txt"),
    # pathlib.Path(r"C:\Measurements\CLINSH\Vaisala\VaisalaWXT201912131451.txt"),
    # pathlib.Path(r"C:\Measurements\CLINSH\Vaisala\VaisalaWXT201912141451.txt"),
    # pathlib.Path(r"C:\Measurements\CLINSH\Vaisala\VaisalaWXT201912151451.txt"),
    # pathlib.Path(r"C:\Measurements\CLINSH\Vaisala\VaisalaWXT201912161451.txt"),
# ]

# path = pathlib.Path(r"C:\Measurements\CLINSH\Vaisala")


# usecols = ["Datetime", "WD", "WS", "Pa avg", "Ta avg"]

# frames = []
# for paf in weather_filename:

    # with open(paf, "rb") as F:
        # frames.append( pandas.read_csv(F, delimiter = ",", parse_dates = [0], index_col = 0, usecols = usecols, dayfirst = True) )
    
# wx_df = pandas.concat(frames)
# wx_df = wx_df.resample("S").interpolate()

# paf = path.joinpath("weather.pickle")
# wx_df.to_pickle(paf)


# print(wx_df)
# dates = numpy.arange('2019-11-30', '2019-12-17', dtype='datetime64[D]')

# for date in dates:
    # idx = numpy.where(wx_df.index.date == date)[0]

    # filename = "{:s}_weather.pickle".format(numpy.datetime_as_string(date))
    # paf = path.joinpath(filename)
    # print(wx_df.iloc[idx,:])
    # wx_df.iloc[idx,:].to_pickle(paf)


# 








# plt.plot(df.index, df["WS"])
# plt.plot(df.index, df["Sm avg"])


# plt.plot(df.index, df["WD"])
# plt.plot(df.index, df["Dm avg"])

# plt.show()