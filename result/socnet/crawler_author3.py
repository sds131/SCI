import requests
from bs4 import BeautifulSoup
import csv
import json
import re


def fun(address):
    """
    headers = {
        'user-agent': '(Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36'    
    }
    driver = requests.get(address, headers=headers)
    soup = BeautifulSoup(driver.text, 'lxml')
    """
    from selenium import webdriver
    driver = webdriver.Chrome('/usr/local/bin/chromedriver')
    driver.set_page_load_timeout(60)
    driver.set_script_timeout(60)
    try:
        driver.get(address)
    except:
        driver.execute_script("window.stop()")

    #driver.get(address)
    html = driver.page_source
    soup = BeautifulSoup(html, 'lxml')
    
    content = soup.findAll('script', {'type':'application/json'})[0].text    
    content_json = json.loads(content)
    num=0
    for i in content_json['authors']['content'][0]['$$']:
        if i['#name']=='author':
            num+=1
    author_name=[]
    author_affiliation=[]

    d=0
    for i in range(0,num):
        for j in range(0,len(content_json['authors']['content'][0]['$$'][i]['$$'])):
            if content_json['authors']['content'][0]['$$'][i]['$$'][j]["#name"]=="cross-ref":
                if content_json['authors']['content'][0]['$$'][i]['$$'][j]["$"]["refid"]=="CORR1" or content_json['authors']['content'][0]['$$'][i]['$$'][j]["$"]["refid"]=="COR1" or "cor" in content_json['authors']['content'][0]['$$'][i]['$$'][j]["$"]["refid"] or content_json['authors']['content'][0]['$$'][i]['$$'][j]["$"]["refid"]=="FN1" or content_json['authors']['content'][0]['$$'][i]['$$'][j]["$"]["refid"]=="fn1" or "fn" in content_json['authors']['content'][0]['$$'][i]['$$'][j]["$"]["refid"]:
                    continue
                else:
                    d=1

    for i in range(0,num):
        name=[]
        for j in range(0,len(content_json['authors']['content'][0]['$$'][i]['$$'])):
            if content_json['authors']['content'][0]['$$'][i]['$$'][j]["#name"]=="given-name":
                name.append(content_json['authors']['content'][0]['$$'][i]['$$'][j]['_'])
            elif content_json['authors']['content'][0]['$$'][i]['$$'][j]["#name"]=="surname":
                name.append(content_json['authors']['content'][0]['$$'][i]['$$'][j]['_'])
            elif content_json['authors']['content'][0]['$$'][i]['$$'][j]['#name']=='suffix':
                name.append(content_json['authors']['content'][0]['$$'][i]['$$'][j]['_'])
            elif content_json['authors']['content'][0]['$$'][i]['$$'][j]["#name"]=="cross-ref":
                if content_json['authors']['content'][0]['$$'][i]['$$'][j]["$"]["refid"]!="CORR1" and content_json['authors']['content'][0]['$$'][i]['$$'][j]["$"]["refid"]!="COR1" and "cor" not in content_json['authors']['content'][0]['$$'][i]['$$'][j]["$"]["refid"] and content_json['authors']['content'][0]['$$'][i]['$$'][j]["$"]["refid"]!="FN1" and content_json['authors']['content'][0]['$$'][i]['$$'][j]["$"]["refid"]!="fn1" and "fn" not in content_json['authors']['content'][0]['$$'][i]['$$'][j]["$"]["refid"]:
                    kk=j
                    break
        cname=str()
        for k in range(0,len(name)-1):
            cname+=name[k]+' '
        cname+=name[len(name)-1]
        author_name.append(cname)
        if d==0:
            if i==0:
                t=str(content_json['authors']['affiliations'].values())
                temp = str(re.findall(r"'#name': 'textfn', '_': '(.*?)'", t))
                temp=temp[2:-2]
                affiliation=temp   
            else:
                affiliation=author_affiliation[0]
            author_affiliation.append(affiliation)
        else:
            s=content_json['authors']['content'][0]['$$'][i]['$$'][kk]['$']['refid']
            affiliation=content_json['authors']['affiliations'][s]['$$'][1]['_']
            author_affiliation.append(affiliation)

            """
            author_name1=content_json['authors']['content'][0]['$$'][i]['$$'][0]['_']
            author_name2=content_json['authors']['content'][0]['$$'][i]['$$'][1]['_']
            name=author_name1+' '+author_name2
            n=2
            if len(content_json['authors']['content'][0]['$$'][i]['$$'])>2:
                if content_json['authors']['content'][0]['$$'][i]['$$'][2]['#name']=='suffix':
                    author_name3=content_json['authors']['content'][0]['$$'][i]['$$'][2]['_']
                    name+=' '+author_name3
                    n=3
            author_name.append(name)
            ss=content_json['authors']['content'][0]['$$'][i]['$$'][n]['$']['refid']
            if ss=="CORR1":
                t=str(content_json['authors']['affiliations'].values())
                temp = str(re.findall(r"'#name': 'textfn', '_': '(.*?)'", t))
                temp=temp[2:-2]
                affiliation=temp
                d=0
            else:
                s=content_json['authors']['content'][0]['$$'][i]['$$'][2]['$']['refid']
                affiliation=content_json['authors']['affiliations'][s]['$$'][1]['_']
                d=1
            author_affiliation.append(affiliation)
        else:
            author_name1=content_json['authors']['content'][0]['$$'][i]['$$'][0]['_']
            author_name2=content_json['authors']['content'][0]['$$'][i]['$$'][1]['_']
            name=author_name1+' '+author_name2
            if len(content_json['authors']['content'][0]['$$'][i]['$$'])>2:
                if content_json['authors']['content'][0]['$$'][i]['$$'][2]['#name']=='suffix':
                    author_name3=content_json['authors']['content'][0]['$$'][i]['$$'][2]['_']
                    name+=' '+author_name3
            author_name.append(name)
            if d==0:
                affiliation=author_affiliation[0]
            else:
                s=content_json['authors']['content'][0]['$$'][i]['$$'][2]['$']['refid']
                affiliation=content_json['authors']['affiliations'][s]['$$'][1]['_']
            author_affiliation.append(affiliation)
        """

    ff = open('author3.csv','a',encoding='utf-8')
    csv_writer = csv.writer(ff)
    for i in range(0,num):
        csv_writer.writerow([str(author_name[i]),str(author_affiliation[i])])
    ff.close()
if __name__ == '__main__':
    
    f = open('/users/sds/downloads/address3.csv','r',encoding='utf-8')
    csv_reader=csv.reader(f)
    tt=0
    for row in csv_reader:
        if tt<685:
            tt+=1
            continue
        else:
            address=str(row)
            address=address[3:-3]
            fun(address)
            tt=tt+1
            print(tt)

    
    """
    address="https://www.sciencedirect.com/science/article/abs/pii/S0378873399000143?via%3Dihub"
    fun(address)
    address="https://www.sciencedirect.com/science/article/abs/pii/S0378873398000100?via%3Dihub"
    fun(address)
    address="https://www.sciencedirect.com/science/article/abs/pii/S0378873398000112?via%3Dihub"
    fun(address)



    <script type="application/json" data-iso-key="_0">{"abstracts":{"content":[{"$$":[{"#name":"section-title","_":"Abstract"},{"$$":[{"$":{"view":"all"},"#name":"simple-para","_":"Social network data often involve transitivity, homophily on observed attributes, community structure, and heterogeneity of actor degrees. We propose a latent cluster random effects model to represent all of these features, and we develop Bayesian inference for it. The model is applicable to both binary and non-binary network data. We illustrate the model using two real datasets: liking between monks and coreaderships between Slovenian publications. We also apply it to two simulated network datasets with very different network structure but the same highly skewed degree sequence generated from a preferential attachment process. One has transitivity and community structure while the other does not. Models based solely on degree distributions, such as scale-free, preferential attachment and power-law models, cannot distinguish between these very different situations, but the latent cluster random effects model does."}],"$":{"id":"aep-abstract-sec-id13"},"#name":"abstract-sec"}],"$":{"id":"aep-abstract-id12","class":"author"},"#name":"abstract"}],"floats":[],"footnotes":[],"attachments":[]},"adobeTarget":{"universal-view-pdf":{"variation":"A"}},"article":{"accessOptions":{"linkType":"PURCHASE","linkUrl":"/getaccess/pii/S0378873309000173","price":{"currency":"USD","totalPrice":35.95}},"analyticsMetadata":{"accountId":"228598","accountName":"ScienceDirect Guests","loginStatus":"anonymous","userId":"12975512","isLoggedIn":false},"cid":"271850","content-family":"serial","copyright-line":"Copyright © 2009 Elsevier B.V. All rights reserved.","cover-date-years":["2009"],"cover-date-start":"2009-07-01","cover-date-text":"July 2009","document-subtype":"fla","document-type":"article","eid":"1-s2.0-S0378873309000173","doi":"10.1016/j.socnet.2009.04.001","first-fp":"204","hub-eid":"1-s2.0-S0378873309X00031","issuePii":"S0378873309X00031","iss-first":"3","item-weight":"FULL-TEXT","language":"en","last-lp":"213","last-author":{"#name":"last-author","$":{"xmlns:ce":true,"xmlns:dm":true,"xmlns:sb":true},"$$":[{"#name":"author","$":{"id":"aep-author-id10"},"$$":[{"#name":"given-name","_":"Peter D."},{"#name":"surname","_":"Hoff"},{"#name":"cross-ref","$":{"refid":"fn4"},"$$":[{"#name":"sup","$":{"loc":"post"},"_":"4"}]}]}]},"normalized-first-auth-initial":"P","normalized-first-auth-surname":"KRIVITSKY","pages":[{"last-page":"213","first-page":"204"}],"pii":"S0378873309000173","srctitle":"Social Networks","timestamp":"2015-05-14T08:13:49.67509-04:00","title":{"content":[{"#name":"title","_":"Representing degree distributions, clustering, and homophily in social networks with latent cluster random effects models"}],"floats":[],"footnotes":[],"attachments":[]},"vol-first":"31","vol-iss-suppl-text":"Volume 31, Issue 3","userSettings":{"forceAbstract":false,"creditCardPurchaseAllowed":true,"blockFullTextForAnonymousAccess":false,"disableWholeIssueDownload":false,"preventTransactionalAccess":false,"preventDocumentDelivery":true},"contentType":"JL","crossmark":false,"document-references":29,"freeHtmlGiven":false,"userProfile":{"departmentName":"ScienceDirect Guests","accessType":"GUEST","accountId":"228598","webUserId":"12975512","accountName":"ScienceDirect Guests","departmentId":"291352","userType":"NORMAL","hasMultipleOrganizations":false},"access":{"openAccess":false,"openArchive":false},"aipType":"none","articleEntitlement":{"entitled":false,"isCasaUser":false,"usageInfo":"(12975512,U|291352,D|228598,A|3,P|2,PL)(SDFE,CON|a7ca56990f951-4729-994b-1515372abc8egxrqa,SSO|ANON_GUEST,ACCESS_TYPE)"},"isThirdParty":false,"crawlerInformation":{"canCrawlPDFContent":false,"isCrawler":false},"dates":{"Available online":"26 May 2009","Revised":[],"Publication date":"1 July 2009"},"displayViewFullText":false,"downloadFullIssue":false,"entitlementReason":"unsubscribed","headerConfig":{"helpUrl":"https://service.elsevier.com/app/home/supporthub/sciencedirect/","contactUrl":"https://service.elsevier.com/app/contact/supporthub/sciencedirect/","userName":"","userEmail":"","orgName":"ScienceDirect Guests","webUserId":"12975512","libraryBanner":{},"shib_regUrl":"","tick_regUrl":"","recentInstitutions":[],"canActivatePersonalization":false,"hasInstitutionalAssociation":false,"hasMultiOrg":false,"userType":"GUEST","userAnonymity":"ANON_GUEST","allowCart":true,"environment":"prod","cdnAssetsHost":"https://sdfestaticassets-us-east-1.sciencedirectassets.com"},"indexTag":true,"isCorpReq":false,"issn":"03788733","issn-primary-formatted":"0378-8733","issRange":"3","pdfEmbed":false,"publication-content":{"noElsevierLogo":false,"imprintPublisher":{"displayName":"North-Holland","id":"68"},"isSpecialIssue":false,"isSampleIssue":false,"transactionsBlocked":false,"publicationOpenAccess":{"oaStatus":"","oaArticleCount":51,"openArchiveStatus":false,"openArchiveArticleCount":0,"openAccessStartDate":"","oaAllowsAuthorPaid":true},"issue-cover":{"attachment":[{"attachment-eid":"1-s2.0-S0378873309X00031-cov200h.gif","file-basename":"cov200h","extension":"gif","filename":"cov200h.gif","ucs-locator":["https://s3.amazonaws.com/prod-ucs-content-store-us-east/content/pii:S0378873309X00031/loc/DOWNSAMPLED200/image/gif/8b6b1bba0bea0deb646928d18a5ccf84/cov200h.gif","https://s3-eu-west-1.amazonaws.com/prod-ucs-content-store-eu-west/content/pii:S0378873309X00031/loc/DOWNSAMPLED200/image/gif/8b6b1bba0bea0deb646928d18a5ccf84/cov200h.gif"],"attachment-type":"IMAGE-COVER-H200","filesize":"13630","pixel-height":"200","pixel-width":"149"},{"attachment-eid":"1-s2.0-S0378873309X00031-cov150h.gif","file-basename":"cov150h","extension":"gif","filename":"cov150h.gif","ucs-locator":["https://s3.amazonaws.com/prod-ucs-content-store-us-east/content/pii:S0378873309X00031/loc/DOWNSAMPLED/image/gif/ceae0ea0037f4792f96052436fef09f4/cov150h.gif","https://s3-eu-west-1.amazonaws.com/prod-ucs-content-store-eu-west/content/pii:S0378873309X00031/loc/DOWNSAMPLED/image/gif/ceae0ea0037f4792f96052436fef09f4/cov150h.gif"],"attachment-type":"IMAGE-COVER-H150","filesize":"9321","pixel-height":"150","pixel-width":"112"}]},"smallCoverUrl":"https://ars.els-cdn.com/content/image/S03788733.gif","title":"social-networks","contentTypeCode":"JL","sourceOpenAccess":false,"publicationCoverImageUrl":"https://ars.els-cdn.com/content/image/1-s2.0-S0378873309X00031-cov150h.gif"},"useEnhancedReader":true,"volRange":"31","features":["keywords","references","preview"],"open-research":{},"self-archiving":{},"titleString":"Representing degree distributions, clustering, and homophily in social networks with latent cluster random effects models","usesAbstractUrl":true,"renderingMode":"Abstract","isAbstract":true,"isContentVisible":false,"ajaxLinks":{"citingArticles":true,"referredToBy":true,"toc":true,"recommendations":true,"authorMetadata":true},"eligibleForUniversalPdf":true},
    "authors":{"content":[{"#name":"author-group","$$":[
        {"#name":"author","$":{"id":"aep-author-id7"},"$$":[{"#name":"given-name","_":"Pavel N."},{"#name":"surname","_":"Krivitsky"},{"#name":"cross-ref","$":{"refid":"cor1"},"$$":[{"#name":"sup","$":{"loc":"post"},"_":"⁎"}]},{"#name":"cross-ref","$":{"refid":"fn1"},"$$":[{"#name":"sup","$":{"loc":"post"},"_":"1"}]},{"#name":"cross-ref","$":{"refid":"fn2"},"$$":[{"#name":"sup","$":{"loc":"post"},"_":"2"}]},{"#name":"e-address","$":{"type":"email"},"_":"pavel@stat.washington.edu"}]},
        {"#name":"author","$":{"id":"aep-author-id8"},"$$":[{"#name":"given-name","_":"Mark S."},{"#name":"surname","_":"Handcock"},{"#name":"cross-ref","$":{"refid":"fn1"},"$$":[{"#name":"sup","$":{"loc":"post"},"_":"1"}]}]},
        {"#name":"author","$":{"id":"aep-author-id9"},"$$":[{"#name":"given-name","_":"Adrian E."},{"#name":"surname","_":"Raftery"},{"#name":"cross-ref","$":{"refid":"fn3"},"$$":[{"#name":"sup","$":{"loc":"post"},"_":"3"}]}]},
        {"#name":"author","$":{"id":"aep-author-id10"},"$$":[{"#name":"given-name","_":"Peter D."},{"#name":"surname","_":"Hoff"},{"#name":"cross-ref","$":{"refid":"fn4"},"$$":[{"#name":"sup","$":{"loc":"post"},"_":"4"}]}]},
        {"#name":"affiliation","$":{"id":"aep-affiliation-id11"},"$$":[{"#name":"textfn","_":"University of Washington, Seattle, United States"}]},{"#name":"correspondence","$":{"id":"cor1"},"$$":[{"#name":"label","_":"⁎"},{"#name":"text","_":"Corresponding author at: University of Washington, Department of Statistics, Box 354322, Seattle, WA 98195-4322, USA. Tel.: +1 206 543 8797; fax: +1 206 685 7419."}]},{"#name":"footnote","$":{"id":"fn1"},"$$":[{"#name":"label","_":"1"},{"#name":"note-para","_":"Supported by NIDA Grant DA012831, DoD ONR MURI award N00014–08–1–1015 and NICHD Grant HD041877."}]},{"#name":"footnote","$":{"id":"fn2"},"$$":[{"#name":"label","_":"2"},{"#name":"note-para","_":"Supported by NIH Grant 8 R01EB 002137–02 and NSF Grant 0729438."}]},{"#name":"footnote","$":{"id":"fn3"},"$$":[{"#name":"label","_":"3"},{"#name":"note-para","_":"Supported by NIH Grant 8 R01EB 002137–02 and NICHD Grant R01 HD054511."}]},{"#name":"footnote","$":{"id":"fn4"},"$$":[{"#name":"label","_":"4"},{"#name":"note-para","_":"Supported by NSF Grant 0631531."}]}]}],"floats":[],"footnotes":[{"#name":"footnote","$":{"id":"fn1"},"$$":[{"#name":"label","_":"1"},{"#name":"note-para","_":"Supported by NIDA Grant DA012831, DoD ONR MURI award N00014–08–1–1015 and NICHD Grant HD041877."}]},{"#name":"footnote","$":{"id":"fn2"},"$$":[{"#name":"label","_":"2"},{"#name":"note-para","_":"Supported by NIH Grant 8 R01EB 002137–02 and NSF Grant 0729438."}]},{"#name":"footnote","$":{"id":"fn3"},"$$":[{"#name":"label","_":"3"},{"#name":"note-para","_":"Supported by NIH Grant 8 R01EB 002137–02 and NICHD Grant R01 HD054511."}]},{"#name":"footnote","$":{"id":"fn4"},"$$":[{"#name":"label","_":"4"},{"#name":"note-para","_":"Supported by NSF Grant 0631531."}]}],"affiliations":{"aep-affiliation-id11":{"#name":"affiliation","$":{"id":"aep-affiliation-id11"},"$$":[{"#name":"textfn","_":"University of Washington, Seattle, United States"}]}},"correspondences":{"cor1":{"#name":"correspondence","$":{"id":"cor1"},"$$":[{"#name":"label","_":"⁎"},{"#name":"text","_":"Corresponding author at: University of Washington, Department of Statistics, Box 354322, Seattle, WA 98195-4322, USA. Tel.: +1 206 543 8797; fax: +1 206 685 7419."}]}},"attachments":[],"scopusAuthorIds":{},"articles":{}},"authorMetadata":[],"banner":{"expanded":false},"biographies":{},"body":{},"browser":{"name":"Chrome","engine":"Blink"},"chapters":{"toc":[],"isLoading":false},"changeViewLinks":{"showFullTextLink":true,"showAbstractLink":false},"citingArticles":{},"clinicalKey":{},"combinedContentItems":{"content":[{"#name":"keywords","$$":[{"#name":"keywords","$":{"xmlns:ce":true,"xmlns:aep":true,"xmlns:xoe":true,"xmlns:mml":true,"xmlns:xs":true,"xmlns:xlink":true,"xmlns:xocs":true,"xmlns:tb":true,"xmlns:xsi":true,"xmlns:cals":true,"xmlns:sb":true,"xmlns:ja":true,"xmlns":true,"class":"keyword","id":"aep-keywords-id14"},"$$":[{"#name":"section-title","_":"Keywords"},{"#name":"keyword","$$":[{"#name":"text","_":"Bayesian inference"}]},{"#name":"keyword","$$":[{"#name":"text","_":"Latent variable"}]},{"#name":"keyword","$$":[{"#name":"text","_":"Markov chain Monte Carlo"}]},{"#name":"keyword","$$":[{"#name":"text","_":"Model-based clustering"}]},{"#name":"keyword","$$":[{"#name":"text","_":"Small world network"}]},{"#name":"keyword","$$":[{"#name":"text","_":"Scale-free network"}]}]}]}],"floats":[],"footnotes":[],"attachments":[]},"crossMark":{"isOpen":false},"downloadIssue":{"openOnPageLoad":false,"isOpen":false,"downloadCapOpen":false,"articles":[],"selected":[]},"enrichedContent":{"tableOfContents":false,"researchData":{"hasResearchData":false,"dataProfile":{},"openData":{},"mendeleyData":{},"databaseLinking":{}},"geospatialData":{"attachments":[]},"interactiveCaseInsights":{},"virtualMicroscope":{}},"entitledRecommendations":{"openOnPageLoad":false,"isOpen":false,"articles":[],"selected":[],"currentPage":1,"totalPages":1},"exam":{},"glossary":{},"issueNavigation":{"previous":{},"next":{}},"linkingHubLinks":[],"metrics":{"isOpen":true},"preview":{},"purchasePdf":{"isOpen":false},"rawtext":"","recommendations":{},"references":{},"referenceLinks":{"internal":[],"external":[]},"refersTo":{},"referredToBy":{},"relatedContent":{"isModal":false,"isOpenSpecialIssueArticles":false,"isOpenRecommendations":true,"isOpenCitingArticles":false,"citingArticles":[false,false,false],"recommendations":[false,false,false,false,false,false],"specialIssueArticles":[false,false,false]},"seamlessAccess":{},"signInFromEmail":{"isOpen":false},"specialIssueArticles":{},"supplementaryFilesData":[],"tableOfContents":{"showEntitledTocLinks":false},"tail":{},"transientError":{"isOpen":false},"userAgent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36","workspace":{"isOpen":false},"viewConfig":{"articleFeature":{"rightsAndContentLink":true},"pathPrefix":""},"viewOnlyPdf":{"showViewOnlyPdfButton":false,"token":""},"virtualSpecialIssue":{"showVirtualSpecialIssueLink":false}}</script>

"""
    