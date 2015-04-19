import urllib2
import re
from bs4 import BeautifulSoup


opener = urllib2.build_opener()
opener.addheaders = [{'User-agent' , 'Mozilla/5.0'}]

#------------begin findPhoneNumber ---------------------------------

def findPhoneNumber(webaddress):
     dict={}
     url = (webaddress)
     ourUrl = opener.open(url).read()
     soup = BeautifulSoup(ourUrl)
     text = (soup.body.get_text())
     
     text = re.sub("[^a-zA-Z0-9]",'',text)
     match = re.search(r'\d\s*\d\s*\d\s*\d\s*\d\s*\d\s*\d\s*\d\s*\d\s*\d', text)
     # If-statement after search() tests if it succeeded
     if match:                      
          if match.group()[0] == '1':
                    match = re.search(r'\d\s*\d\s*\d\s*\d\s*\d\s*\d\s*\d\s*\d\s*\d\s*\d\s*\d', text)
                    if match:
                         return match.group()
          else: return match.group()
     

     return 'no match'

#print findPhoneNumber('http://fullbloomlandscape.com')

#-------------begin Link Finder -----------------------------------------

def findLinks(webaddress):
     dict={}
     url = (webaddress)
     ourUrl = opener.open(url).read()
     soup = BeautifulSoup(ourUrl)
     #finds relative links only
     for link in soup.find_all('a', href=re.compile(r'^(?!(?:[a-zA-Z][a-zA-Z0-9+.-]*:|//))')):          
          #confirms not already added to dictionary
          if (link.get('href')) not in dict:
               #confirms there is text in the link
               if (link.get_text())  != ' ' and (link.get_text())  != '':
                    pageName = (link.get_text())
                    pageName = re.sub('\xa0Us',' ',pageName)
                    pageName = re.sub('\n','',pageName)
                    pageName = re.sub('\r','',pageName)
                    pageName = re.sub('\t','',pageName)
                    if len(pageName) > 2 and len(pageName) < 15:
                         dict[((link.get('href')))] = pageName     


     if len(dict)< 3:
          #more robust method for sites with no link text
          return findLinksSecondTry(soup)
          
          
     else: return dict

def findLinksSecondTry(soup):
     dict = {}
     for link in soup.find_all('a', href=re.compile(r'^(?!(?:[a-zA-Z][a-zA-Z0-9+.-]*:|//))')):          
          #confirms not already added to dictionary
          if (link.get('href')) not in dict:
               #below code should set url value in dictionary to url without entension, aboutus.html becomes ABOUTUS, we should have tool for common names so aboutus and contactus become CONTACT US
               pageName = (link.get('href'))
               pageName = pageName.upper()
               pageName = re.sub('_',' ',pageName)
               pageName = re.sub('-',' ',pageName)
               regexp = re.compile(r'HOME')
               if regexp.search(pageName) is not None:
                    pageName = 'HOME'
               regexp = re.compile(r'ABOUT')
               if regexp.search(pageName) is not None:
                    pageName = 'ABOUT US'
               regexp = re.compile(r'CONTACT')
               if regexp.search(pageName) is not None:
                    pageName = 'CONTACT'
               regexp = re.compile(r'SERVICE')
               if regexp.search(pageName) is not None:
                    pageName = 'SERVICES'
               regexp = re.compile(r'PORTFOLIO')
               if regexp.search(pageName) is not None:
                    pageName = 'PORTFOLIO' 
               dict[((link.get('href')))] = pageName
     if len(dict)< 3:
          dict = { 'home.html' : 'Home' , 'about_us.html' : 'About Us' , 'contact.html' : 'Contact' } 
     return dict


#--------------------Begin White  Scrape -------------------------------
#returns formated string of address by looking up address in whitepages reverse lookup (just need phone number)
def whiteScrape(webaddress):
     url = ('file:///Users/user/Documents/programming/1-978-251-1362.html')
     ourUrl = opener.open(url).read()
     
     soup = BeautifulSoup(ourUrl)
     soup = soup.find("div", { "class" : "address-card" })
     #below code will delete tags except /br
     soup = str(soup)
     soup = soup.replace('<br/>' , '^')
     soup = BeautifulSoup(soup)
     soup = (soup.get_text())
     soup = str(soup)
     soup=soup.replace('^' , '<br/>')
     
     return soup

fullAddress = whiteScrape('http://www.whitepages.com/phone/1-978-251-1362')


#-------------Begin Split Add-----------------------------------------------
   
#split address into list - this will be useful for clearing out footer and other repetitive contents
def splitAddress(fullAddress , splitTerm = '^'):
    tempList=[]
    position = 0
    nextPosition = 0
    fullAddress = fullAddress.replace('<br/>' , '^')    
    fullAddress = fullAddress.replace('\n' , '')
    #last digit of last entry was being cut off so added an extra space
    fullAddress = fullAddress + ' '
    while nextPosition != -1:
        
        nextPosition = fullAddress.find(splitTerm , position  , len(fullAddress) )
        tempList.extend([fullAddress[position :nextPosition]])
        
        position = nextPosition + 1
        
        findZip(tempList)
    return tempList
