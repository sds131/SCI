import os 
import requests
from bs4 import BeautifulSoup
import re
import shutil
import csv
import pandas as pd
from selenium import webdriver
# get the unique names of authors in DBLP like: Fei-Yue Wang 0001, so we don't need to use dblp_aliases.csv.

def get_unique(filepath, journal_name):
    f1 = open(filepath, 'r', encoding='utf-8')
    csv_reader = csv.reader(f1)
    f2 = open('author_unique' + "_" + journal_name + '.csv', 'a', encoding='utf-8')
    csv_writer = csv.writer(f2)
    for row in csv_reader:
        journal_url = str(row)
        journal_url = journal_url[2:-2]
        res = requests.get(journal_url)
        res.encoding = 'utf-8'
        soup = BeautifulSoup(res.text, 'lxml')
        sesoup = soup.select('.publ-list .entry .data ')
        strsoup = str(sesoup)
        temp = str(re.findall(r'<span itemprop="name" title="(.*?)"', strsoup))
        temp = temp[1:-1]
        temp = temp.split(", ")
        author = []
        for i in temp:
            author.append(i[1:-1])
        for i in range(0, len(author)):
            csv_writer.writerow([str(author[i])])
    f2.close()


# 由于论文网址丢失、部分作者无单位等原因，authors_xxx.csv可能不完整，需要手动将authors_xxx.csv和author_unique_xxx.csv进行比对，
# 补充并修改authors_xxx.csv，使得authors_xxx.csv和author_unique_xxx.csv行数一致。
# 同时由于author_unique_xxx.csv的author字段正是dblp的作者姓名标识符，补充修改authors_xxx.csv后，
# 需要将author_unique_xxx.csv中的author字段代替authors_xxx.csv中的name字段，这步可以直接复制粘贴。
# 将文件更名为 modified1_xxx.csv
# authors_xxx -> modified1


# Remove controversial and unidentified authors
# modified1 -- -> modified2
def disambiguation(filepath1, filepath2, journal_name):
    f1 = open(filepath1, 'r', encoding='utf-8')
    csv_reader1 = csv.reader(f1)
    journal_url = []
    for row in csv_reader1:
        j_url = str(row)
        j_url = j_url[2:-2]
        journal_url.append(j_url)

    check = []
    for url in journal_url:
        res = requests.get(url)
        print('debug' + url)
        res.encoding = 'utf-8'
        soup = BeautifulSoup(res.text, 'lxml')
        # print(soup)
        sesoup = soup.select('.publ-list .entry .data ')
        strsoup = str(sesoup)
        check_url = str(
            re.findall(r'<a href="(.*?)" itemprop="url"><span itemprop="name"',
                       strsoup))
        check_url = check_url[1:-1]
        check_url = check_url.split(", ")
        for i in check_url:
            check.append(i[1:-1])

    f2 = open(filepath2, 'r', encoding='utf-8')
    csv_reader2 = csv.reader(f2)
    author = []
    affiliation = []
    for row in csv_reader2:
        
        author.append(row[0])
        affiliation.append(row[1])
    # print(author)
    print(check)
    if len(check) != len(author):
        print(
            "Some urls of authors' DBLP entry are missing. You need check manually and delete some urls in author_modified1.csv."
        )
        return 0

    disam = [0] * len(author)
    k = 0
    for i in check:
        res = requests.get(i)
        res.encoding = 'utf-8'
        soup = BeautifulSoup(res.text, 'lxml')
        strsoup = str(soup)
        if "<i>disambiguation page</i>" in strsoup:
            disam[k] = 1
        k += 1
    print('here!!')
    f3 = open('modified2_' + journal_name + '.csv', 'a', encoding='utf-8')
    csv_writer = csv.writer(f3)
    for i in range(0, len(author)):
        if disam[i] != 1:
            csv_writer.writerow([str(author[i]), str(affiliation[i])])
    f3.close()
    return 1


# 手动修改author_affiliation字符串，比如"Chinese Academy of Sciences"，
# 会有人写成"Chinese Academic of Sciences"或者"Chinese Academy of Science"
# 这种错误需要我们手动修正
# 这步可以反复使用normalize()，根据unnormlize.csv反馈的信息对modified2_xxx.csv进行修改


# normalize, 其实就是匹配
def normalize(filepath1, filepath2, journal_name):
    f1 = open(filepath1, 'r', encoding='utf-8')
    csv_reader1 = csv.reader(f1)
    university = []
    for row in csv_reader1:
        university.append(str(row[0]))

    f2 = open(filepath2, 'r', encoding='utf-8')
    print('debug: ', filepath2)
    df2 = pd.read_csv(filepath2, header=None)
    # csv_reader2 = csv.reader(f2)
    author = []
    affiliation = []
    for index, row in df2.iterrows():
        print("debug: ", row)
        author.append(str(row[0]))
        affiliation.append(str(row[1]))
    print(len(author))
    f = open('normalize_author_' + journal_name + '.csv', 'w', encoding='utf-8')
    csv_writer3 = csv.writer(f)
    ff = open('unnormalize_author_' + journal_name + '.csv', 'w', encoding='utf-8')
    csv_writer4 = csv.writer(ff)
    for i in range(0, len(author)):
        print("debug: ", author[i])
        for j in range(0, len(university)):
            if university[j] in affiliation[i]:
                f.write(str(author[i]) + ',' + str(university[j]) + '\n')
                # csv_writer3.writerow([str(author[i]), str(university[j])])
                break
            if j == len(university) - 1:
                ff.write(str(author[i]) + ',' +  str(affiliation[i]) + '\n')
                # csv_writer4.writerow([str(author[i]), str(affiliation[i])])
    f.close()
    ff.close()


# duplicate removal 去重，保留作者最近最新的单位。
def duplicate(filepath, journal_name):
    f1 = open(filepath, 'r', encoding='utf-8')
    lines = f1.readlines()
    l = len(lines)
    author_name = []
    author_affiliation = []
    for i in range(0, l):
        name = lines[l - 1 - i].split(',')[0]
        affiliation = lines[l - 1 - i].split(',')[1]
        affiliation = affiliation.strip()
        if name not in author_name:
            author_name.append(name)
            author_affiliation.append(affiliation)
    # f2 = open('modified3_' + journal_name + '.csv', 'w', encoding='utf-8')
    # csv_writer = csv.writer(f2)
    num = len(author_name)
    print(author_name)
    author_name = [author_name[num - 1 - i] for i in range(num)]
    author_affiliation = [author_affiliation[num - 1 - i] for i in range(num)]
    author_affiliation = [affil.replace('"', '') for affil in author_affiliation]
    df = pd.DataFrame({'name': author_name, 'affiliation': author_affiliation})
    df.to_csv('modified3_' + journal_name + '.csv', index=False, header=False)
    # f2.close()

if __name__ == '__main__':
    path = './journals/'
    file_list = os.listdir(path)
    for file in file_list:
        if "authors" in file:
            f = path + file
           
            journal_name = f.split('_')[1]
            journal_name = journal_name.split('.')[0]
            ori_dblp_file = path + 'ori_dblp_' + journal_name + '.txt'
            shutil.copy(f, './authors_' + journal_name + '.csv')
            f = './authors_' + journal_name + '.csv'
            default = 1
            # if you are updating, don't use the default setting! It is just for testing. Please follow the doc instructions
            if default:
                
                shutil.copy(f, './modified1_' + journal_name + '.csv')
                f = './modified1_' + journal_name + '.csv'
                
                r = disambiguation(ori_dblp_file, 'modified1_' + journal_name + '.csv', journal_name)
                if r == 0:
                    shutil.copy(f, './modified2_' + journal_name + '.csv')
                duplicate('modified2_' + journal_name + '.csv', journal_name)
                normalize('country-info.csv', 'modified3_' + journal_name + '.csv', journal_name)
            else:
                # you should make the codes below unannotated to normalize the infos
                pass
                # Step 1:
                # get_unique(ori_dblp_file, journal_name)
                # Step 2:
                # check manually
                # Step 3:
                # disambiguation(ori_dblp_file, 'modified1_' + journal_name + '.csv', journal_name)
                # normalize('country-info.csv', 'modified2_' + journal_name + '.csv')
                # Step 4:
                # check manually repeatedly
                # Step 5:
                # duplicate('modified2_' + journal_name + '.csv', journal_name)
                # normalize('country-info.csv', 'modified3_' + journal_name + '.csv', journal_name)
            