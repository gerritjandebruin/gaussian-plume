import pathlib

import numpy
import matplotlib 
import matplotlib.pyplot as plt

import pandas
plt.close("all")
paf = pathlib.Path(r"C:\Users\bloemr\TNO\5.4547 - CLINSH - Team\Work\Data_meetcampagnes\Campagne 2\Vaisala\VaisalaWXT201912161451.txt")

with open(paf, "rb") as F:
    df = pandas.read_csv(F, delimiter = ",", parse_dates = [0], index_col = 0) 


df = df.resample("S").interpolate()

    
print(df)

"C:\Measurements\CLINSH\Vaisala\VaisalaWXT201911301451.txt"
"C:\Measurements\CLINSH\Vaisala\VaisalaWXT201912011451.txt"
"C:\Measurements\CLINSH\Vaisala\VaisalaWXT201912021451.txt"
"C:\Measurements\CLINSH\Vaisala\VaisalaWXT201912031451.txt"
"C:\Measurements\CLINSH\Vaisala\VaisalaWXT201912041451.txt"
"C:\Measurements\CLINSH\Vaisala\VaisalaWXT201912051451.txt"
"C:\Measurements\CLINSH\Vaisala\VaisalaWXT201912061451.txt"
"C:\Measurements\CLINSH\Vaisala\VaisalaWXT201912071451.txt"
"C:\Measurements\CLINSH\Vaisala\VaisalaWXT201912081451.txt"
"C:\Measurements\CLINSH\Vaisala\VaisalaWXT201912091451.txt"
"C:\Measurements\CLINSH\Vaisala\VaisalaWXT201912101451.txt"
"C:\Measurements\CLINSH\Vaisala\VaisalaWXT201912111451.txt"
"C:\Measurements\CLINSH\Vaisala\VaisalaWXT201912121451.txt"
"C:\Measurements\CLINSH\Vaisala\VaisalaWXT201912131451.txt"
"C:\Measurements\CLINSH\Vaisala\VaisalaWXT201912141451.txt"
"C:\Measurements\CLINSH\Vaisala\VaisalaWXT201912151451.txt"
"C:\Measurements\CLINSH\Vaisala\VaisalaWXT201912161451.txt"

# plt.plot(df.index, df["WS"])
# plt.plot(df.index, df["Sm avg"])


plt.plot(df.index, df["WD"])
plt.plot(df.index, df["Dm avg"])

plt.show()