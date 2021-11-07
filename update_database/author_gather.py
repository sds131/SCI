import os
import re
import pandas as pd
path = './journals/'
normalize_names = []
unnormalize_names = []
for file in os.listdir(path): 
    # file_path = os.path.join(path, file) 
    if "normalize_author" in file and ".csv" in file and re.search('\d', file) != None:
        if "un" in file:
            unnormalize_names.append(file)
        else:
            normalize_names.append(file)
normalize_df = []
for file in normalize_names:
    df = pd.read_csv(file, header=None)
    normalize_df.append(df)

final_df = pd.concat(normalize_df, axis=0)
final_df.to_csv('normalize_authors.csv', index=False, header=None)

unnormalize_df = []
for file in unnormalize_names:
    df = pd.read_csv(file, header=None)
    unnormalize_df.append(df)

final_df = pd.concat(unnormalize_df, axis=0)
final_df.to_csv('unnormalize_authors.csv', index=False, header=None)