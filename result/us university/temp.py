import re
import csv
f1 = open('/users/sds/downloads/temp.csv','r',encoding='utf-8')
csv_reader1=csv.reader(f1)
origin_university=[]
for row in csv_reader1:
    origin_university.append(str(row[0]))

num=len(origin_university)

f2 = open('temp1.csv','w',encoding='utf-8')
csv_writer = csv.writer(f2)
for i in range(0,num):
    university=str(re.findall(r'<option value="(.*?)">',origin_university[i]))
    university=university.replace("['","")
    university=university.replace("']","")
    csv_writer.writerow([university,"us"])
f2.close()

"""
f = open('university-info.csv','a',encoding='utf-8')
csv_writer3 = csv.writer(f)
for i in range(0,num):
    for j in range(0,len(university)):
        if university[j] in affiliation[i]:
            csv_writer3.writerow([str(author[i]),str(university[j])])
            break
        if j==len(university)-1:
            csv_writer4.writerow([str(author[i]),str(affiliation[i])])        
f.close()
"""