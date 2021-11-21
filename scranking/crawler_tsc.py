import requests
from bs4 import BeautifulSoup
import re
import csv
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
def get_author_info(address):
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_experimental_option("excludeSwitches", ['enable-automation', 'enable-logging'])
    driver = webdriver.Chrome(options=chrome_options)
    # while True:
    driver.get(address)
    button = driver.find_element_by_link_text('Authors Info & Claims')
    driver.execute_script("$(arguments[0]).click()", button)
    time.sleep(2)
    names_eles = driver.find_elements_by_class_name('auth-name')
    
    names = []
    
    for item in names_eles:
        # print("item class: ", item.is_displayed())
        name = item.find_element_by_tag_name('a')
        # print("texts:", name.text)
        name = name.text
        names.append(name)
        # time.sleep(1)
    # print("names", names)
    affiliations = driver.find_elements_by_class_name('auth-institution')
    schools = [re.sub('"', '', item.text) for item in affiliations]
    if len(names) != len(schools):
        print("debug: Not equal!!")
    return names, schools


if __name__ == '__main__':
    file_name = './journals/urls_tsc.csv' # subject to change
    with open(file_name,'r',encoding='utf-8') as f:
        all_names = []
        scholar_graph = []
        all_schools = []
        cnt = 0
        while True:
            row = f.readline()
            if not row:
                break
            address=str(row)
            print(address)
            if 'http' not in address:
                continue
  
            address = re.sub('\n', '', address)
            address = re.sub('"', '', address)
            address = re.sub("'", '', address)
            names1, schools1 = get_author_info(address)
            scholar_graph.append(names1)
            print(names1, schools1)
            cnt += 1
            print("Cnt: ", cnt)
            all_names += names1
            all_schools += schools1
            
        
    import pandas as pd
    df = pd.DataFrame({"name": all_names, "affiliation": all_schools})
    df.to_csv("./journals/authors_tsc"  + ".csv", index=False, header=None)
    


    