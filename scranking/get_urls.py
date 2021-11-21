import requests
from bs4 import BeautifulSoup
import re
import csv
import os


def get_paper_url(address, file_name):
    res = requests.get(address)
    res.encoding = 'utf-8'
    soup = BeautifulSoup(res.text, 'lxml')
    article_address = soup.select('.publ-list .entry .publ .drop-down .head')
    # print(article_address[1])
    num = int(len(article_address) / 4)
    addr = []
    for i in range(0, num):
        s = str(article_address[4 * i].contents[0])
        n = re.findall(r"<a href=(.+?)><img alt=", s)
        addr.append(n)
    with open(file_name, 'a+', encoding='utf-8') as f:
        for i in range(0, num):
            temp = re.sub('"', '', addr[i][0])
            f.write(temp)
            f.write('\n')


if __name__ == '__main__':
    path = './journals/'
    file_list = os.listdir(path)
    journal_num = len(file_list)
    for every in file_list:

        if 'ori' in every:
            print(every)
            journal = re.sub('ori_', '', every)
            journal = re.sub('dblp_', '', journal)
            journal = re.sub('.txt', '', journal)
            print(journal)
            file_name = "urls_" + journal + '.csv'
            file = open(path + file_name,
                        'w').close()  # clear the file content
            with open(path + every, 'r', encoding='utf-8') as f:
                while True:
                    row = f.readline()
                    if not row:
                        break
                    print(row)
                    get_paper_url(row, path + file_name)
