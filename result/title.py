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
    temp = str(re.findall(r'<span class="title" itemprop="name">(.*?)</span>', strsoup))
    temp=temp[2:-2]
    temp=temp.replace('"',"'")
    temp=temp.split("', '")
    title=[]
    for i in temp:
        title.append(i)

    f = open('title.csv','a',encoding='utf-8')
    csv_writer = csv.writer(f)
    for i in range(0,len(title)):
        csv_writer.writerow([str(title[i])])
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

    s1="https://dblp.org/db/journals/tsoco/tsoco"
    s2=".html"
    for i in range(1,5):
        address=s1+str(i)+s2
        fun(address)

    s1="https://dblp.org/db/journals/socnet/socnet"
    s2=".html"
    for i in range(21,65):
        address=s1+str(i)+s2
        fun(address)

    fun("https://dblp.org/db/journals/socomp/socomp1.html")
    fun("https://dblp.org/db/journals/socomp/socomp2.html")


    s1="https://dblp.uni-trier.de/db/journals/snam/snam"
    s2=".html"
    for i in range(1,13):
        address=s1+str(i)+s2
        fun(address)