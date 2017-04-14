import pandas as pd
import string

def CleanName(name):
    for punct in string.punctuation:
        name = name.replace(punct, " ")
    name = name.replace(" AVE", " AV")
    name = name.replace("AVE ", "AV ")
    name = name.replace("AVENUE", "AV")
    name = name.replace(" STS", " ST")
    name = name.replace("ROAD", "RD")
    name = name.replace("HIGHWAY", "HWY")
    name = name.replace("PARKWAY","PKWY")
    return name

df = pd.read_csv("2year_total.csv")
df = df.drop_duplicates(["STATION","year","month","day"])

#clean names of some stations
df["STATION"] = df["STATION"].map(CleanName) 

#count how many weeks we got for each station
df = df.merge(df.groupby("STATION")
              .count()
              .reset_index()
              .rename(columns={"ENTRIES":"num"})
              [["STATION","num"]],
              how="left",on="STATION")

#remove the data of the stations whose week count is not 96
#these stations are still named differently in different weeks
df = df[df.num==96]

#get time index
df["time"] = pd.to_datetime(df[["year","month","day"]])
df = df.drop(["num","year","month","day"],axis=1)\
       .sort_values(["STATION","time"])\
       .set_index("time")

#new dataframe with station names as column names
data = {}
for s in list(df.STATION.unique()):
    data[s] = df[df["STATION"]==s]["ENTRIES"]#.resample("4W").median()
df = pd.DataFrame(data)
df.to_csv("two_year.csv",index=True)

