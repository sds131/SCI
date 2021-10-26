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
  #csv_writer.writerow(["address"])
  for i in range(0,num):
    csv_writer.writerow(addr[i])
  f.close()


if __name__ == '__main__':
  s1="https://dblp.org/db/journals/socnet/socnet"
  s2=".html"
  for i in range(21,65):
    address=s1+str(i)+s2
    fun(address)