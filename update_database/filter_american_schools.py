import pandas as pd
from pandas import DataFrame
df1 = pd.read_csv('enged-country-info-full-new.csv', header=0)

df2 = pd.read_csv('us-university-info.csv', header=0)
df1 = df1.append(df2)
df1 = df1.append(df2)
df1 = df1.drop_duplicates(keep=False)
df1.to_csv('country-info.csv', index=False)