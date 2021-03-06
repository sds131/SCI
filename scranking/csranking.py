import requests
from bs4 import BeautifulSoup
import re
import csv
from selenium import webdriver


# get urls of papers
def get_urls(filepath):
    f1 = open(filepath, 'r', encoding='utf-8')
    csv_reader = csv.reader(f1)
    f2 = open('paper_url.csv', 'a', encoding='utf-8')
    csv_writer = csv.writer(f2)
    for row in csv_reader:
        journal_url = str(row)
        journal_url = journal_url[2:-2]
        res = requests.get(journal_url)
        res.encoding = 'utf-8'
        soup = BeautifulSoup(res.text, 'lxml')
        url = soup.select('.publ-list .entry .publ .drop-down .head')
        num = int(len(url) / 4)
        paper_url = []
        for i in range(0, num):
            s = str(url[4 * i].contents[0])
            n = re.findall(r"<a href=(.+?)><img alt=", s)
            n = str(n)
            n = n[3:-3]
            paper_url.append(n)
        for i in range(0, num):
            csv_writer.writerow([paper_url[i]])
    f2.close()


# get affiliations of authors of TCSS
def get_affiliations_tcss(filepath):
    f1 = open(filepath, 'r', encoding='utf-8')
    csv_reader = csv.reader(f1)
    f2 = open('raw_author.csv', 'a', encoding='utf-8')
    csv_writer = csv.writer(f2)
    for row in csv_reader:
        paper_url = str(row)
        paper_url = paper_url[2:-2]
        res = requests.get(paper_url)
        res.encoding = 'utf-8'
        soup = BeautifulSoup(res.text, 'lxml')
        s = str(soup)
        temp = str(re.findall(r'xplGlobal.document.metadata=(.*);', s))
        author_name = str(re.findall(r'"name":"(.*?)","affiliation"', temp))
        author_affiliation = str(re.findall(r'"affiliation":\["(.*?)"\]',
                                            temp))
        author_name = author_name[1:-1]
        author_name = author_name.replace("'", "")
        author_name = author_name.split(", ")
        author_affiliation = author_affiliation[1:-1]
        author_affiliation = author_affiliation.split("', '")
        for i in range(0, len(author_affiliation)):
            author_affiliation[i] = author_affiliation[i].replace("'", "")
            author_affiliation[i] = author_affiliation[i].replace('","', ',')
        if author_name == ['']:
            author_name = str(re.findall(r'"name":"(.*?)","bio"', temp))
            author_name = author_name[1:-1]
            author_name = author_name.replace("'", "")
            author_name = author_name.split(", ")
            author_affiliation = []
            for i in range(0, len(author_name)):
                author_affiliation.append('')
        num = len(author_name)
        for i in range(0, num):
            csv_writer.writerow(
                [str(author_name[i]),
                 str(author_affiliation[i])])
    f2.close()


"""
def get_affiliations_tcss(url):
    paper_url=str(url)
    paper_url=paper_url[2:-2]
    res = requests.get(paper_url)
    res.encoding = 'utf-8'
    soup = BeautifulSoup(res.text, 'lxml')
    s=str(soup)
    temp = str(re.findall(r'xplGlobal.document.metadata=(.*);', s))
    author_name = str(re.findall(r'"name":"(.*?)","affiliation"',temp))
    author_affiliation=str(re.findall(r'"affiliation":\["(.*?)"\]',temp))
    author_name=author_name[1:-1]
    author_name=author_name.replace("'", "")
    author_name=author_name.split(", ")
    author_affiliation=author_affiliation[1:-1]
    author_affiliation=author_affiliation.split("', '")
    for i in range(0,len(author_affiliation)):
        author_affiliation[i]=author_affiliation[i].replace("'", "")
        author_affiliation[i]=author_affiliation[i].replace('","', ',')
    if author_name==['']:
        author_name = str(re.findall(r'"name":"(.*?)","bio"',temp))
        author_name=author_name[1:-1]
        author_name=author_name.replace("'", "")
        author_name=author_name.split(", ")
        author_affiliation=[]
        for i in range(0,len(author_name)):
            author_affiliation.append('')
    num=len(author_name)
    f = open('raw_author.csv','a',encoding='utf-8')
    csv_writer = csv.writer(f)
    for i in range(0,num):
        csv_writer.writerow([str(author_name[i]),str(author_affiliation[i])])
    f.close()
"""


# get affiliations of authors of TSC
def get_affiliations_tsc(filepath):
    pass


# get affiliations of authors of SocNet
def get_affiliations_SocNet(filepath):
    f1 = open(filepath, 'r', encoding='utf-8')
    csv_reader = csv.reader(f1)
    f2 = open('raw_author.csv', 'a', encoding='utf-8')
    csv_writer = csv.writer(f2)
    for row in csv_reader:
        url = str(row)
        url = url[2:-2]
        driver = webdriver.Chrome('/usr/local/bin/chromedriver')
        driver.set_page_load_timeout(60)
        driver.set_script_timeout(60)
        try:
            driver.get(url)
        except:
            driver.execute_script("window.stop()")
        html = driver.page_source
        soup = BeautifulSoup(html, 'lxml')
        content = soup.findAll('script', {'type': 'application/json'})[0].text
        content_json = json.loads(content)
        num = 0
        for i in content_json['authors']['content'][0]['$$']:
            if i['#name'] == 'author':
                num += 1
        author_name = []
        author_affiliation = []
        d = 0
        for i in range(0, num):
            for j in range(
                    0,
                    len(content_json['authors']['content'][0]['$$'][i]['$$'])):
                if content_json['authors']['content'][0]['$$'][i]['$$'][j][
                        "#name"] == "cross-ref":
                    if content_json['authors']['content'][0]['$$'][i]['$$'][j]["$"][
                            "refid"] == "CORR1" or content_json['authors']['content'][
                                0]['$$'][i]['$$'][j]["$"]["refid"] == "COR1" or "cor" in content_json[
                                    'authors']['content'][0]['$$'][i]['$$'][j][
                                        "$"]["refid"] or content_json['authors'][
                                            'content'][0]['$$'][i]['$$'][j]["$"][
                                                "refid"] == "FN1" or content_json[
                                                    'authors']['content'][0][
                                                        '$$'][i]['$$'][j]["$"][
                                                            "refid"] == "fn1" or "fn" in content_json[
                                                                'authors']['content'][
                                                                    0]['$$'][i][
                                                                        '$$'][j][
                                                                            "$"][
                                                                                "refid"]:
                        continue
                    else:
                        d = 1

        for i in range(0, num):
            name = []
            for j in range(
                    0,
                    len(content_json['authors']['content'][0]['$$'][i]['$$'])):
                if content_json['authors']['content'][0]['$$'][i]['$$'][j][
                        "#name"] == "given-name":
                    name.append(content_json['authors']['content'][0]['$$'][i]
                                ['$$'][j]['_'])
                elif content_json['authors']['content'][0]['$$'][i]['$$'][j][
                        "#name"] == "surname":
                    name.append(content_json['authors']['content'][0]['$$'][i]
                                ['$$'][j]['_'])
                elif content_json['authors']['content'][0]['$$'][i]['$$'][j][
                        '#name'] == 'suffix':
                    name.append(content_json['authors']['content'][0]['$$'][i]
                                ['$$'][j]['_'])
                elif content_json['authors']['content'][0]['$$'][i]['$$'][j][
                        "#name"] == "cross-ref":
                    if content_json['authors']['content'][0]['$$'][i]['$$'][j]["$"][
                            "refid"] != "CORR1" and content_json['authors']['content'][
                                0]['$$'][i]['$$'][j]["$"]["refid"] != "COR1" and "cor" not in content_json[
                                    'authors']['content'][0]['$$'][i]['$$'][j][
                                        "$"]["refid"] and content_json['authors'][
                                            'content'][0]['$$'][i]['$$'][j]["$"][
                                                "refid"] != "FN1" and content_json[
                                                    'authors']['content'][0][
                                                        '$$'][i]['$$'][j]["$"][
                                                            "refid"] != "fn1" and "fn" not in content_json[
                                                                'authors']['content'][
                                                                    0]['$$'][i][
                                                                        '$$'][j][
                                                                            "$"][
                                                                                "refid"]:
                        kk = j
                        break
            cname = str()
            for k in range(0, len(name) - 1):
                cname += name[k] + ' '
            cname += name[len(name) - 1]
            author_name.append(cname)
            if d == 0:
                if i == 0:
                    t = str(content_json['authors']['affiliations'].values())
                    temp = str(
                        re.findall(r"'#name': 'textfn', '_': '(.*?)'", t))
                    temp = temp[2:-2]
                    affiliation = temp
                else:
                    affiliation = author_affiliation[0]
                author_affiliation.append(affiliation)
            else:
                s = content_json['authors']['content'][0]['$$'][i]['$$'][kk][
                    '$']['refid']
                affiliation = content_json['authors']['affiliations'][s]['$$'][
                    1]['_']
                author_affiliation.append(affiliation)

        for i in range(0, num):
            csv_writer.writerow(
                [str(author_name[i]),
                 str(author_affiliation[i])])
    f2.close()


def get_affiliations_snam(filepath):
    f1 = open(filepath, 'r', encoding='utf-8')
    csv_reader = csv.reader(f1)
    f2 = open('raw_author.csv', 'a', encoding='utf-8')
    csv_writer = csv.writer(f2)
    for row in csv_reader:
        paper_url = str(row)
        paper_url = paper_url[2:-2]
        res = requests.get(paper_url)
        res.encoding = 'utf-8'
        soup = BeautifulSoup(res.text, 'lxml')        
        s = str(soup)
        temp = str(re.findall(r'<script type="application/ld\+json">{(.*)</script>', s))
        temp = str(re.findall(r'"author":\[(.*)\]',temp))
        temp = str(re.findall(r'"name":".*?"@type":"Person"}',temp))
        name_list=temp.split("', '")
        author_name=[]
        for i in name_list:
            if '"url":' not in i:
                t=str(re.findall(r'"name":"(.*?)","affiliation"',i))
            else:
                t=str(re.findall(r'"name":"(.*?)","url"',i))
            t=t[2:-2]
            t=t.split(", ")
            tt=str()
            num=len(t)
            for i in range(0,num):
                tt+=t[num-1-i]
                if i!=num-1:
                    tt+=' '
            author_name.append(tt)
        author_affiliation=[]
        # temp=str(re.findall(r'"affiliation":\[{"name":"(.*?)","address"',temp))
        temp=str(re.findall(r'"address":{"name":"(.*?)","@type":"PostalAddress"',temp))
        temp=temp[2:-2]
        affiliation_list=temp.split("', '")
        for i in affiliation_list:
            author_affiliation.append(i)
        
        num = len(author_name)
        for i in range(0, num):
            csv_writer.writerow(
                [str(author_name[i]),
                 str(author_affiliation[i])])
    f2.close()


# get the unique names of authors in DBLP like: Fei-Yue Wang 0001, so we don't need to use dblp_aliases.csv.
def get_unique(filepath):
    f1 = open(filepath, 'r', encoding='utf-8')
    csv_reader = csv.reader(f1)
    f2 = open('author_unique.csv', 'a', encoding='utf-8')
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


# ????????????????????????????????????????????????????????????raw_author.csv?????????????????????????????????raw_author.csv???author_unique.csv???????????????
# ???????????????raw_author.csv?????????raw_author.csv???author_unique.csv???????????????
# ????????????author_unique.csv???author????????????dblp???????????????????????????????????????raw_author.csv??????
# ?????????author_unique.csv??????author????????????raw_author.csv??????name??????????????????????????????????????????
# ?????????author_modified1.csv
# raw ++ -> modified1


# Remove controversial and unidentified authors
# modified1 -- -> modified2
def disambiguation(filepath1, filepath2):
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
        res.encoding = 'utf-8'
        soup = BeautifulSoup(res.text, 'lxml')
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

    if len(check) != len(author):
        print(
            "Some urls of authors' DBLP entry are missing. You need check manually and delete some urls in author_modified1.csv."
        )
        return

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

    f3 = open('author_modified2.csv', 'a', encoding='utf-8')
    csv_writer = csv.writer(f3)
    for i in range(0, len(author)):
        if disam[i] != 1:
            csv_writer.writerow([str(author[i]), str(affiliation[i])])
    f3.close()

# duplicate removal ?????????????????????????????????????????????
def duplicate(filepath):
    f1 = open(filepath, 'r', encoding='utf-8')
    lines = f1.readlines()
    l = len(lines)
    author_name = []
    author_affiliation = []
    for i in range(0, l):
        name = lines[l - 1 - i].split(',')[0]
        affiliation = lines[l - 1 - i].split(',')[1]
        affiliation = affiliation.strip()
        affiliation=affiliation.replace('"','')
        if name not in author_name:
            author_name.append(name)
            author_affiliation.append(affiliation)
    f2 = open('author_modified3.csv', 'w', encoding='utf-8')
    csv_writer = csv.writer(f2)
    num = len(author_name)
    for i in range(0, num):
        csv_writer.writerow([
            str(author_name[num - 1 - i]),
            str(author_affiliation[num - 1 - i])
        ])
    f2.close()

# ????????????author_affiliation??????????????????"Chinese Academy of Sciences"???
# ???????????????"Chinese Academic of Sciences"??????"Chinese Academy of Science"
# ????????????????????????????????????
# ????????????????????????normalize()?????????unnormlize.csv??????????????????author_modified.csv????????????
# ??????author_modified.csv

#normalize
def normalize(filepath1, filepath2):
    f1 = open(filepath1, 'r', encoding='utf-8')
    csv_reader1 = csv.reader(f1)
    university = []
    for row in csv_reader1:
        university.append(str(row[0]))

    f2 = open(filepath2, 'r', encoding='utf-8')
    csv_reader2 = csv.reader(f2)
    author = []
    affiliation = []
    for row in csv_reader2:
        author.append(str(row[0]))
        affiliation.append(str(row[1]))

    f = open('normalize.csv', 'w', encoding='utf-8')
    csv_writer3 = csv.writer(f)
    ff = open('unnormalize.csv', 'w', encoding='utf-8')
    csv_writer4 = csv.writer(ff)
    for i in range(0, len(author)):
        for j in range(0, len(university)):
            if university[j] in affiliation[i]:
                csv_writer3.writerow([str(author[i]), str(university[j])])
                break
            if j == len(university) - 1:
                csv_writer4.writerow([str(author[i]), str(affiliation[i])])
    f.close()
    ff.close()


#main
if __name__ == '__main__':
    f1 = "journal_url.csv"
    # get_urls(f1)
    f2 = 'paper_url.csv'
    # get_affiliations_snam(f2)
    
    # get_unique(f1)

    # check manually
    
    # disambiguation(f1,'author.csv')

    # duplicate('author_modified2.csv')

    normalize('country-info.csv','author_modified3.csv')

    # check manually