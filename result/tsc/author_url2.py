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

  f = open('author_title2.csv','a',encoding='utf-8')
  csv_writer = csv.writer(f)
  for i in range(0,len(author)):
    csv_writer.writerow([str(author[i])])
  f.close()

if __name__ == '__main__':
  s1="https://dblp.org/db/journals/tsoco/tsoco"
  s2=".html"
  for i in range(1,5):
    address=s1+str(i)+s2
    fun(address)