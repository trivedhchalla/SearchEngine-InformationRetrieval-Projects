# Count the frequency of every word (a word is a sequence of alphanumeric characters, case does NOT matter) in the body of your document
# Write a 64 bit hash function for a word using polynomial rolling hash function

# hash(s) = s[0] + s[1]*p + s[2]*(p)**2 +....+ s[n-1]*(p)**(n-1) (mod m)

# Here s[i] is the ASCII for letter i in a word, use p = 53 and m = 264
# Compute Simhash for the document (as shown in slide 52)
# Modify your program to take two URLs from the web on the command line, print how many bits are common in their simhashes.

import subprocess as sp #for execute of curl or module used for automating terminal commands
import sys#for taking command line arguments
from bs4 import BeautifulSoup#for parsing the html

class SearchEngine:
    # simHash dict class variable since the search engine should store the simhash value for all documents and we will use it for indexing process
    simHashSearchEngine = {}# store Docname : hashvalue
    def __init__(self,url1):
        # all the attributes are private as a good practice 
        self._url = url1
        self._title = ""
        self._body = ""
        self._freqDoc = {}#stores word(key) : frequency(value)
        self._hashDict = {}#store word(key) : hash(value)
        self._links = []
    #getter methods for the private variables 
    #methods are returning 0 since the changes are made directly to the attributes and zero is used as successfull termination of program or not 
    def printUrl(self):
        print(self._url)
        return 0
    
    def printTitle(self):
        print(self._title)
        return 0
    
    def getBody(self):
        print(self._body)
        return 0
    
    def getLinks(self):
        print(self._links)
        return 0
    #methods are private and we call them in simhash when required
    # method for parsing the url using BeautifulSoup
    def _parseUrl(self):
        links = []
        try:
            html = sp.run(["curl", "-L", "-A", "Mozilla/5.0", self._url],   capture_output=True,text=True,encoding="utf-8").stdout
            parsedHTML1 = BeautifulSoup(html,"lxml")
            self._title = parsedHTML1.title.text
            self._body = parsedHTML1.get_text().lower()
            anchorTags = parsedHTML1.find_all('a')
            for link in anchorTags:
                self._links.append(link.get("href"))
        except Exception as e:
            print("Issue with website",e)
            print(e)
        return 0
    # method for generating word frequency of document
    # isalnum() is a string method to check for non-alphanumeric like \,/,+,-,*,etc
    def _freq(self):
        for word in self._body.split():
            if(word.isalnum()):#check for alphanumeric 
                if(self._freqDoc.get(word)):
                    self._freqDoc[word] += 1
                else:
                    self._freqDoc[word] = 1
        return 0
    # ord for char to ascii 
    # chr for ascii to char
    # bin() a built in function for converting number in a bit string
    # method for generating the Hash value of each word
    def _generateWordHash(self):
        m = 2 ** 64 # the value we should divide
        p = 53#is the prime number equal to no.of diff characters in input
        for word in self._freqDoc.keys():#taking word
            hashValue = 0#start hashvalue = 0
            for char in word:#take each char of word 
                hashValue = (hashValue * p + ord(char))#adding the ascci value and raise power p to prev hashvalue as function is p**i
            hashValue = hashValue % m #taking remainder after 
            self._hashDict[word] = format(hashValue,'064b')#converting the hashvalue into a 64 bit binary string 
        return 0
    # method for computation of simHash of a document using other methods
    def generateSimHash(self):
        self._parseUrl()
        self._freq()
        self._generateWordHash()
        fingerPrint = ""#the simhash 64 bit string
        bDimVector = [0]*64 #this the array storing the overall the value of ith element after iterating ith element of hashvalue of  each word
        for word,weight in self._freqDoc.items():#getting the word and weight(the frequency of word in document)
            hashWord = self._hashDict[word]#the 64 bit hashvalue of that word 
            for i in range(len(hashWord)):#iterating over 
                if(hashWord[i] == "1"):
                    bDimVector[i] += weight
                else:
                    bDimVector[i] -= weight 
        for i in bDimVector:#take each value and check pos or neg "1" or "0" respectively
            if( i > 0):
                fingerPrint += "1"
            else:
                fingerPrint += "0"
        self.simHashSearchEngine[self._title + self._url] = fingerPrint # title + url since the title can be same for multiple documents 
        return fingerPrint    
if(len(sys.argv) >= 3):
    url1 = sys.argv[1]
    url2 = sys.argv[2]
    search1 = SearchEngine(url1)
    simHash1 = search1.generateSimHash()
    search2 = SearchEngine(url2)
    simHash2 = search2.generateSimHash()
    # print(simHash1)
    # print(simHash2)
    similarBitCount = 0
    for i in range(64):
        if(simHash1[i] == simHash2[i]):
            similarBitCount += 1
    print(similarBitCount)
else:

    print("Please enter URLs")
