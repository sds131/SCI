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

  f = open('author_disam3.csv','a',encoding='utf-8')
  csv_writer = csv.writer(f)
  for i in range(0,len(author)):
    csv_writer.writerow([str(author[i]),str(disam[i])])
  f.close()


if __name__ == '__main__':
  """
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
  
  s1="https://dblp.org/db/journals/tsoco/tsoco"
  s2=".html"
  for i in range(1,5):
    address=s1+str(i)+s2
    fun(address)
  """
  s1="https://dblp.org/db/journals/socnet/socnet"
  s2=".html"
  for i in range(43,65):
    address=s1+str(i)+s2
    fun(address)