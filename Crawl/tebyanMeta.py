from bs4 import BeautifulSoup
import sys  
import os
import re

reload(sys)  
sys.setdefaultencoding('utf8')

faAlphs = ['%D8%A7','%D8%A8', '%D9%BE', '%D8%AA', '%D8%AB', '%D8%AC', '%DA%86', '%D8%AD', '%D8%AE'
            , 'D8%AF','%D8%B0', '%D8%B1', '%D8%B2' '%DA%98', '%D8%B3' , '%D8%B4', '%D8%B5', '%D8%B6'
            , '%D8%B7', '%D8%B8', '%D8%B9', '%D8%BA', '%D9%81', '%D9%82', '%DA%A9', '%DA%AF', '%D9%84'
            , '%D9%85', '%D9%86', '%D9%88', '%D9%87', '%DB%8C' ]
Nums = [1204,1018,264,981, 13, 250, 161, 308, 175, 425, 14, 466, 152, 6, 406, 335, 74, 29, 90, 11, 
        289, 47, 269, 171, 202, 141, 51, 1201, 676, 236, 121, 45]
nums = [1]
FaAlphs = ['%D8%A7']
cnt = 0
for ch in FaAlphs:
  for n in range(0,nums[cnt]):
    print("n " ,n, " ch: ", ch)
    os.system(u'phantomjs save_page.js http://library.tebyan.net/fa/Browse/Alphabet?Alpha='+ch+'#PageIndex='+str(n)+' > page.html')
    print('page.html created')
    data = open("page.html",'r').read()
    soup = BeautifulSoup(data, 'html.parser')
    arr = soup.find_all('a')
    pattern = re.compile("\/fa\/\d+\/")
    refs = set()
    for a in arr:
      ref = a.get('href')
      refs.add(ref)
    #print('refs ' , refs)
    for r in refs:
      #print("ref1 ", r)
      #rmChars = ['(',')']
      r = r.replace('(', '28')
      r = r.replace(')', '29')
      #print("ref2 ", r)
      if pattern.search(r):
        #print("ref include 	", r)
        os.system(u'phantomjs save_page.js http://library.tebyan.net'+ r +' > meta.html')
	 #  print(u'phantomjs save_page.js http://library.tebyan.net'+bookURL+' > content.html')       
        meta = open("meta.html",'r').read()
        soup2 = BeautifulSoup(meta, 'html.parser')
        pTitle =  soup2.title.string
        with open("metaData", "a") as f2:
          #print(pTitle)
          cnt = cnt + 1
          f2.write("********************************************* \n")
          f2.write( str(cnt) + ": " + pTitle.strip('0123456789'))
          f2.write("\n")
          f2.write("********************************************* \n")
          h1 = soup2.find_all('h1')
          for tmp in h1:
          #cnt = cnt+1
          #print("cnt:", cnt)
            #print(tmp.string)
          #if 'SquareBack' in tmp.get('class'):
          #with open("metaData", "a") as f2:#str(soup2.title.string), "w") as f2:      
            c = tmp.get('class')
            if c is not None:
              if 'TitleRow' in c:
                 #print(u'tRow' + tmp.string)
                titleStr = tmp.string
                f2.write(titleStr.strip())
              elif 'ValueRow' in c:
                valueStr = tmp.string
                if tmp.string is not None:
                  #print(u'value: ' + tmp.string)
                  f2.write(valueStr.strip() + "\n")
                else:
                  for a in tmp.findChildren():
                    #print("child: " , a)
                    if a.string is not None:
                      #print(u'non value: '+ a.string)
                      val = a.string
                      f2.write(val + ", ")
                f2.write("\n")
#                 valueStr = ''
print("all done!")

