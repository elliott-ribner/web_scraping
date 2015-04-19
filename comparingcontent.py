def getContent():
     url_one = ('http://www.ostiguylandscape.com/landscaping.html')
     html_doc = opener.open(url_one).read()
     #url two is the primary index page
     url_two = ('http://www.ostiguylandscape.com/')
     html_docTwo = opener.open(url_two).read()
     soup = BeautifulSoup(html_doc)
     soupTwo = BeautifulSoup(html_docTwo)
     soupTwoOriginal = BeautifulSoup(html_docTwo)
     thelist = []
     thelistTwo = []
     uniqueList = []

     #clear unwanted tag

     for images in soup.find_all(['img' , 'a' , 'title' ]):
          images.extract()
     for images in soupTwo.find_all(['img' , 'a' , 'title' ]):
          images.extract()
     for images in soupTwoOriginal.find_all(['img' , 'a' , 'title' ]):
          images.extract()
     for tag in soup.find_all(True):
         thelist.extend([tag.get_text()])

     for tag in soupTwo.find_all(True):
         thelistTwo.extend([tag.get_text()])
     #sort list by length with shortest first, This insures that parents will never be
     #tested before their children, otherwise you will return larger sections than needed (i.e. html tag!)

     thelistTwo = sorted(thelistTwo, key=len)

     #goes through every entry in listtwo
     for entry in thelistTwo:
         #if listtwo entry not in listone (meaning tag string is not in the other page)
         if entry not in thelist:
             for tag in soupTwo.find_all(True):
                 if tag.get_text() == entry:
                     #checks for several tags that won't be useufl alone and therefore we should
                     #look for parent
                     while tag.name == 'span'or tag.name == 'font'or tag.name == 'b':
                          tag=tag.parent
                     if tag.name == 'li':
                          while tag.name != 'ul':
                               tag = tag.parent
                     if tag.name ==  'tr':
                          while tag.name != 'table':
                              tag = tag.parent
                     if tag.name ==  'td':
                          while tag.name != 'table':
                               tag = tag.parent
                     if tag.name ==  'strong':
                          #this may be a bad move as it does not have any clever loop to get to p etc
                               tag = tag.parent
                     #add check to see if parent - current tag is still unique
                     
                     tempvalue = tag.extract()
                     uniqueList.extend([tempvalue])
                     
                     #clear listTwo and replace with new version of soupTwo that has
                     #been decomposed of matched tag. Otherwise all parent tags would
                     #also be unqiue.
                     #we could add another feature like if entryAtag - (ie decompose)
                     #entry b tag and entryAtag is still unqique then restore entry b inside
                     #of a and get rid of individual entry b (as it can be kept inside A)
                     thelistTwo = []
                     for tag in soupTwo.find_all(True):
                         thelistTwo.extend([tag.get_text()])
                     #at the point the uniquelist is a random order list of our desired results

     #this code will order list correctly so that it can be inputted back html
     finalList = []
     for tab in soupTwoOriginal.find_all(True):
          for entryB in uniqueList:
               if tab == entryB:
                    finalList.extend([tab])

     #print '''if final list length != uniqueList then that means that one of the the the unique elements
     #must have been altered when another unqiue element that was inside the element was decomposed
     #perhaps we should reincorporate these by finding the missing element and trying to join it with
     #the other elements and running that against the theListTwo or some other method'''
     #converting contents to string and then joining them
     finalList = [str(entry) for entry in finalList]
     finalList = ''.join(finalList)
     print finalList
