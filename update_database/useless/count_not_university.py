import pandas as pd
import re

if __name__ == '__main__':
    new_universities = []
    not_universities = []
    univer_country = {}
    count_not_university = {}
    with open('not-university-name1.csv', encoding='utf-8') as f:
        for line in f:
            school = line.strip('\n')
            school = re.sub('"', '', school) 
            temp_split = school.split(', ')
            for every in temp_split:
                if every in count_not_university:
                    count_not_university[every] += 1
                else:
                    count_not_university[every] = 1
    count_not_university = sorted(count_not_university.items(), key=lambda x:x[1], reverse=True)
    names = [item[0] for item in count_not_university]
    counts = [item[1] for item in count_not_university]
    df = pd.DataFrame({'name': names, 'count': counts})
    df.to_csv("count-not-university.csv", index=False) 
