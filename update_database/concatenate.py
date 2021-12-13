from numpy.lib.npyio import save
import pandas as pd
import re
from translate_string import save_dict
def concatenate_dict(new_dict):
    import json
    with open("./jsons/dict-enged-university-info.json", 'r', encoding='utf-8') as load_f:
        dict1 = json.load(load_f)
    dict2 = new_dict    
    dictMerged2=dict(dict1, **dict2)
    from translate_string import save_dict
    save_dict(dictMerged2, 'dict-enged-university-info')

df1 = pd.read_csv('complement-university-info1.csv', header=0)
df0 = pd.read_csv('enged-country-info-full.csv', header=0)
ori = df0['institution'].tolist()
ori_country = df0['countryabbrv'].tolist()

df0['institution'] = ori
df0['countryabbrv'] = ori_country
comple_contryabbrv = df1['countryabbrv'].tolist()
for i in range(len(comple_contryabbrv)):
    comple_contryabbrv[i] = comple_contryabbrv[i].lower()
df1['countryabbrv'] = comple_contryabbrv

comp = df1['institution'].tolist()
from translate_string import google_translate_single
enged_complement_school = {}
for i in range(len(comp)):
    every = comp[i]
    
    new_name = google_translate_single(every)
    comp[i] = new_name
    if new_name != every:
        enged_complement_school[every] = new_name
df1['institution'] = comp




df2 = pd.concat([df0, df1], axis=0)
# check the case again
insts = df2['institution'].tolist()
ctrys = df2['countryabbrv'].tolist()
for i in range(len(insts)):
    if 'institute' in insts[i]:
        insts[i] = re.sub('institute', 'Institute', insts[i])
    if 'campus' in insts[i]:
        insts[i] = re.sub('campus', 'Campus', insts[i])
    if 'Of' in insts[i]:
        insts[i] = re.sub('Of', 'of', insts[i])
    if 'For' in insts[i]:
        insts[i] = re.sub('For', 'for', insts[i])
    if 'The' in insts[i] and insts[i][0:3] != 'The':
        insts[i] = re.sub('The', 'the', insts[i])
    if 'Air force' in insts[i]:
        insts[i] = re.sub('force', 'Force', insts[i])
    if 'foreign' in insts[i]:
        insts[i] = re.sub('foreign', 'Foreign', insts[i])
    if 'forensic' in insts[i]:
        insts[i] = re.sub('forensic', 'Forensic', insts[i])
    insts[i] = insts[i].replace('"', '')
    insts[i] = insts[i].strip()
    ctrys[i] = ctrys[i].lower()
df2['institution'] = insts
df2['countryabbrv'] = ctrys
df2 = df2.drop_duplicates()

df2.to_csv('enged-country-info-full-new.csv', index=False)

concatenate_dict(enged_complement_school)