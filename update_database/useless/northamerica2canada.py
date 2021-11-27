import pandas as pd

df = pd.read_csv('country-info.csv', header=0)
region = df['region'].tolist()
abbr = df['countryabbrv'].tolist()
length = len(region)
for i in range(length):
    if abbr[i] == 'ca':
        region[i] = 'canada'
df['region'] = region

df.to_csv('country-info.csv',index=False)
    