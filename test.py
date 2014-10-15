import oauth2 as oauth
import urlparse 
import time


consumer_key           = "77isgsk67moiyi"
consumer_secret        = "A8jGsvz4D21n3s01"
consumer = oauth.Consumer(consumer_key, consumer_secret)
client = oauth.Client(consumer)
request_token_url      = 'https://api.linkedin.com/uas/oauth/requestToken'
resp, content = client.request(request_token_url, "POST")
if resp['status'] != '200':
    raise Exception("Invalid response %s." % resp['status'])
 
request_token = dict(urlparse.parse_qsl(content))


authorize_url =      'https://api.linkedin.com/uas/oauth/authorize'
print "Go to the following link in your browser:"
print "%s?oauth_token=%s" % (authorize_url, request_token['oauth_token'])


accepted = 'n'
while accepted.lower() == 'n':
    accepted = raw_input('Have you authorized me? (y/n) ')
oauth_verifier = raw_input('What is the PIN? ')


access_token_url = 'https://api.linkedin.com/uas/oauth/accessToken'
token = oauth.Token(request_token['oauth_token'], request_token['oauth_token_secret'])
token.set_verifier(oauth_verifier)
client = oauth.Client(consumer, token)

 
resp, content = client.request(access_token_url, "POST")


access_token = dict(urlparse.parse_qsl(content))
print "Access Token:"
print "    - oauth_token        = %s" % access_token['oauth_token']
print "    - oauth_token_secret = %s" % access_token['oauth_token_secret']
print
print "You may now access protected resources using the access tokens above."
print
url = "http://api.linkedin.com/v1/people/~"

consumer = oauth.Consumer(
  
     key= consumer_key ,
     secret= consumer_secret)

token = oauth.Token(
     key="bc403344-9c8c-4ede-abf7-357f7989f433", 
     secret="8643fe09-0390-4323-b432-1273db652b88")


client = oauth.Client(consumer, token)

resp, content = client.request(url)
print resp
print content

##!/usr/bin/python
## 
##import urllib
##import urllib2
##import sys
##import time
##import copy
##import pickle
##import math
## 
##from person import person_searchobj
##from HTMLParser import HTMLParser
##from GoogleQueery import GoogleQueery
## 
##TODO add a test function that tests the website format for easy diagnostics when HTML changes
##TODO use HTMLParser like a sane person
##class LinkedinPageGatherer():
##  """
##  class that generates the initial linkeding queeries using the company name
##  as a search parameter. These search strings will be searched using google
##  to obtain additional information (these limited initial search strings usually lack
##  vital info like names)
##  """
##  def __init__(self, companyName, login, password, maxsearch=100,
##               totalresultpercent=.7, maxskunk=100):
##    """
##    login and password are params for a valid linkedin account
##    maxsearch is the number of results - linkedin limit unpaid accounts to 100
##    totalresultpercent is the number of results this script will try to find
##    maxskunk is the number of searches this class will attempt before giving up
##    """
##    #list of person_searchobj
##    self.people_searchobj = []
##    self.companyName = companyName
##    self.login = login
##    self.password = password
##    self.fullurl = ("https://www.linkedin.com/vsearch/p?","page_num=1","&company="+companyName+"&companyScope=currentCompany")
##    self.opener = self.linkedin_login()
##    #for the smart_people_adder
##    self.searchSpecific = []
##    #can only look at 100 people at a time. Parameters used to narrow down queries
##    self.total_results = self.get_num_results()
##    self.maxsearch = maxsearch
##    self.totalresultpercent = totalresultpercent
##    #self.extraparameters = {"locationinfo" : [], "titleinfo" : [], "locationtitle" : [] }
##    #extraparameters is a simple stack that adds keywords to restrict the search
##    self.extraparameters = []
##    #TODO can only look at 100 people at a time - like to narrow down queries
##    #and auto grab more
##    currrespercent = 0.0
##    skunked = 0
##    currurl = self.fullurl[0] + self.fullurl[1]+ self.fullurl[2]
##    extraparamindex = 0
## 
##    while currrespercent < self.totalresultpercent and skunked <= maxskunk:
##      numresults = self.get_num_results(currurl)
##      save_num = len(self.people_searchobj)
## 
##      print "-------"
##      print "currurl", currurl
##      print "percentage", currrespercent
##      print "skunked", skunked
##      print "numresults", numresults
##      print "save_num", save_num
## 
##      for i in range (0, int(self.maxsearch/10)):
##        #function adds to self.people_searchobj
##        print "currurl" + currurl
##        self.return_people_links(currurl)
##      currrespercent = float(len(self.people_searchobj))/self.total_results
##      if save_num == len(self.people_searchobj):
##        skunked += 1
##      for i in self.people_searchobj:
##        pushTitles = [("title", gName) for gName in i.givenName.split()]
##        #TODO this could be inproved for more detailed results, etc, but keeping it simple for now
##        pushKeywords = [("keywords", gName) for gName in i.givenName.split()]
##        pushTotal = pushTitles[:] + pushKeywords[:]
##        #append to extraparameters if unique
##        self.push_search_parameters(pushTotal)
##      print "parameters", self.extraparameters
##      #get a new url to search for, if necessary
##      #use the extra params in title, "keywords" parameters
##      try:
##        refineel = self.extraparameters[extraparamindex]
##        extraparamindex += 1
##        currurl = self.fullurl[0] + "&" + refineel[0] + "=" + refineel[1] + self.fullurl[1]
##      except IndexError:
##        break
## 
##  """
##  #TODO: This idea is fine, but we should get names first to better distinguish people
##  #also maybe should be moved
##  def smart_people_adder(self):
##    #we've already done a basic search, must do more
##    if "basic" in self.searchSpecific:
##  """
##  def return_people_links(self, linkedinurl):
##    req = urllib2.Request(linkedinurl)
##    fd = self.opener.open(req)
##    pagedata = ""
##    while 1:
##      data = fd.read(2056)
##      pagedata = pagedata + data
##      if not len(data):
##        break
##    #print pagedata
##    self.parse_page(pagedata)
## 
##  def parse_page(self, page):
##    thesePeople = HTMLParser()
##    thesePeople.feed(page)
##    for newperson in thesePeople.personArray:
##      unique = True
##      for oldperson in self.people_searchobj:
##        #if all these things match but they really are different people, they
##        #will likely still be found as unique google results
##        if (oldperson.givenName == newperson.givenName and
##            oldperson.familyName == newperson.familyName and
##            oldperson.title == newperson.title and
##            oldperson.location == oldperson.location):
##              unique = False
##              break
##      if unique:
##        self.people_searchobj.append(newperson)
##  """
##    print "======================="
##    for person in self.people_searchobj:
##      print person.goog_printstring()
##  """
## 
##  #return the number of results, very breakable
##  def get_num_results(self, url=None):
##    #by default return total in company
##    if url == None:
##      fd = self.opener.open(self.fullurl[0] + "1")
##      print fd 
##    else:
##      fd = self.opener.open(url)
##    data = fd.read()
##    fd.close()
##    searchstr = "<p class=\"summary\">"
##    sindex = data.find(searchstr) + len(searchstr)
##    eindex = data.find("</strong>", sindex)
##    return(int(data[sindex:eindex].strip().strip("<strong>").replace(",", "").strip()))
## 
##  #returns an opener object that contains valid cookies
##  def linkedin_login(self):
##    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor())
##    urllib2.install_opener(opener)
##    #login page
##    fd = opener.open("https://www.linkedin.com/secure/login?trk=hb_signin")
##    data = fd.read()
##    fd.close()
##    #csrf 'prevention' login value
##    searchstr = """<input type="hidden" name="csrfToken" value="ajax:"""
##    sindex = data.find(searchstr) + len(searchstr)
##    eindex = data.find('"', sindex)
##    params = urllib.urlencode(dict(csrfToken="ajax:-"+data[sindex:eindex],
##                              session_key=self.login,
##                              session_password=self.password,
##                              session_login="Sign+In",
##                              session_rikey=""))
##    print params
##    #need the second request to get the csrf stuff, initial cookies
##    request = urllib2.Request("https://www.linkedin.com/secure/login")
##    request.add_header("Host", "www.linkedin.com")
##    request.add_header("Referer", "https://www.linkedin.com/secure/login?trk=hb_signin")
##    time.sleep(1.5)
##    fd = opener.open(request, params)
##    data = fd.read()
##    if "<div id=\"header\" class=\"guest\">" in data:
##      print "Linkedin authentication faild. Please supply a valid linkedin account"
##      sys.exit(1)
##    else:
##      print "Linkedin authentication Successful"
##    fd.close()
##    return opener
## 
##  def push_search_parameters(self, extraparam):
##    uselesswords = [ "for", "the", "and", "at", "in"]
##    for pm in extraparam:
##      pm = (pm[0], pm[1].strip().lower())
##      if (pm not in self.extraparameters) and (pm[1] not in uselesswords) and pm != None:
##        self.extraparameters.append(pm)
## 
##class LinkedinTotalPageGather(LinkedinPageGatherer):
##  """
##  Overhead class that generates the person_searchobjs, using GoogleQueery
##  """
##  def __init__(self, companyName, login, password):
##    LinkedinPageGatherer.__init__(self, companyName, login, password)
##    extraPeople = []
##    for person in self.people_searchobj:
##      mgoogqueery = GoogleQueery(person.goog_printstring())
##      #making the assumption that each pub url is a unique person
##      count = 0
##      for url in mgoogqueery.linkedinurl:
##        #grab the real name from the url
##        begindex = url.find("/pub/") + 5
##        endindex = url.find("/", begindex)
##        if count == 0:
##          person.url = url
##          person.name = url[begindex:endindex]
##        else:
##          extraObj = copy.deepcopy(person)
##          extraObj.url = url
##          extraObj.name = url[begindex:endindex]
##          extraPeople.append(extraObj)
##        count += 1
##      print person
##    print "Extra People"
##    for person in extraPeople:
##      print person
##      self.people_searchobj.append(person)
## 
##if __name__ == "__main__":
##  #args are email and password for linkedin
##  my = LinkedinTotalPageGather("IBM", sys.argv[1], sys.argv[2])
## 
