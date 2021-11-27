# to get rid of non-English strings
from datetime import time
import pandas as pd
import urllib
import random
import json
import random
import requests
import urllib.parse
from hashlib import md5
import re
import time
# not used
# def baidu_translate_api(text):
#     """英文翻译成中文"""
#     appid = '20210929000960577'
#     secretKey = 'x1zvnQxvGGmrpH7HEv92'
#     myurl = 'http://api.fanyi.baidu.com/api/trans/vip/translate'
#     q = text
#     fromLang = 'auto'
#     toLang = 'en'
#     salt = random.randint(32768, 65536)
#     sign = appid+q+str(salt)+secretKey
#     m1 = md5()
#     m1.update(sign.encode("utf-8"))
#     sign = m1.hexdigest()

#     myurl = myurl+'?appid='+appid+'&q='+urllib.parse.quote(q)+'&from='+fromLang+'&to='+toLang+'&salt='+str(salt)+'&sign='+sign
#     response = requests.get(myurl)
#     return_json = json.loads(response.text)
#     result = return_json['trans_result'][0]['dst']
#     return result 

# def baidu_translate_list(univ_list):
#     siz = len(univ_list)
#     cnt = 0
#     for i in range(siz):
#         string = univ_list[i]
#         flag = 0
#         string = re.sub('-', ' ', string)
#         string = re.sub('—', ' ', string)
#         string = re.sub('’', "'", string)
#         splits = string.split(' ')
#         for item in splits:
#             for c in item:
#                 if c != "'" and (not isEnglish(c)):
#                     flag = 1
#                     break
#             if flag == 1:
#                 break
#         if flag == 1:
#             cnt += 1
#             print('cnt: ', cnt)
#             print('original: ', string)
#             time.sleep(1)
#             result = translate_api(string)
#             print('result: ', result)
#             univ_list[i] = result

#     return univ_list

def isEnglish(s):
    try:
        s.encode(encoding='utf-8').decode('ascii')
    except UnicodeDecodeError:
        return False
    else:
        return True

map2eng = {
'ê': 'e',
'ș': 's',
'ü': 'u',
'—': '-',
'Ö': 'o',
'ò': 'o',
'í': 'i',
'ñ': 'n',
'ı': 'i',
'–': '-',
'ä': 'a',
'’': "'",
'ç': 'c',
'å': 'a',
'ğ': 'g',
'ó': 'o',
'á': 'a',
'ö': 'o',
'ł': 'l',
'õ': 'o',
'ã': 'a',
'é': 'e',
'à': 'a',
'â': 'a',
'è': 'e'
}



def save_dict(dict, name):
    dict = json.dumps(dict)
    path = './jsons/' + name + '.json'
    with open(path, "w", encoding='utf-8') as f:
        f.write(dict)
    
def google_translate_list(univ_list, name):
    from googletrans import Translator as trans
    translator = trans(service_urls=[
      'translate.google.com.cn'])
    siz = len(univ_list)
    cnt = 0
    dict = {}
    for i in range(siz):
        string = univ_list[i]
        flag = 0
        string = re.sub('-', ' ', string)
        string = re.sub('—', ' ', string)
        string = re.sub('’', "'", string)
        splits = string.split(' ')
        new_splits = []
        for item in splits:
            if not '(' in item:
                new_splits.append(item)
        for item in new_splits:
            if 'Universidad' in item or item == 'Universiteit' or item == 'Universite' or item == 'Universitat' or item == 'de':
                flag = 1
            else:
                for c in item:
                    if c != "'" and (not isEnglish(c)):
                        flag = 1
                        break
            if flag == 1:
                break
        if flag == 1:
            cnt += 1
            print('cnt: ', cnt)
            # print('original: ', string)
            time.sleep(1)
            new_string = ' '.join(new_splits)
            result = translator.translate(new_string)
            print('result: ', result.text)
            univ_list[i] = result.text
            dict[string] = result.text
    save_dict(dict, name)
    return univ_list

def google_translate_single(univ):
    from googletrans import Translator as trans
    translator = trans(service_urls=[
      'translate.google.com.cn'])
    cnt = 0
    dict = {}
    string = univ
    flag = 0
    string = re.sub('-', ' ', string)
    string = re.sub('—', ' ', string)
    string = re.sub('’', "'", string)
    splits = string.split(' ')
    new_splits = []
    for item in splits:
        if not '(' in item:
            new_splits.append(item)
    for item in new_splits:
        if 'Universidad' in item or item == 'Universiteit' or item == 'Universite' or item == 'Universitat' or item == 'de':
            flag = 1
        else:
            for c in item:
                if c != "'" and (not isEnglish(c)):
                    flag = 1
                    break
        if flag == 1:
            break
    if flag == 1:
        cnt += 1
        print('cnt: ', cnt)
        # print('original: ', string)
        time.sleep(1)
        new_string = ' '.join(new_splits)
        result = translator.translate(new_string)
        print('result: ', result.text)
        univ = result.text
        dict[string] = result.text
    return univ

if __name__ == '__main__':

    df1 = pd.read_csv('ori-country-info-full.csv', header=0)
    ori_list = df1['institution'].tolist()
    name1 = "enged-ori-country-info-full1"
    ori_list = google_translate_list(ori_list, name1)
    # for i in range(siz1):
    #     # splits = string.split(' ')
    #     string = comp_list[i]
    #     siz = len(string)
    #     for j in range(siz):
    #         if not isEnglish(string[j]):
    #             print('debug: ', string[j])
    #             comp_list[i][j] = map2eng[string[j]]
    
    # for i in range(siz2):
    #     # splits = string.split(' ')
    #     string = ori_list[i]
    #     siz = len(string)
    #     for j in range(siz):
    #         if not isEnglish(string[j]):
    #             print('debug: ', string[j])
    #             ori_list[i][j] = map2eng[string[j]]
      
    df1['institution'] = ori_list
    
    
    df1.to_csv(name1 + '.csv', index=False)
