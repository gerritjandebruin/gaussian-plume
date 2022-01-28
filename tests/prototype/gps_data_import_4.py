"""
Data is stored in rows with various number of colums. 
The length of the header line is not always correct.
Some timestamps are missing or double. 

"""


import pathlib

import numpy
import matplotlib 
import matplotlib.pyplot as plt

import pandas

reload_measurement_to_pickle = False
reload_weather_to_pickle = False

output_path = pathlib.Path(r"C:\Measurements\CLINSH\output")

measurement_paf = pathlib.Path(r"C:\Measurements\CLINSH\Plumes_data_Campagne2.csv")
measurement_pickle_paf = pathlib.Path(r"C:\Measurements\CLINSH\Plumes_data_Campagne2.pickle")

weather_path = pathlib.Path(r"C:\Measurements\CLINSH\Vaisala")

gps_path = pathlib.Path(r"C:\Measurements\CLINSH\AIS")

### MEASUREMENT DATA ###

if reload_measurement_to_pickle or measurement_pickle_paf.exists() == False:
    print("Importing measurement data")
    with open(measurement_paf, "rb") as F:
        mess_df = pandas.read_csv(F, header = 0, delimiter = ",", parse_dates = [0], index_col = 0) 
    mess_df.to_pickle(measurement_pickle_paf)

else:   
    print("Loading measurement data")
    mess_df = pandas.read_pickle(measurement_pickle_paf)

### WEATHER ###

weather_filename = [
    weather_path.joinpath(r"VaisalaWXT201911301451.txt"),
    weather_path.joinpath(r"VaisalaWXT201912011451.txt"),
    weather_path.joinpath(r"VaisalaWXT201912021451.txt"),
    weather_path.joinpath(r"VaisalaWXT201912031451.txt"),
    weather_path.joinpath(r"VaisalaWXT201912041451.txt"),
    weather_path.joinpath(r"VaisalaWXT201912051451.txt"),
    weather_path.joinpath(r"VaisalaWXT201912061451.txt"),
    weather_path.joinpath(r"VaisalaWXT201912071451.txt"),
    weather_path.joinpath(r"VaisalaWXT201912081451.txt"),
    weather_path.joinpath(r"VaisalaWXT201912091451.txt"),

    weather_path.joinpath(r"VaisalaWXT201912101451.txt"),
    weather_path.joinpath(r"VaisalaWXT201912111451.txt"),
    weather_path.joinpath(r"VaisalaWXT201912121451.txt"),
    weather_path.joinpath(r"VaisalaWXT201912131451.txt"),
    weather_path.joinpath(r"VaisalaWXT201912141451.txt"),
    weather_path.joinpath(r"VaisalaWXT201912151451.txt"),
    weather_path.joinpath(r"VaisalaWXT201912161451.txt"),
]

weather_pickle_paf = weather_path.joinpath("weather.pickle")

if reload_weather_to_pickle or weather_pickle_paf.exists() == False:
    print("Importing weather data")
    
    usecols = ["Datetime", "WD", "WS", "Pa avg", "Ta avg"]

    frames = []
    for paf in weather_filename:

        with open(paf, "rb") as F:
            frames.append( pandas.read_csv(F, delimiter = ",", parse_dates = [0], index_col = 0, usecols = usecols, dayfirst = True) )
        
    wx_df = pandas.concat(frames)
    
    wx_df.rename(columns = {"WD": "wind_direction", "WS": "wind_speed"}, inplace = True)

    
    wx_df = wx_df.resample("S").interpolate()


    wx_df.to_pickle(weather_pickle_paf)

else:
    print("Loading weather data")

    wx_df = pandas.read_pickle(weather_pickle_paf)

### GPS DATA ###

gps_filenames = [
    # gps_path.joinpath(r"ECNDATA_20191119.csv"),
    # gps_path.joinpath(r"ECNDATA_20191120.csv"),
    # gps_path.joinpath(r"ECNDATA_20191121.csv"),
    # gps_path.joinpath(r"ECNDATA_20191122.csv"),
    # gps_path.joinpath(r"ECNDATA_20191124.csv"),
    # gps_path.joinpath(r"ECNDATA_20191125.csv"),
    # gps_path.joinpath(r"ECNDATA_20191126.csv"),
    # gps_path.joinpath(r"ECNDATA_20191127.csv"),
    # gps_path.joinpath(r"ECNDATA_20191128.csv"),
    # gps_path.joinpath(r"ECNDATA_20191129.csv"),
    # gps_path.joinpath(r"ECNDATA_20191130.csv"),
    # gps_path.joinpath(r"ECNDATA_20191201.csv"),
    # gps_path.joinpath(r"ECNDATA_20191202.csv"),
    # gps_path.joinpath(r"ECNDATA_20191203.csv"),
    # gps_path.joinpath(r"ECNDATA_20191204.csv"),
    # gps_path.joinpath(r"ECNDATA_20191205.csv"),
    # gps_path.joinpath(r"ECNDATA_20191206.csv"),
    # gps_path.joinpath(r"ECNDATA_20191209.csv"),
    # gps_path.joinpath(r"ECNDATA_20191210.csv"),
    
    # gps_path.joinpath(r"ECNDATA_20191211.csv"),
    gps_path.joinpath(r"ECNDATA_20191212.csv"),
    # gps_path.joinpath(r"ECNDATA_20191213.csv"),
    # gps_path.joinpath(r"ECNDATA_20191214.csv"),
    # gps_path.joinpath(r"ECNDATA_20191215.csv"),
    # gps_path.joinpath(r"ECNDATA_20191216.csv"),
    # gps_path.joinpath(r"ECNDATA_20191217.csv"),
]

all_ship_ids = numpy.array([], dtype = int)

for paf in gps_filenames:

    print(paf)

    # first, construct the header. 
    # import the column with nr ships, look for the maximum, and make the header (column names)
    # paf = pathlib.Path(r"C:\Measurements\CLINSH\AIS\ECNDATA_20191119.csv")
    with open(paf, "rb") as F:
        df = pandas.read_csv(F, header = 1, delimiter = ",", usecols = ["nrships"]) 

    max_ships = int(max(df["nrships"]) )
    print(max_ships)
    names = ["datetime","sampling","nrships"]
    for i in range(max_ships):
        names.append("id.{:d}".format(i))
        names.append("lat.{:d}".format(i))
        names.append("lon.{:d}".format(i))
        names.append("speed.{:d}".format(i))
        names.append("heading.{:d}".format(i))
        names.append("imo.{:d}".format(i))
        
    # now import the data
    df = 0
    with open(paf, "rb") as F:
        df = pandas.read_csv(F, delimiter = ",", parse_dates = [0], index_col = 0, names = names, header = None, skiprows = 2) 

    # extract which ships are present
    ship_ids = numpy.array([], dtype = int)
    for i in range(max_ships):
        x = df["id.{:d}".format(i)].to_numpy()
        idx = numpy.where(numpy.isfinite(x))[0]
        temp = numpy.unique(x[idx])
        ship_ids = numpy.concatenate((ship_ids, temp), axis = None)
    # list with unique ships
    ship_ids = numpy.array(numpy.unique(ship_ids), dtype = int)
    # all_ship_ids = numpy.concatenate((all_ship_ids, ship_ids), axis = None)
    nr_unique_ships = len(ship_ids)

    # make a table with the lat/lon
    latlon = numpy.zeros((len(df), nr_unique_ships * 2))
    latlon[:,:] = numpy.nan
    col_names_lat = []
    col_names_lon = []
    for ship_i, ship_id in enumerate(ship_ids):
        col_names_lat.append("latS{:d}".format(ship_id))
        col_names_lon.append("lonS{:d}".format(ship_id))
        for i in range(max_ships):
            ids = df["id.{:d}".format(i)].to_numpy()
            if ship_id in ids:
                idx = numpy.where(ids == ship_id)[0]
                lat = df["lat.{:d}".format(i)].to_numpy()
                lon = df["lon.{:d}".format(i)].to_numpy()
                latlon[idx, ship_i] =lat[idx]
                latlon[idx, ship_i + nr_unique_ships] = lon[idx]

    # make a dataframe with the ship positions
    # each set of columns (lat/lon) represents 1 ship
    col_names = col_names_lat + col_names_lon
    gps_df = pandas.DataFrame(latlon, index = df.index, columns = col_names)

    # mean: if there are two values, take the mean
    # pad: if a value is missing, forward fill it, with a limit. 
    gps_df = gps_df.resample("S").mean().pad(limit = 1)

    # inner merge with measurement data
    # this means that only timestamps with a plume are left
    result = pandas.merge(mess_df, gps_df, left_index=True, right_index=True, how="inner")
    result = pandas.merge(result, wx_df, left_index=True, right_index=True, how="inner")

    # drop columns with NaN only
    result.dropna(axis = "columns", how = "all", inplace = True)

    ship_ids = []
    for cn in result.columns:
        if "latS" in cn:
            ship_ids.append(cn[4:])
    
    ship_ids = numpy.array(ship_ids, dtype = int)
    all_ship_ids = numpy.concatenate((all_ship_ids, ship_ids), axis = None)

    date = paf.stem[8:]

    ships_paf = output_path.joinpath("{:s}_ships.csv".format(date))
    numpy.savetxt(ships_paf, ship_ids, fmt = "%d")

    pickle_paf = output_path.joinpath("{:s}_merged_data.pickle".format(date))
    result.to_pickle(pickle_paf)


all_ship_ids = numpy.array(numpy.unique(all_ship_ids), dtype = int)

ships_paf = output_path.joinpath("all_ships.csv")
numpy.savetxt(ships_paf, all_ship_ids, fmt = "%d")
