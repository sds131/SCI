import json

with open("./jsons/country-full-info.json", 'r', encoding='utf-8') as load_f:
    countries = json.load(load_f)
with open("./jsons/continent-info.json", 'r', encoding='utf-8') as load_f:
    continents = json.load(load_f)

import pandas as pd

df = pd.read_csv('country-info-syt.csv', header=0)
affiliation = df['institution'].tolist()
region = df['region'].tolist()
ctry = df['countryabbrv'].tolist()
not_matched_ctry = []
length = len(ctry)
for i in range(length):
    ct = ctry[i].upper()
    if ctry[i] == 'uk':
        ct = 'GB'
    if ct in countries:
        cont = countries[ct]['continent']
        region[i] = continents[cont]
    else:
        print(ctry[i].upper())
        not_matched_ctry.append(ctry[i])
df['region'] = region

df.to_csv('country-info-cjc.csv', index=False)
