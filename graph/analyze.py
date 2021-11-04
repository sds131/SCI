import easygraph as eg
import csv

def make_graph(journal:str,time:int):
    G=eg.Graph()
    nodes=[]
    nodes_attr=[]
    edges=[]
    edges_attr=[]
    f=open('faculty-coauthors.csv','r')
    next(f)
    csv_reader=csv.reader(f)
    for row in csv_reader:
        if(int(row[6])==time and str(row[7])==journal):
            i=str(row[0])
            i_affifiation=str(row[1])
            i_country=str(row[2])
            j=str(row[3])
            j_affifiation=str(row[4])
            j_country=str(row[5])
            year=int(row[6])
            area=str(row[7])

            nodes.append(i)
            temp1={}
            temp1['affiliation']=i_affifiation
            temp1['country']=i_country
            nodes_attr.append(temp1)

            nodes.append(j)
            temp2={}
            temp2['affiliation']=j_affifiation
            temp2['country']=j_country
            nodes_attr.append(temp2)

            edges.append((i,j))
            temp3={}
            temp3['year']=year
            temp3['area']=area
            edges_attr.append(temp3)

            G.add_nodes(nodes,nodes_attr)
            G.add_edges(edges,edges_attr)

    return G

# draw weight journal year
# 2010 2015 2020
# tcss tsc socnets
# country

# tcss - 2010
G1=make_graph('tcss',2010)
# tcss - 2015
G2=make_graph('tcss',2015)
# tcss - 2020
G3=make_graph('tcss',2020)

def country_list(G:eg.Graph()):
    country={}
    for i in G.nodes():
        if i.country not in country:
            country.add(i.country)
            country[i.country]=1
        else:
            country[i.country]+=1
    return country

country1=sorted(country_list(G1).items(), key=lambda d: d[1],reverse=True)
country2=sorted(country_list(G2).items(), key=lambda d: d[1],reverse=True)
country3=sorted(country_list(G3).items(), key=lambda d: d[1],reverse=True)