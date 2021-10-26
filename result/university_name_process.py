from numpy.core.fromnumeric import sort
import pandas as pd
import re

if __name__ == '__main__':
    df = pd.read_csv("affiliations6.0.csv")
    names = df['name'].tolist()
    schools = df['affiliation'].tolist()

    school_list = pd.read_csv("university-info.csv", header=0)
    school_list = school_list['affiliation'].tolist()
    matches = {}
    not_matched = {}
    for i in range(len(schools)):
        name = names[i]
        school = schools[i]
        if not type(school) == str:
            not_matched[name] = school
            continue
        # remove the quote
        school = re.sub('"', '', school) 
        temp_split = school.split(', ')

        flag = 0
        for item in temp_split:
            if item in school_list:
                matches[name] = item
                flag = 1
                break
        if flag == 0:
            not_matched[name] = school

    matches = sorted(matches.items())
    names = [item[0] for item in matches]
    schools = [item[1] for item in matches]
    df = pd.DataFrame({'name': names, 'affiliation': schools})
    df.to_csv('author-affiliation.csv', index=False)

    not_matched = sorted(not_matched.items())
    not_matched_names = [item[0] for item in not_matched]
    not_matched_schools = [item[1] for item in not_matched]
    df = pd.DataFrame({'name': not_matched_names, 'affiliation': not_matched_schools})
    df.to_csv('not-matched-author.csv', index=False)
            
    
