import requests
from bs4 import BeautifulSoup
import re
import csv

def fun(address):
    res = requests.get(address)
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
    ff = open('/users/sds/downloads/author4.csv','a',encoding='utf-8')
    csv_writer = csv.writer(ff)
    for i in range(0,num):
        csv_writer.writerow([str(author_name[i]),str(author_affiliation[i])])
    ff.close()

if __name__ == '__main__':
    f = open('/users/sds/downloads/result/socomp/address.csv','r',encoding='utf-8')
    csv_reader=csv.reader(f)
    for row in csv_reader:
        address=str(row)
        address=address[3:-3]
        fun(address)