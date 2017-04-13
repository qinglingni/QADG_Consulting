import pandas as pd
import numpy as np
import string
from datetime import datetime
import time


def GetWeekData(name):
    url = "http://web.mta.info/developers/data/nyct/turnstile/turnstile_{0}.txt".format(name)
    df = pd.read_csv(url)
    df.columns = df.columns.str.strip()
    df.drop(["DESC", "TIME"], inplace=True, axis=1)

    df_min = df.groupby(['C/A', 'UNIT', 'SCP', 'STATION', 'LINENAME', 'DIVISION', 'DATE']).min()
    df_max = df.groupby(['C/A', 'UNIT', 'SCP', 'STATION', 'LINENAME', 'DIVISION', 'DATE']).max()
    df_min = df_max[["ENTRIES", "EXITS"]] - df_min[["ENTRIES", "EXITS"]]
    df = df_min.reset_index()
    df = df[["STATION", "ENTRIES", "EXITS"]]
    df = df.groupby(['STATION'], as_index=False).sum()
    df["year"] = int("20" + name[:2])
    df["month"] = int(name[2:4])
    df["day"] = int(name[4:])
    return df


week = 604800
t = time.mktime(datetime.strptime("20150718", "%Y%m%d").timetuple())
t = t + 14400
end = time.mktime(datetime.strptime("20150401", "%Y%m%d").timetuple())
# end=time.mktime(datetime.strptime("20170315","%Y%m%d").timetuple())
df = pd.DataFrame()
while True:
    if t < end:
        break
    name = datetime.fromtimestamp(t).strftime('%Y%m%d')[2:]
    print
    name
    df = df.append(GetWeekData(name))
    t -= week
df.sort_values(by=["STATION", "year", "month", "day"], inplace=True)
df.to_csv("2year.csv", index=False)
