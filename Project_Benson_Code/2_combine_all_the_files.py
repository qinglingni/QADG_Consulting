import pandas as pd

df = pd.DataFrame()
for i in range(96):
    fname = "2year_{0}.csv".format(i)
    df1 = pd.read_csv(fname)
    df = df.append(df1)

df.to_csv("2year_total.csv",index=False)
