from numpy.core.fromnumeric import sort
import pandas as pd
import re

from translate_string import google_translate_single

supplement_list = {
    'Wake Forest School of Medicine': 'Wake Forest School of Medicine',
    'CSIRO': 'CSIRO',
    'Max-Planck': 'Max Planck Institute',
    'CNRS': 'CNRS',
    'Argonne National Laboratory': 'Argonne National Laboratory',
    'Pacific Northwest National Laboratory': 'Pacific Northwest National Laboratory',
    'Los Alamos National Laboratory': 'Los Alamos National Laboratory',
    'London School of Economics': 'London School of Economics and Political Science',
    'London School Economics': 'London School of Economics and Political Science',
    'Indian Institute of Engineering Science and Technology': 'Indian Institute of Engineering Science and Technology',
    'Indian Institute of Information Technology': 'Indian Institute of Information Technology',
  
    'Google': 'Google',
    'Nokia Bell Labs': 'Nokia Bell Labs',
    'Microsoft': 'Microsoft',
    'Airbnb': 'Airbnb',
    'IBM': 'IBM',
    'HP Labs': 'HP Labs',
    'Telefónica Research': 'Telefónica Research',
    'Amazon ': 'Amazon Inc.',
    'Santa Fe': 'Santa Fe Institute',
    'Telecom ParisTech': 'Telecom ParisTech',
    'CERN': 'CERN',
    'MIT ': 'Massachusetts Institute of Technology',
    'Copenhagen Business School': 'Copenhagen Business School',
    'IMT School for Advanced Studies': 'IMT School for Advanced Studies',
    'U.S. Army Research Laboratory': 'U.S. Army Research Laboratory',
    'U.S. Army Engineer Research and Development Center': 'U.S. Army Engineer Research and Development Center',
    '515 College Hall Duquesne University': 'Duquesne University',
    'Leibniz Institute': 'GESIS - Leibniz Institute for the Social Sciences',
    'University of Greenwich': 'University of Greenwich',
    'Technical University of Munich': 'Technical University of Munich',
    'Erasmus University': 'Erasmus University Rotterdam',
    'Trinity College Dublin': 'Trinity College Dublin',
    'UFRPE': 'UFRPE',
    'Vel Tech': 'Vel Tech',
    'Banasthali Vidyapith': 'Banasthali Vidyapith',
    'Institute of Information Science': 'Institute of Information Science',
    'Netherlands Defense Academy': 'Netherlands Defense Academy',
    'Oregon Research Institute': 'Oregon Research Institute',
    'Institute for Service Marketing and Tourism': 'Institute for Service Marketing and Tourism',
    'FU Berlin': 'FU Berlin',
    'DAMO Academy': 'Alibaba Group',
    "Kebangsaan Malaysia": 'National University of Malaysia'
    # 'China University of Petroleum': 'China University of Petroleum (Huadong)'
}

exclude_list = [
    'University of California - Department of Sociology',
    'University of Illinois',
    'California State University',
    'Johns Hopkins Bloomberg School of Public Health',
    'Telefonica Research',
    'IIIT-Delhi',
    # 'FU Berlin',
    'Beijing University',
    'University of Paris – Dauphine',
    'Université du Québec À Montréal',
    'Universidade Federal de Pernambuco',
    'National University of Defence Technology',
    'Ludwig-Maximilians-University',
    'Ludwigs-Maximilians-Universität München',
    'ISPA– Instituto Universitário',
    'VU University',
    'Vrije Universiteit',
    'VU University Amsterdam',
    'University of Lugano (Switzerland)',
    'University of Hawai’i at Mānoa',
    'ETH Zürich',
    'and Corvinus University of Budapest',
    'université de caen',
    'ZPID – Leibniz Institute for Psychology Information',
    'KTH - Royal Institute of Technology,europe',
    'Wroclaw University of Technology',
    'Wrocław University of Technology',
    "Institut Barcelona d'Estudis Internacionals (IBEI)"
]

def get_country_abbr(country):
    import json
    with open("./jsons/country-abbr.json", 'r', encoding='utf-8') as load_f:
        dict = json.load(load_f)
    abbr = []
    for i in country:
        if 'Saudi Arabia' in i:
            i = 'Saudi Arabia'
        if 'UK' in i or 'Scotland' in i or 'England' in i:
            i = 'United Kingdom'
        if 'Russian Federation' in i:
            i = 'Russia'
        if 'China' in i:
            i = 'China'
        if 'Palestinian Authority' in i:
            i = 'Palestine'
        if i == 'Korea':
            i = 'South Korea' 
        if i == 'España':
            i = 'Spain'
        if i == 'UAE':
            i = 'United Arab Emirates'
        if i == 'Brasil':
            i = 'Brazil'
        if i not in dict:
            print("ERROR: Country not in the JSON, please check ./jsons/country-abbr.json: ", i.encode('utf-8'))
            a = dict[i].lower()
        a = dict[i].lower()
        abbr.append(a)
            
        
    return abbr

def get_continent(abbr_country):
    import json
    with open("./jsons/country-full-info.json", 'r', encoding='utf-8') as load_f:
        countries = json.load(load_f)
    with open("./jsons/continent-info.json", 'r', encoding='utf-8') as load_f:
        continents = json.load(load_f)
    region = []
    not_matched_ctry = []
    length = len(abbr_country)
    for i in range(length):
        ct = abbr_country[i].upper()
        if abbr_country[i] == 'uk':
            ct = 'GB'
        if ct in countries:
            cont = countries[ct]['continent']
            if ct == 'CA': 
                # if it is Canada, then the continent should be 'canada', in order to match the front-end codes
                region.append('canada')
            else:
                region.append(continents[cont])
        else:
            print(abbr_country[i].upper())
            not_matched_ctry.append(abbr_country[i])

    return region

if __name__ == '__main__':
    new_universities = []
    not_universities = []
    univer_country = {}
    count_not_university = {}
    flag_school = {}
    filename_root = 'not-matched-authors'
    filename = filename_root + '.csv'
    df = pd.read_csv(filename, header=0, encoding='utf-8')
    try:
        temp = df['affiliation'].tolist()
    except KeyError:
        df = pd.read_csv(filename, header=None, names=['name', 'affiliation'], encoding='utf-8')
        temp = df['affiliation'].tolist()
    for school in temp:
        if not type(school) == str:
            continue
        # remove the quote
        school = re.sub('"', '', school) 
        school = re.sub(r'([a-zA-z])(,)([a-zA-z])', r'\1, \3', school)
        school = re.sub('The Univer', 'Univer', school)
        temp_split = school.split(', ')

        flag_school[school] = 0
        for every in temp_split:
            
            
            if every in exclude_list:
                flag_school[school] = 1
                break
            for temp in supplement_list.items():
                if temp[0] in every:
                    new_universities.append(temp[1])
                    flag_school[school] = 1
                    if 'DAMO Academy' in every:
                        univer_country[temp[1]] = 'China'
                    else:
                        univer_country[temp[1]] = temp_split[-1]
            if flag_school[school] == 0 and ('Univer' in every or 'univer' in every):
                new_universities.append(every)
                flag_school[school] = 1
                univer_country[every] = temp_split[-1]

        if flag_school[school] == 0:
            not_universities.append(school)
            for every in temp_split:
                if every in count_not_university:
                    count_not_university[every] += 1
                else:
                    count_not_university[every] = 1


    filename = filename_root + '.csv'
    df = pd.read_csv(filename, header=0, encoding='utf-8')
    try:
        temp = df['affiliation'].tolist()
    except KeyError:
        df = pd.read_csv(filename, header=None, names=['name', 'affiliation'], encoding='utf-8')
        temp = df['affiliation'].tolist()
    for school in temp:
        if not type(school) == str:
            continue
        # remove the quote
        school = re.sub('"', '', school) 
        school = re.sub(r'([a-zA-z])(,)([a-zA-z])', r'\1, \3', school)
        school = re.sub('The Univer', 'Univer', school)
        temp_split = school.split(', ')
        if flag_school[school] == 1:
            continue
        # flag = 0
        for every in temp_split:
            if ('Institu' in every or 'institu' in every or 'Acade' in every or 'acade' in every) and every in count_not_university :
                new_universities.append(every)
                flag_school[school] = 1
                univer_country[every] = temp_split[-1]
        if flag_school[school] == 0:
            not_universities.append(school)
    # for i in flag_school.keys():
    #     if flag_school[i] == 0:
    #         not_universities.append(i)

    # not_universities = set(not_universities)
    with open('not-university-name.csv', 'w+', encoding='utf-8') as f:
        for i in not_universities:
            f.write(i)
            f.write('\n')

    new_universities = list(set(new_universities))
    new_universities = sorted(new_universities)
    new_universities_country = [univer_country[school] for school in new_universities]
    with open('complement-university-name1.csv', 'w+', encoding='utf-8') as f:
        for i in new_universities:
            f.write(i)
            f.write('\n')
    abbr = get_country_abbr(new_universities_country)
    region = get_continent(abbr)
    if len(abbr) == len(region):
        df = pd.DataFrame({'institution': new_universities, 'region': region,'countryabbrv': abbr})
        df.to_csv('complement-university-info1.csv', index=False)
    else:
        print("ERROR")
    
    