import requests
from bs4 import BeautifulSoup
import re
import csv

def fun(address):
  res = requests.get(address)
  res.encoding = 'utf-8'
  soup = BeautifulSoup(res.text, 'lxml')
  article_address = soup.select('.publ-list .entry .publ .drop-down .head')
  num=int(len(article_address)/4)
  addr=[]
  for i in range(0,num):
    s=str(article_address[4*i].contents[0])
    n = re.findall(r"<a href=(.+?)><img alt=", s)
    addr.append(n)

  f = open('address.csv','a',encoding='utf-8')
  csv_writer = csv.writer(f)
  csv_writer.writerow(["address"])
  for i in range(0,num):
    csv_writer.writerow(addr[i])
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