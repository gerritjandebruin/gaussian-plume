import pathlib

import numpy
import matplotlib 
import matplotlib.pyplot as plt

import pandas

import PythonTools.PlottingTools as PT

plt.close("all")
figures = [
    "wide", 
] 

fig, ax = PT.make_figures(figures, label = False)
fig_i = 0
ax_i = 0

# paf = pathlib.Path(r"C:\Python\GaussianPlume\tests\prototype\raw_data.xlsx")
# df = pandas.read_excel(paf, sheet_name = "Sheet1")

paf = pathlib.Path(r"C:\Python\GaussianPlume\tests\prototype\raw_data.pickle")
# df.to_pickle(paf)

df = pandas.read_pickle(paf)

# ax[fig_i][ax_i].plot(df.loc[:,"Date"].to_numpy(), df.loc[:,"CH4"].to_numpy())

df["CH4"] = df["CH4"].shift(periods = -7) #, axis = "CH4")

start_time = pandas.to_datetime("25/9/2020 09:15:00")
end_time = pandas.to_datetime("25/9/2020 10:00:00")
df.loc[df.Date.between(start_time, end_time),:] = numpy.nan

quantile = df.loc[:,"CH4"].quantile(0.10)

# print(quantile)

df.loc[:,"CH4"] -= quantile


ax[fig_i][ax_i].plot(df.loc[:,"Date"].to_numpy(), df.loc[:,"CH4"].to_numpy())
ax[fig_i][ax_i].plot(df.loc[:,"Date"].to_numpy(), df.loc[:,"Processed"].to_numpy())


plt.show()
