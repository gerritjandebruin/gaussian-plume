import pathlib

import numpy
import matplotlib 
import matplotlib.pyplot as plt

import pandas

paf = pathlib.Path(r"C:\Measurements\CLINSH\AIS\ECNDATA_20191119.csv")
df = 0
with open(paf, "rb") as F:
    df = pandas.read_csv(F, header = 1, delimiter = ",", parse_dates = [0], index_col = 0) 

df.rename(columns = {"id": "id.0", "lat": "lat.0", "lon": "lon.0", "speed": "speed.0", "heading": "heading.0", "imo": "imo.0"}, inplace = True)

max_ships = max(df["nrships"])

ship_ids = numpy.array([], dtype = int)



for i in range(max_ships):
    # df["id.{:d}".format(i)] = df["id.{:d}".format(i)].fillna(0)
    # df["id.{:d}".format(i)] = df["id.{:d}".format(i)].astype(int)
    x = df["id.{:d}".format(i)].to_numpy()
    idx = numpy.where(numpy.isfinite(x))[0]
    temp = numpy.unique(x[idx])
    ship_ids = numpy.concatenate((ship_ids, temp), axis = None)

ship_ids = numpy.array(numpy.unique(ship_ids), dtype = int)
# ship_ids = numpy.delete(ship_ids, 0)
# print(ship_ids)

nr_unique_ships = len(ship_ids)

# time = numpy.arange("2019-11-19 00:00:00", "2019-11-20 00:00:00", dtype = "datetime64[s]")
# print(time)


latlon = numpy.zeros((len(df), nr_unique_ships * 2))
latlon[:,:] = numpy.nan
# lon = numpy.zeros((len(df), nr_unique_ships)) - 1

col_names_lat = []
col_names_lon = []

for ship_i, ship_id in enumerate(ship_ids):
    col_names_lat.append("latS{:d}".format(ship_i))
    col_names_lon.append("lonS{:d}".format(ship_i))
    for i in range(max_ships):
        # print(ship_id, i)
        ids = df["id.{:d}".format(i)].to_numpy()
        if ship_id in ids:
            # print("   x")
            
            # idx = numpy.where(ids == ship_id)[0]
            # latlon[idx, ship_i] = df.loc[idx, "lat.{:d}".format(i)].to_numpy()
            # latlon[idx, ship_i + nr_unique_ships] = df.loc[idx, "lon.{:d}".format(i)].to_numpy()

            idx = numpy.where(ids == ship_id)[0]
            lat = df["lat.{:d}".format(i)].to_numpy()
            lon = df["lon.{:d}".format(i)].to_numpy()
            latlon[idx, ship_i] =lat[idx]
            latlon[idx, ship_i + nr_unique_ships] = lon[idx]



col_names = col_names_lat + col_names_lon


gps_df = pandas.DataFrame(latlon, index = df.index, columns = col_names)
print(gps_df.dtypes)
# mean: if there are two values, take the mean
# pad: if a value is missing, forward fill it, with a limit. 
gps_df = gps_df.resample("S").mean().pad(limit = 1)
print(gps_df.dtypes)

# gps_df = gps_df.resample("S")


print(gps_df)

pickle_paf = pathlib.Path(r"C:\Measurements\CLINSH\AIS\GPS_20191119.pickle")

gps_df.to_pickle(pickle_paf)


# print(ship_ids)
# print(len(ship_ids))

# 
# print(ship_ids)
# print(len(ship_ids))


# headers = "datetime,sampling,nrships,id,lat,lon,speed,heading,imo,id,lat,lon,speed,heading,imo,id,lat,lon,speed,heading,imo,id,lat,lon,speed,heading,imo,id,lat,lon,speed,heading,imo,id,lat,lon,speed,heading,imo,id,lat,lon,speed,heading,imo,id,lat,lon,speed,heading,imo,id,lat,lon,speed,heading,imo,id,lat,lon,speed,heading,imo,id,lat,lon,speed,heading,imo,id,lat,lon,speed,heading,imo,id,lat,lon,speed,heading,imo,id,lat,lon,speed,heading,imo,id,lat,lon,speed,heading,imo,id,lat,lon,speed,heading,imo,id,lat,lon,speed,heading,imo,id,lat,lon,speed,heading,imo,id,lat,lon,speed,heading,imo,id,lat,lon,speed,heading,imo,id,lat,lon,speed,heading,imo,id,lat,lon,speed,heading,imo,id,lat,lon,speed,heading,imo,id,lat,lon,speed,heading,imo,id,lat,lon,speed,heading,imo,id,lat,lon,speed,heading,imo,id,lat,lon,speed,heading,imo,id,lat,lon,speed,heading,imo,id,lat,lon,speed,heading,imo,id,lat,lon,speed,heading,imo,id,lat,lon,speed,heading,imo,id,lat,lon,speed,heading,imo,id,lat,lon,speed,heading,imo,id,lat,lon,speed,heading,imo,id,lat,lon,speed,heading,imo,id,lat,lon,speed,heading,imo,id,lat,lon,speed,heading,imo"
# data = numpy.loadtxt(paf, delimiter = ",", skiprows = 2 )

# x = df["id.1"].to_numpy()

# idx = numpy.where(x == x[0])[0]
# print(len(idx))
# idx = numpy.where(x == x[-1])[0]
# print(len(idx))

# print(numpy.all(x == x[0]))
# print(numpy.all(x == 244015636))


# print(df["id.1"])


# numpy.unique(x)






print()