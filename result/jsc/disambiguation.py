import requests
from bs4 import BeautifulSoup
import re
import csv

def fun(address):
  res = requests.get(address)
  res.encoding = 'utf-8'
  soup = BeautifulSoup(res.text, 'lxml')
  sesoup = soup.select('.publ-list .entry .data ')
  strsoup=str(sesoup)

  temp = str(re.findall(r'<span itemprop="name" title="(.*?)"', strsoup))
  temp=temp[1:-1]
  temp=temp.split(", ")
  author=[]
  for i in temp:
    author.append(i[1:-1])

  check_url=str(re.findall(r'<a href="(.*?)" itemprop="url"><span itemprop="name"', strsoup))
  check_url=check_url[1:-1]
  check_url=check_url.split(", ")
  check=[]
  for i in check_url:
    check.append(i[1:-1])

  disam=[0]*len(author)
  k=0
  for i in check:
    res = requests.get(i)
    res.encoding = 'utf-8'
    soup = BeautifulSoup(res.text, 'lxml')
    strsoup=str(soup)
    if "<i>disambiguation page</i>" in strsoup:
      disam[k]=1
    k+=1

  f = open('author_disam4.csv','a',encoding='utf-8')
  csv_writer = csv.writer(f)
  for i in range(0,len(author)):
    csv_writer.writerow([str(author[i]),str(disam[i])])
  f.close()


if __name__ == '__main__':
  fun("https://dblp.org/db/journals/socomp/socomp1.html")
  fun("https://dblp.org/db/journals/socomp/socomp2.html")