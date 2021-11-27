import csv
if __name__ == '__main__':
    f = open('/Users/sds/Downloads/result/socomp/normalize_author4.csv','r',encoding='utf-8')
    lines = f.readlines()
    l=len(lines)
    author_name=[]
    author_affiliation=[]
    for i in range(0,l):
        name=lines[l-1-i].split(',')[0]
        affiliation=lines[l-1-i].split(',')[1]
        affiliation=affiliation.strip()
        if name not in author_name:
            author_name.append(name)
            author_affiliation.append(affiliation)
    ff = open('/users/sds/downloads/result/socomp/author4_dis_dr.csv','w',encoding='utf-8')
    csv_writer = csv.writer(ff)
    num=len(author_name)
    for i in range(0,num):
        csv_writer.writerow([str(author_name[num-1-i]),str(author_affiliation[num-1-i])])
    ff.close()