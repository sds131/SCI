from csrankings import *
import json
import gzip
import csv

authorPaperCountThreshold = 0

startyear = 1990
endyear   = 2021

def csv2dict_str_str(fname):
    """Takes a CSV file and returns a dictionary of pairs."""
    with open(fname, mode='r') as infile:
        rdr = csv.reader(infile)
        d = {str(rows[0].strip()): str(rows[1].strip()) for rows in rdr}
    return d

def parseDBLP(facultydict):
    coauthors = {}
    papersWritten = {}
    counter = 0
    with gzip.open('dblp.xml.gz') as f:

        oldnode = None
        
        for (event, node) in ElementTree.iterparse(f, events=['start', 'end'],load_dtd=True):

            if (oldnode is not None):
                oldnode.clear()
            oldnode = node
            
            foundArticle = False
            inRange = False
            authorsOnPaper = 0
            authorName = ""
            confname = ""
            year = -1
            
            if (node.tag == 'inproceedings' or node.tag == 'article'):
                
                # Check that dates are in the specified range.
                
                # First, check if this is one of the conferences we are looking for.
                
                for child in node:
                    if (child.tag == 'booktitle' or child.tag == 'journal'):
                        if True: # INCLUDE ALL VENUES
                            # if (confname in confdict):
                            foundArticle = True
                            confname = child.text
                        break
                    if (child.tag == 'volume'):
                        volume = child.text
                    if (child.tag == 'number'):
                        number = child.text
                    if child.tag == 'year':
                        if child.text is not None:
                            year = int(child.text)

                if (not foundArticle):
                    # Nope.
                    continue

                # It's a booktitle or journal, and it's one of our conferences.

                # Check that dates are in the specified range.
                
                if ((year >= startyear) and (year <= endyear)):
                    inRange = True

                if (not inRange):
                    # Out of range.
                    continue

                # Count the number of pages. It needs to exceed our threshold to be considered.
                pageCount = -1
                for child in node:
                    if (child.tag == 'pages'):
                        pageCount = pagecount(child.text)

                tooFewPages = False
                if ((pageCount != -1) and (pageCount < pageCountThreshold)):
                    tooFewPages = True

                if (tooFewPages):
                    continue

                coauthorsList = []
                if not confname in confdict:
                    areaname = "na"
                else:
                    areaname = confdict[confname]

                for child in node:
                    if (child.tag == 'author'):
                        authorName = child.text
                        authorName = authorName.strip()
                        if (True): # authorName in facultydict):
                            authorsOnPaper += 1
                            if (not authorName in coauthors):
                                coauthors[authorName] = {}
                            if (not (year,areaname) in coauthors[authorName]):
                                coauthors[authorName][(year,areaname)] = set([])
                            coauthorsList.append(authorName)
                            papersWritten[authorName] = papersWritten.get(authorName, 0) + 1

                # No authors? Bail.
                if (authorsOnPaper == 0):
                    continue
                
                counter = counter + 1
                
                for child in node:
                    if (child.tag == 'author'):
                        authorName = child.text
                        authorName = authorName.strip()
                        if (authorName in facultydict):
                            for coauth in coauthorsList:
                                if (coauth != authorName):
                                    if (coauth in facultydict):
                                        coauthors[authorName][(year,areaname)].add(coauth)
                                        coauthors[coauth][(year,areaname)].add(authorName)

    author={}
    f1=open('csrankings.csv','r')
    csv_reader=csv.reader(f1)
    for row in csv_reader:
        k=str(row[0])
        v=str(row[1])
        author[k]=v

    affiliation={}
    f2=open('country-info 2.csv','r')
    csv_reader=csv.reader(f2)
    for row in csv_reader:
        k=str(row[0])
        v=str(row[2])
        affiliation[k]=v

    o = open('faculty-coauthors.csv', 'w')
    o.write('"author","author_affiliation","author_country","coauthor","coauthor_affiliation","coauthor_country","year","area"\n')
    for auth in coauthors:
        if (auth in facultydict):
            for (year,area) in coauthors[auth]:
                for coauth in coauthors[auth][(year,area)]:
                    if (papersWritten[coauth] >= authorPaperCountThreshold):
                        if(area!='na'):
                            o.write(auth)
                            # o.write(auth.encode('utf-8'))
                            o.write(',')
                            o.write(author[auth])
                            o.write(',')
                            o.write(affiliation[author[auth]])
                            o.write(',')
                            o.write(coauth)
                            # o.write(coauth.encode('utf-8'))
                            o.write(',')
                            o.write(author[coauth])
                            o.write(',')
                            o.write(affiliation[author[coauth]])
                            o.write(',')
                            o.write(str(year))
                            o.write(',')
                            o.write(area)
                            o.write('\n')
    o.close()
    
    return 0


facultydict = csv2dict_str_str('faculty-affiliations.csv')

parseDBLP(facultydict)

