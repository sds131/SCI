import csv

f1 = open('/Users/sds/Downloads/result/enged-country-info-full-new.csv','r',encoding='utf-8')
csv_reader1=csv.reader(f1)
university=[]
for row in csv_reader1:
    university.append(str(row[0]))

#f2 = open('/users/sds/downloads/raw_author3.csv','r',encoding='utf-8')
f2 = open('/users/sds/downloads/result/socomp/author_fixed4.csv','r',encoding='utf-8')
csv_reader2=csv.reader(f2)
author=[]
affiliation=[]
for row in csv_reader2:
    author.append(str(row[0]))
    affiliation.append(str(row[1]))

f = open('/Users/sds/Downloads/normalize_author4.csv','w',encoding='utf-8')
csv_writer3 = csv.writer(f)
ff = open('/Users/sds/Downloads/unnormalize_author4.csv','w',encoding='utf-8')
csv_writer4 = csv.writer(ff)
for i in range(0,len(author)):
    for j in range(0,len(university)):
        if university[j] in affiliation[i]:
            csv_writer3.writerow([str(author[i]),str(university[j])])
            break
        if j==len(university)-1:
            csv_writer4.writerow([str(author[i]),str(affiliation[i])])        
f.close()  
ff.close()