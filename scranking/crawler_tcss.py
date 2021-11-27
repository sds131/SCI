import requests
from bs4 import BeautifulSoup
import re
import csv
from selenium import webdriver

def get_affiliations_tcss(filepath):
    f1 = open(filepath,'r',encoding='utf-8')
    csv_reader=csv.reader(f1)
    f2 = open('./journals/authors_tcss.csv','a',encoding='utf-8')
    csv_writer = csv.writer(f2)
    for row in csv_reader:
        paper_url=str(row)
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
        for i in range(0,num):
            csv_writer.writerow([str(author_name[i]),str(author_affiliation[i])])
    f2.close()
    
if __name__ == '__main__':
    
    file_name = './journals/urls_tcss.csv'  # subject to change
    get_affiliations_tcss(file_name)