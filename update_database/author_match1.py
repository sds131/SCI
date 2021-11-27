from numpy.core.fromnumeric import sort
import pandas as pd
import re

uc_names = ['Los Angeles', 'Berkeley', 'Santa Barbara', 'San Diego', 'Davis', 'Irvine', 'Santa Cruz', 'Riverside', 'Merced']

def process_raw_author(filename, full_list, unnormalize):
    un = 'un-' if unnormalize else '' 
    df = pd.read_csv(filename, header=None, names=['name', 'affiliation'])
    names = df['name'].tolist()
    schools = df['affiliation'].tolist()
    matches = {}
    not_matched = {}
    import json
    with open("./jsons/dict-enged-university-info.json", 'r', encoding='utf-8') as load_f:
        dict = json.load(load_f)
    for i in range(len(schools)):
        name = names[i]
        school = schools[i]
        if not type(school) == str:
            not_matched[name] = school
            continue
        # remove the quote
        school = re.sub('–', '-', school)
        school = re.sub('"', '', school)
        school = re.sub('’', "'", school) 
        school = re.sub(r'([a-zA-z])(,)([a-zA-z])', r'\1, \3', school)
        temp_split = school.split(', ')
        flag = 0
        for iter in range(len(temp_split)):
            item = temp_split[iter]
            if unnormalize:
                if item in dict:
                    item = dict[item]
                # else: 
                    # item = google_translate_single(item)
            if 'University of California' in item:
                if item == 'University of California' or item == 'The University of California':
                    new_item = item
                    for temp in range(iter + 1, len(temp_split)):
                        campus_name = temp_split[temp]
                        if campus_name in uc_names:
                            new_item =  item + ' - ' + campus_name
                            break
                        if 'LA' in campus_name:
                            new_item =  item + ' - ' + 'Los Angeles'
                            break
                        if 'Barrows Hall' in campus_name:
                            new_item =  item + ' - ' + 'Berkeley'
                            break
                elif 'University of California at' in item:
                    new_item = 'University of California' + ' - ' + item[len('University of California at '):]
                elif item == 'University of California - Department of Sociology':
                    new_item = 'University of California' + ' - ' + 'Berkeley'
                elif 'University of California -' in item:
                    new_item = item
                else:
                    new_item = 'University of California' + ' - ' + item[len('University of California '):]
            elif 'Maryland' in item or "Maryand" in item:
                new_item = 'University of Maryland - College Park'
            else:
                new_item = item
            if "Stanford" in new_item:
                new_item = 'Stanford University'
            if 'Max-Planck' in new_item:
                new_item = 'Max-Planck Institute for Informatics'
            if 'London School' in new_item:
                new_item = 'London School of Economics and Political Science'
            if 'MIT ' in new_item:
                new_item = 'Massachusetts Institute of Technology'
            if item == 'UC Berkeley':
                new_item = 'University of California - Berkeley'
            if item == 'Telefonica Research':
                new_item = 'Telefónica Research'
            if 'Johns Hopkins' in item:
                new_item = 'Johns Hopkins University'
            if item == 'IIIT-Delhi':
                new_item = 'IIIT Delhi'
            if 'GESIS' in item:
                new_item = 'GESIS - Leibniz Institute for the Social Sciences'
            if 'Erasmus University' in item:
                new_item = 'Erasmus University Rotterdam'
            # if 'China University of Petroleum' in item: 
            #     new_item = 'China University of Petroleum (Huadong)'
            if item == 'Beijing University':
                new_item = 'Peking University'
            if 'University of Illinois' in item:
                if 'Champaign' in item:
                    new_item = 'University of Illinois at Urbana-Champaign'
                elif 'Chicago' in item:
                    new_item = 'University of Illinois at Chicago'
                else:
                    for temp in range(iter + 1, len(temp_split)):
                        campus_name = temp_split[temp]
                        if 'Champaign' in campus_name:
                            new_item = 'University of Illinois at Urbana-Champaign'
                            break
                        if 'Chicago' in campus_name:
                            new_item = 'University of Illinois at Chicago'
                            break
            if 'University of Paris – Dauphine' in item:
                new_item = 'University of Paris - Dauphine'
            if 'Université du Québec À' in item:
                new_item = 'Université du Québec à Montréal'
            if 'Universidade Federal de Pernambuco' == item:
                new_item = 'Universidade Federal Rural de Pernambuco'
            if 'National University of Defence Technology' == item:
                new_item = 'National University of Defense Technology'
            if 'Ludwig-Maximilians-University' == item or 'Ludwigs-Maximilians-Universität München' == item:
                new_item = 'LMU Munich'
            if 'ISPA– Instituto Universitário' == item:
                new_item = 'ISPA University Institute of Psychological Sciences'
            if 'VU University' in item or 'Vrije Universiteit' in item:
                new_item = 'VU Amsterdam'
            if "University of Hawai'i at Mānoa" == item:
                new_item = 'University of Hawaii at Manoa'
            if 'ETH ' in item:
                new_item = 'ETH Zurich'
            if 'université de caen' == item:
                new_item = 'University of Caen'
            if 'DAMO Academy' in item:
                new_item = 'Alibaba Group'
            if 'Complex Systems of Paris' in item:
                new_item = 'ISC-PIF'
            if ('Max-Planck' in item or 'Max Planck' in item):
                new_item = 'Max Planck Institute'
            for university in full_list:
                if university in new_item:
                    matches[name] = university
                    flag = 1
                    break
            if flag == 1:
                break
            
        if flag == 0:
            not_matched[name] = school

    matches = sorted(matches.items())
    names = [item[0] for item in matches]
    schools = [item[1] for item in matches]
    df = pd.DataFrame({'name': names, 'affiliation': schools})
    if unnormalize:
        df2 = pd.read_csv('author-affiliation' + filename[-5] + '.csv', header=0)
        df = pd.concat([df2, df], axis=0)
    df.to_csv('author-affiliation' + filename[-5] + '.csv', index=False)

    # not_matched = sorted(not_matched.items())
    not_matched_names = [item for item in not_matched.keys()]
    not_matched_schools = [item for item in not_matched.values()]
    df = pd.DataFrame({'name': not_matched_names, 'affiliation': not_matched_schools})
    if unnormalize:
        df2 = pd.read_csv('not-matched-author' + filename[-5] + '.csv', header=0)
        df = pd.concat([df2, df], axis=0)
    df.to_csv('not-matched-author' + filename[-5] + '.csv', index=False)

from translate_string import google_translate_single

if __name__ == '__main__':
    us_school_list = pd.read_csv('us-university-info.csv', header=0)
    us_school_list = us_school_list['institution'].tolist()

    school_list = pd.read_csv("enged-country-info-full.csv", header=0)
    school_list = school_list['institution'].tolist()
    school_list += us_school_list
    # comple_names = ["complement-university-name" + str(i) + ".csv" for i in range(1, 2)]
    # complement_school_list = [pd.read_csv(item, header=None, names=['affiliation']) for item in comple_names]
    # complement_school_list = [item['affiliation'].tolist() for item in complement_school_list]
    full_list = school_list
    # for item in complement_school_list:
    #     full_list += item

    unnormal = 0
    un = 'un' if unnormal else ''
    filename = un + 'normalize_authors.csv'
    process_raw_author(filename, full_list, unnormal)
    

    
            
    
