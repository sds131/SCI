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

  f = open('author_title.csv','a',encoding='utf-8')
  csv_writer = csv.writer(f)
  for i in range(0,len(author)):
    csv_writer.writerow([str(author[i])])
  f.close()

if __name__ == '__main__':
  address="https://dblp.org/db/journals/tcss/tcss1.html"
  fun(address)
  address="https://dblp.org/db/journals/tcss/tcss2.html"
  fun(address)
  address="https://dblp.org/db/journals/tcss/tcss3.html"
  fun(address)
  address="https://dblp.org/db/journals/tcss/tcss4.html"
  fun(address)
  address="https://dblp.org/db/journals/tcss/tcss5.html"
  fun(address)
  address="https://dblp.org/db/journals/tcss/tcss6.html"
  fun(address)
  address="https://dblp.org/db/journals/tcss/tcss7.html"
  fun(address)
  address="https://dblp.org/db/journals/tcss/tcss8.html"
  fun(address)