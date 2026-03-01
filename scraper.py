# Write a python program that takes a URL on the command line, fetches the page, and outputs (one per line).
# 1. Page Title(without any html tags)
# 2. Page Body (just the text, without any html tags)
# 3. All the URLs that the page points/link to

import subprocess as sp #for execute of curl or module used for automating terminal commands
import sys#for taking command line arguments
from bs4 import BeautifulSoup#for parsing the html
class SearchEngine:
    def __init__(self,url1):
        # all the attributes are private as a good practice 
        self._url = url1
        self._title = ""
        self._body = ""
        self._links = []
    #methods are private and we call them in simhash when required
    # method for parsing the url using BeautifulSoup
    def parseUrl(self):
        links = []
        try:
            #using the below thing as some web site might not allow robot downloading the content 
            # for acess purpose as learnt in web-scraping (DHP-course)
            html = sp.run(["curl", "-L", "-A", "Mozilla/5.0", self._url],   capture_output=True,text=True,encoding="utf-8").stdout
            parsedHTML1 = BeautifulSoup(html,"html.parser")#using builtin parser
            self._title = parsedHTML1.title.text
            self._body = self._body = " ".join(parsedHTML1.get_text().split())
            anchorTags = parsedHTML1.find_all('a')
            for link in anchorTags:#for getting link of other documents from anchor tags
                self._links.append(link.get("href"))
        except Exception as e:# as some document might have body or don't allow crawling 
            print("Issue with website",e)
            print(e)
        return 0
    def printLinks(self):
        for link in self._links:
            print(link)
        return 0
    def printTitle(self):
        print(self._title)
        return 0

    def printBody(self):
        print(self._body)
        return 0    

if(len(sys.argv) >= 2):
    url1 = sys.argv[1]
    search1 = SearchEngine(url1)
    search1.parseUrl()
    search1.printTitle()
    search1.printBody()
    search1.printLinks()
else:

    print("Please enter correct number of arguments")

