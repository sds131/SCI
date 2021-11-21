import requests
from bs4 import BeautifulSoup
import re
import csv
from selenium import webdriver
import json
from selenium.webdriver.chrome.options import Options
import time

# get affiliations of authors of SocNet
def get_affiliations_SocNet(filepath):
    f1 = open(filepath, 'r', encoding='utf-8')
    csv_reader = csv.reader(f1)
    f2 = open('./journals/authors_socnet.csv', 'a', encoding='utf-8')
    csv_writer = csv.writer(f2)
    for row in csv_reader:
        url = str(row)
        url = url[2:-2]
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_experimental_option(
            "excludeSwitches", ['enable-automation', 'enable-logging'])
        driver = webdriver.Chrome(options=chrome_options)
        driver.set_page_load_timeout(60)
        driver.set_script_timeout(60)
        try:
            driver.get(url)
            time.sleep(10)
        except:
            driver.execute_script("window.stop()")
        html = driver.page_source
        soup = BeautifulSoup(html, 'lxml')
        print(html)
        content = soup.findAll('script', {'type': 'application/json'})[0].text
        content_json = json.loads(content)
        num = 0
        for i in content_json['authors']['content'][0]['$$']:
            if i['#name'] == 'author':
                num += 1
        author_name = []
        author_affiliation = []
        d = 0
        for i in range(0, num):
            for j in range(0, len(content_json['authors']['content'][0]['$$'][i]['$$'])):
                if content_json['authors']['content'][0]['$$'][i]['$$'][j][
                        "#name"] == "cross-ref":
                    if content_json['authors']['content'][0]['$$'][i]['$$'][j]["$"][
                            "refid"] == "CORR1" or content_json['authors']['content'][
                                0]['$$'][i]['$$'][j]["$"]["refid"] == "COR1" or "cor" in content_json[
                                    'authors']['content'][0]['$$'][i]['$$'][j][
                                        "$"]["refid"] or content_json['authors'][
                                            'content'][0]['$$'][i]['$$'][j]["$"][
                                                "refid"] == "FN1" or content_json[
                                                    'authors']['content'][0][
                                                        '$$'][i]['$$'][j]["$"][
                                                            "refid"] == "fn1" or "fn" in content_json[
                                                                'authors']['content'][
                                                                    0]['$$'][i][
                                                                        '$$'][j][
                                                                            "$"][
                                                                                "refid"]:
                        continue
                    else:
                        d = 1

        for i in range(0, num):
            name = []
            for j in range(
                    0,
                    len(content_json['authors']['content'][0]['$$'][i]['$$'])):
                if content_json['authors']['content'][0]['$$'][i]['$$'][j][
                        "#name"] == "given-name":
                    name.append(content_json['authors']['content'][0]['$$'][i]
                                ['$$'][j]['_'])
                elif content_json['authors']['content'][0]['$$'][i]['$$'][j][
                        "#name"] == "surname":
                    name.append(content_json['authors']['content'][0]['$$'][i]
                                ['$$'][j]['_'])
                elif content_json['authors']['content'][0]['$$'][i]['$$'][j][
                        '#name'] == 'suffix':
                    name.append(content_json['authors']['content'][0]['$$'][i]
                                ['$$'][j]['_'])
                elif content_json['authors']['content'][0]['$$'][i]['$$'][j][
                        "#name"] == "cross-ref":
                    if content_json['authors']['content'][0]['$$'][i]['$$'][j]["$"][
                            "refid"] != "CORR1" and content_json['authors']['content'][
                                0]['$$'][i]['$$'][j]["$"]["refid"] != "COR1" and "cor" not in content_json[
                                    'authors']['content'][0]['$$'][i]['$$'][j][
                                        "$"]["refid"] and content_json['authors'][
                                            'content'][0]['$$'][i]['$$'][j]["$"][
                                                "refid"] != "FN1" and content_json[
                                                    'authors']['content'][0][
                                                        '$$'][i]['$$'][j]["$"][
                                                            "refid"] != "fn1" and "fn" not in content_json[
                                                                'authors']['content'][
                                                                    0]['$$'][i][
                                                                        '$$'][j][
                                                                            "$"][
                                                                                "refid"]:
                        kk = j
                        break
            cname = str()
            for k in range(0, len(name) - 1):
                cname += name[k] + ' '
            cname += name[len(name) - 1]
            author_name.append(cname)
            if d == 0:
                if i == 0:
                    t = str(content_json['authors']['affiliations'].values())
                    temp = str(
                        re.findall(r"'#name': 'textfn', '_': '(.*?)'", t))
                    temp = temp[2:-2]
                    affiliation = temp
                else:
                    affiliation = author_affiliation[0]
                author_affiliation.append(affiliation)
            else:
                s = content_json['authors']['content'][0]['$$'][i]['$$'][kk][
                    '$']['refid']
                affiliation = content_json['authors']['affiliations'][s]['$$'][
                    1]['_']
                author_affiliation.append(affiliation)

        for i in range(0, num):
            csv_writer.writerow(
                [str(author_name[i]),
                 str(author_affiliation[i])])
    f2.close()


if __name__ == '__main__':
    file_name = './journals/urls_socnet.csv'  # subject to change
    get_affiliations_SocNet(file_name)
