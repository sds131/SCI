import csv

if __name__ == '__main__':
    f = open('/users/sds/downloads/author_disam3.csv','r',encoding='utf-8')
    csv_reader=csv.reader(f)
    author=[]
    affiliation=[]
    for row in csv_reader:
        if row[1]=='0':
           author.append(row[0]) 
           affiliation.append(row[2])
    ff = open('/users/sds/downloads/author3.csv','a',encoding='utf-8')
    csv_writer = csv.writer(ff)
    for i in range(0,len(author)):
        csv_writer.writerow([str(author[i]),str(affiliation[i])])
    ff.close()