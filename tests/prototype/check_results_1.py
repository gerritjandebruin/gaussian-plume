import pathlib

import numpy
import matplotlib 
import matplotlib.pyplot as plt

import scipy
import pandas

import PlottingTools as PT

paf = pathlib.Path(r"C:\Measurements\CLINSH\output\20191212_merged_data.pickle")

df = pandas.read_pickle(paf)

paf_ships = pathlib.Path(r"C:\Measurements\CLINSH\20191212_ships.csv")
ship_ids = numpy.loadtxt(paf_ships, dtype = int)[1:]
# print(ship_ids)
# print(df)


# plt.show()




plt.close("all")
figures = [
    {"u": 1/2.54, "fig_w": 20, "fig_h": 15, "l": 1.8, "b": 1.2, "ax_w": 17.5, "ax_h": 13}
]
fig, ax = PT.make_figures(figures, label = False)
fig_i = 0
ax_i = 0

img = plt.imread(r"C:\Measurements\CLINSH\map_only.png")
# plt.imshow(img, extent = extend)
# # [left, right, bottom, top]
extent = [5.9295, 6.1990, 51.8205, 51.9174]
ax[fig_i][ax_i].imshow(img, extent = extent, aspect = "auto", zorder = 0)

n_ships = 0
for ship_id in ship_ids:
    
    if "lonS{:d}".format(ship_id)in df.columns:

        ax[fig_i][ax_i].plot(df["lonS{:d}".format(ship_id)], df["latS{:d}".format(ship_id)])
        n_ships += 1
# ax[fig_i][ax_i].set_xlim(5.9295, 6.1990)
# ax[fig_i][ax_i].set_ylim( 51.8205, 51.9174)

ax[fig_i][ax_i].set_xlim(6.02, 6.13)
ax[fig_i][ax_i].set_ylim( 51.835, 51.88)

plt.show()
print(n_ships)