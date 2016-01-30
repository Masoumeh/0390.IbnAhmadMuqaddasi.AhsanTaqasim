from bs4 import BeautifulSoup
import sys  
import os

reload(sys)  
sys.setdefaultencoding('utf8')

FaAlphs = ['%D8%A7','%D8%A8']
Nums = [1204,1019]
nums = [1,0]
cnt = 0
for ch in FaAlphs:
  for n in range(0,nums[cnt]):
    os.system(u'phantomjs save_page.js http://library.tebyan.net/fa/Browse/Alphabet?Alpha='+ch+'#PageIndex='+str(nums[cnt]-1)+' > page.html')
    print('page.html created')
    cnt = cnt + 1
    data = open("page.html",'r').read()
    soup = BeautifulSoup(data, 'html.parser')
    arr = soup.find_all('a')
    for a in arr:
      if 'Viewer' in str(a.get('href')):
        if 'PDF' not in str(a.get('href')):
          bookURL = str(a.get('href'))
          bookURL = bookURL.replace('Switcher', 'Text')
          bookURL = bookURL[0:-1]+'1'
          print("bookurl"+bookURL)
          os.system(u'phantomjs save_page.js http://library.tebyan.net'+bookURL+' > content.html')
	  print(u'phantomjs save_page.js http://library.tebyan.net'+bookURL+' > content.html')       
          data2 = open("content.html",'r').read()
          soup2 = BeautifulSoup(data2, 'html.parser')
          arr3 = soup2.find_all('section')
	  for tmp in arr3:
            if 'PagingFooter' in tmp.get('class'):
                pageSize = int(str(tmp.input.string).strip()[1:].strip())
		if(pageSize == 1):
          	  arr2  = soup2.find_all('meta')
                  print(str(soup2.title.string))
	  	  with open(str(soup2.title.string), "w") as f2:      
                    f2.write(str(arr2[1].get('content')))
	          #exit()
                else:
                  for page in range(1,pageSize):
                    os.system(u'phantomjs save_page_book.js http://library.tebyan.net'+bookURL+'#'+ str(page) +' > bookpage.html')
	            print(u'phantomjs save_page_book.js http://library.tebyan.net'+bookURL+'#'+ str(page) +' > bookpage.html')       
                    data3 = open("bookpage.html",'r').read()
                    soup3 = BeautifulSoup(data3, 'html.parser')
                    arr2  = soup3.find_all('meta')
                    print(str(soup3.title.string))
	  	    with open(str(soup3.title.string), "a") as f2:      
                      f2.write('\n'+str(arr2[1].get('content')))
	              #exit()
