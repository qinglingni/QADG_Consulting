import pandas as pd
import numpy as np
import string
from datetime import datetime
import time

def GetWeekData(name):
    """
    Input: string of the six-digit number in the filename
    Output: pandas dataframe with cols named year, month, day, STATION, and ENTRIES.
            The ENTRIES are weekly avearge daily entries of each staion.
    """
    url = "http://web.mta.info/developers/data/nyct/turnstile/turnstile_{0}.txt".format(name)
    print url
    df = pd.read_csv(url)
    df = df.drop_duplicates(["C/A","UNIT","SCP","STATION","LINENAME","DIVISION","DATE","TIME"])

    #get the earlyest time of each day
    df = df.merge(df.groupby(["C/A","UNIT","SCP","STATION","LINENAME","DIVISION","DATE"])
                    .min()
                    .reset_index()[["C/A","UNIT","SCP","STATION","LINENAME","DIVISION","DATE","TIME"]]
                    .rename(columns={"TIME":"TMIN"}),
                  on=["C/A","UNIT","SCP","STATION","LINENAME","DIVISION","DATE"],
                  how="left")

    #keep only keep the earlyest-time data for each day
    df = df[df.TIME==df.TMIN]
    #calculate the entries for each day
    df["ENTRIES"] = df.ENTRIES.diff()
    #remove the first day (NAN)
    df = df[df.DATE!=list(df.DATE)[0]]
    #remove negative values
    df = df[df.ENTRIES>=0]
    #calculate weekly average entries for each SCP
    df = df[["C/A","UNIT","SCP","STATION","ENTRIES"]]
    df = df.groupby(["C/A","UNIT","SCP","STATION"]).mean().reset_index()
    #calculate total daily entries for each station
    df = df[["STATION","ENTRIES"]]
    df = df.groupby("STATION").sum().reset_index()
    #year, month, day columns
    df["year"] = int("20"+name[:2])
    df["month"] = int(name[2:4])
    df["day"] = int(name[4:])
    return df

week = 604800
df = pd.DataFrame()
#get the data of the previous 96 weeks back
for i in range(0,96):
    #back from the day 20170408
    t=time.mktime(datetime.strptime("20170408","%Y%m%d").timetuple())
    #get the day which marked the ith week back from the start day
    t = t+14400
    t-=i*week
    name = datetime.fromtimestamp(t).strftime('%Y%m%d')[2:]
    print i,name
    #get data
    df = df.append(GetWeekData(name))
    #save the data 
    df.to_csv("2year_{0}.csv".format(i),index=False)
