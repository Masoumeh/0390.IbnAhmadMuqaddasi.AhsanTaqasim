# Normalization function

import re
import sys, codecs

def normalizeArabic(text):
    text = re.sub("[إأٱآا]", "ا", text)
    text = re.sub("ى", "ي", text)
    text = re.sub("ؤ", "ء", text)
    text = re.sub("ئ", "ء", text)
    text = re.sub("ه", "ة", text)
    text = re.sub("ک", "ك", text)
    #if text.startswith("ال"):
    #  text = text[2:] 
    return(text)

def normalizeArabicList(strList):
  for s in strList:  
    s = re.sub("[إأٱآا]", "ا", s)
    s = re.sub("ى", "ي", s)
    s = re.sub("ؤ", "ء", s)
    s = re.sub("ئ", "ء", s)
    s = re.sub("ه", "ة", s)
    s = re.sub("ک", "ك", s)
    #if s.startswith("ال"):
    #  s = s[2:] 
  return(strList)
